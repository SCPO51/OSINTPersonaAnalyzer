from src.common import *
from src.utils import *
import datetime


class SearchIntelligenceEngine:
    def __init__(self, main_person, proxy, keywords):
        self.main_person = main_person

        self.keywords = []
        for i in keywords:
            self.keywords.append({"keyword": i, "link": ""})

        self.strong_relevance_keywords = (
            f"{main_person} {self.keywords[0]['keyword']}"  # 强关联关键字
        )

        self.log = self.keywords.copy()
        self.proxy = proxy
        self.seen = set({main_person})

        self.net = NetworkManager()
        self.config = Config()

        current_datetime = datetime.datetime.now()
        self.formatted_datetime = current_datetime.strftime("%Y_%m_%d_%H_%M")
        self.file_path = f"./src/report/{self.formatted_datetime}_{main_person}"
        self.log_path = f"./src/log/{self.formatted_datetime}_{main_person}"

        self.md = None

        self.net.add_node(main_person, "original", "orange")
        for i in self.keywords:
            self.net.add_node(i["keyword"], "original", "orange")
            self.net.add_edge(main_person, i["keyword"])

        self.debug = ""

        self.stop = False

    def _stop(self):
        self.stop = True

    def save_graph(self):
        self.net.save_html(self.file_path + ".html")

    def get_graph_html(self):
        return self.net.generate_html()

    def get_md_html(self):
        if self.md is not None:
            return md_to_html(self.md)
        else:
            return ""

    def save_md(self):
        with open(self.file_path + ".md", "w", encoding="utf-8") as f:
            f.write(self.md)

    def save_log(self):
        with open(self.log_path + ".json", "a", encoding="utf-8") as f:
            for i in self.log:
                f.write(str(i).strip() + "\n")

    def search_and_analyze(self, keyword):
        search_results = Crawler.duckduckgo(keyword, self.proxy)
        if len(search_results) == 0:
            return {"keywords": []}
        prompt = PromptGenerator.generate_search_extraction_prompt(
            self.main_person, keyword, search_results
        )
        system_prompt = PromptGenerator.generate_system_search_extraction_prompt(
            self.main_person, keyword
        )
        model = self.config.get_base_model()
        analysis_report = LLMClient.ask(model, prompt, system=system_prompt)
        return LLMOutputFormatter.extract_json(analysis_report)

    def keywords_analyze(self, keywords_json):
        prompt = PromptGenerator.construct_inferred_search_terms_prompt(
            self.strong_relevance_keywords, keywords_json
        )
        # prompt = PromptGenerator.construct_inferred_search_terms_prompt(
        #     self.main_person, keywords_json
        # )
        system_prompt = PromptGenerator.system_construct_inferred_search_terms_prompt(
            self.main_person
        )
        model = self.config.get_reasoning_model()
        analysis_report = LLMClient.ask(model, prompt, system=system_prompt)
        return LLMOutputFormatter.extract_json(analysis_report)

    def generate_ddg_syntax(self, keywords_json):
        prompt = PromptGenerator.generate_advanced_ddg_syntax_prompt(
            self.main_person, keywords_json
        )
        system_prompt = PromptGenerator.system_generate_advanced_ddg_syntax_prompt(
            self.main_person
        )
        model = self.config.get_reasoning_model()
        analysis_report = LLMClient.ask(
            model, prompt, system=system_prompt, temperature=0.7
        )
        return LLMOutputFormatter.extract_json(analysis_report)["search"]

    def report_generate(self, keywords_json):
        prompt = PromptGenerator.pre_report_generate_prompt(
            self.main_person, keywords_json
        )
        system_prompt = PromptGenerator.system_pre_report_generate_prompt()

        model = self.config.get_reasoning_model()
        analysis_report = LLMClient.ask(model, prompt, system=system_prompt)
        return LLMOutputFormatter.extract_md(analysis_report)

    def iterate_report_generate(self, keywords_json):
        prompt = PromptGenerator.iterate_report_generate_prompt(self.md, keywords_json)
        system_prompt = PromptGenerator.system_iterate_report_generate_prompt()

        model = self.config.get_reasoning_model()
        analysis_report = LLMClient.ask(model, prompt, system=system_prompt)
        number_rows = len(self.md.split("\n"))
        md = LLMOutputFormatter.extract_md(analysis_report)
        if len(md.split("\n")) >= number_rows:
            self.md = md

    def add_node_and_dedupe(self, keyword, keywords_json):
        for i in keywords_json["keywords"]:
            if type(i) == dict:
                if i["keyword"] not in self.seen:
                    self.net.add_node(i["keyword"], i["link"])
                    self.net.add_edge(i["keyword"], keyword)

                    self.seen.add(i["keyword"])
                    self.keywords.insert(0, i)
                    self.log.append(i)

    def pre_report_generate(self):
        keyword = self.keywords.pop()
        search_json = self.search_and_analyze(
            f"{self.main_person} {keyword['keyword']}"
        )  # 获取搜索结果，并分析关联关键字
        self.debug += DebugInfo.search_analyze(
            self.main_person, f"{self.main_person} {keyword['keyword']}", search_json
        )

        keywords_json = self.keywords_analyze(
            search_json
        )  # 分析初关联结果，生成强关联关键字
        self.debug += DebugInfo.keywords_analyze(
            self.main_person, search_json["keywords"], keywords_json
        )

        self.add_node_and_dedupe(
            keyword["keyword"], keywords_json
        )  # 加入节点，并去重关键字

        self.md = self.report_generate(keywords_json)  # 生成预报告

    def run(self):
        self.pre_report_generate()  # 生成预报告
        self.debug += "预报告生成\n"
        while len(self.keywords) > 0:
            keyword = self.keywords.pop()

            if self.stop:
                break
            search_json = self.search_and_analyze(
                f"{self.main_person} {keyword['keyword']}"
            )  # 获取搜索结果，并分析关联关键字
            self.debug += DebugInfo.search_analyze(
                self.main_person,
                f"{self.main_person} {keyword['keyword']}",
                search_json,
            )
            if self.stop:
                break

            keywords_json = self.keywords_analyze(
                search_json
            )  # 分析初关联结果，生成强关联关键字
            self.debug += DebugInfo.keywords_analyze(
                self.main_person, search_json["keywords"], keywords_json
            )
            if self.stop:
                break

            self.add_node_and_dedupe(
                keyword["keyword"], keywords_json
            )  # 加入节点，并去重关键字
            if self.stop:
                break

            syntax_json = self.generate_ddg_syntax(
                keywords_json
            )  # 生成duckduckgo搜索语法
            self.debug += DebugInfo.ddg_analyze(syntax_json)
            if self.stop:
                break

            syntax_keywords_lst = []
            for i in syntax_json:
                keywords_json = self.search_and_analyze(
                    str(i["syntax"])
                )  # 根据搜索语法精确搜索目标，并分析关联关键字
                self.debug += DebugInfo.search_extraction(i["syntax"], keywords_json)
                if self.stop:
                    break

                for j in keywords_json.get("keywords", []):
                    syntax_keywords_lst.append(j)  # 保存精确搜索分析后关联结果

            if self.stop:
                break
            precise_keywords_json = self.keywords_analyze(
                str(syntax_keywords_lst)
            )  # 分析精确搜索后关联结果，生成强关联关键字
            self.debug += DebugInfo.keywords_analyze(
                self.main_person, syntax_keywords_lst, precise_keywords_json
            )
            if self.stop:
                break

            self.add_node_and_dedupe(
                keyword["keyword"], precise_keywords_json
            )  # 加入节点，并去重关键字

            self.iterate_report_generate(precise_keywords_json)  # 迭代对预报告进行完善
            self.debug += "完善预报告\n"
            if self.stop:
                break
        self.debug += "任务结束\n"