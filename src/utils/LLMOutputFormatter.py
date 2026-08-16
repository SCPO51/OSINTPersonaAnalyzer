import json


class LLMOutputFormatter:
    @staticmethod
    def extract_json(response):
        try:
            start = response.find("{")
            end = response.rfind("}")
            return json.loads(response[start : end + 1])
        except:
            return {"keywords": []}

    @staticmethod
    def extract_md(response):
        try:
            start = response.find("```markdown")
            end = response.rfind("\n```")
            if start == -1 or end == -1:
                return response
            else:
                return response[start + 11 : end]
        except:
            return None
