# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request, Response
from threading import Thread
from src.core.SearchIntelligenceEngine import SearchIntelligenceEngine
from urllib.parse import quote
import uuid
import time
import threading

task_lock = threading.Lock()

app = Flask(__name__)
tasks = {}  # 全局任务存储
g_proxy = None


class TaskRunner(Thread):
    def __init__(self, task_id, main_person, keywords):
        super().__init__()
        self.task_id = task_id
        self.engine = SearchIntelligenceEngine(
            main_person=main_person,
            keywords=keywords,
            proxy=g_proxy,
        )
        self._stopped = False

    def stop(self):
        if not self._stopped:
            self.engine._stop()
            self._stopped = True

    def run(self):
        with task_lock:
            tasks[self.task_id]["status"] = "running"
            tasks[self.task_id]["engine"] = self.engine
        try:
            self.engine.run()
            with task_lock:
                tasks[self.task_id].update(
                    {
                        "status": "completed",
                        "debug": self.engine.debug,
                        "net": self.engine.net,
                        "md": self.engine.md,
                    }
                )
        except Exception as e:
            with task_lock:
                tasks[self.task_id]["status"] = f"error: {str(e)}"


# API端点
@app.route("/add_task")
def add_task():
    """启动新的分析任务"""
    main_person = request.args.get("person")
    keywords = request.args.getlist("keyword")  # 支持多个keyword参数

    if not main_person or not keywords:
        return jsonify({"error": "Missing parameters"}), 400

    task_id = str(uuid.uuid4())

    # 启动后台任务
    runner = TaskRunner(task_id, main_person, keywords)

    with task_lock:
        tasks[task_id] = {
            "status": "pending",
            "create_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "person": main_person,
            "keywords": keywords,
            "thread": runner,
        }
    runner.start()

    return jsonify(
        {
            "task_id": task_id,
            "monitor_url": f"/task/{task_id}",
            "graph_url": f"/task/{task_id}/graph",
            "report_url": f"/task/{task_id}/report",
            "debug_url": f"/task/{task_id}/debug",
        }
    )


@app.route("/task/<task_id>")
def get_task(task_id):
    """获取任务详情"""
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    response = {
        "status": task["status"],
        "person": task["person"],
        "keywords": task["keywords"],
        "create_time": task["create_time"],
    }

    return jsonify(response)


@app.route("/tasks")
def list_tasks():
    """列出所有任务"""
    return jsonify(
        [
            {
                "id": tid,
                "person": info["person"],
                "status": info["status"],
                "create_time": info["create_time"],
            }
            for tid, info in tasks.items()
        ]
    )


@app.route("/task/<task_id>/graph")
def get_network_graph(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    html_content = task["engine"].net.generate_html()  # 假设已实现生成HTML的方法

    if "download" in request.args:
        filename = f"{task['person']}_graph.html"
        safe_filename = quote(filename, safe="", encoding="utf-8")
        content_disposition = f"attachment; filename*=UTF-8''{safe_filename}"
        return Response(
            html_content,
            mimetype="text/html",
            headers={
                "Content-Disposition": content_disposition,
                "Content-Type": "text/html; charset=utf-8",
            },
        )
    return Response(html_content, mimetype="text/html")


@app.route("/task/<task_id>/report")
def get_report_html(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    if "download" in request.args:

        filename = f"{task['person']}_report.md"
        safe_filename = quote(filename, safe="", encoding="utf-8")
        content_disposition = f"attachment; filename*=UTF-8''{safe_filename}"

        return Response(
            task["engine"].md,
            mimetype="text/markdown",
            headers={
                "Content-Disposition": content_disposition,
                "Content-Type": "text/markdown; charset=utf-8",
            },
        )
    return Response(task["engine"].get_md_html(), mimetype="text/html")


@app.route("/task/<task_id>/debug")
def get_debug_html(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return Response(
        task["engine"].debug,
        mimetype="text/plain; charset=utf-8",  # 明确指定字符集
        headers={
            "Content-Type": "text/plain; charset=utf-8",  # 双重保障
            "Cache-Control": "no-cache",  # 避免缓存旧数据
        },
    )


@app.route("/task/<task_id>/stop")
def stop_task(task_id):

    task = tasks.get(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    current_status = task["status"]

    if current_status not in ("pending", "running"):
        return jsonify({"error": f"Cannot stop task in {current_status} state"}), 409

    runner = task.get("thread")
    if not runner or not isinstance(runner, TaskRunner):
        return jsonify({"error": "Thread not found"}), 500

    runner.stop()
    with task_lock:
        task["status"] = "completed"

    return jsonify(
        {
            "status": "completed",
            "monitor_url": f"/task/{task_id}",
            "message": "Stop signal received, waiting for termination...",
        }
    )


def start(proxy):
    global g_proxy
    g_proxy = proxy
    app.run(host="0.0.0.0", port=5000, threaded=True)


if __name__ == "__main__":
    start()
