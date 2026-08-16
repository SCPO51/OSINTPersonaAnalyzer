class DebugInfo:
    @staticmethod
    def search_analyze(main_person,keyword,keywords_json):
        debug_str=""
        debug_str+=f"[关联发现] {main_person} & {keyword} → {keywords_json.get('reason','')}\n"
        #print(debug_str,end="")
        return debug_str

    @staticmethod
    def keywords_analyze(main_person,keyword,keywords_json):
            debug_str=""
            debug_str+=(f"\n{'='*60}\n")
            debug_str+=("推理关键词\n")
            debug_str+=(f"核心人物: {main_person}\n")
            debug_str+=(f"输入关键词: {str(keyword)}\n")
            debug_str+=('-'*60+"\n")
            
            if keywords_json.get('keywords'):
                debug_str+=("生成关键词:\n")
                debug_str+=(f"{str(keywords_json.get('keywords', []))}")
                
                debug_str+=("\n推理解释:\n")
                for kw, reason in keywords_json.get('reason', {}).items():
                    debug_str+=(f"{kw} → {reason}\n")
            else:
                debug_str+=("未生成有效关键词\n")
            
            debug_str+=('='*60+"\n")

            #print(debug_str,end="")
            return debug_str

    @staticmethod
    def search_extraction(syntax,keywords_json):
        debug_str=""
        debug_str+=f"[精确搜索] {syntax}  → {keywords_json.get('reason','')}\n"
        #print(debug_str,end="")
        return debug_str

    @staticmethod
    def ddg_analyze(syntax_json):
        debug_str=""
        debug_str+=("推理搜索语法\n")
        for i in syntax_json:
            debug_str+=(f'{i["syntax"]}  →  {i["reason"]}\n')

        debug_str+=('='*60+"\n")
        #print(debug_str,end="")
        return debug_str