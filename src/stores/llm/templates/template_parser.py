import os

class TemplateParser:

    def __init__(self, language: str, default_lang: str = "en"):

        # hayda ana hala2 ween aw l file hayda wayno
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.default_language = default_lang
        self.language = language

    def set_language(self, language: str):

        if not language:
            self.language = self.default_language

        # awwal shi badde et2akad enno 3nde l language ly badde yeha

        language_path = os.path.join(self.current_path, "locales", language)
        if language or os.path.exists(language_path):
            self.language = language

        else:
            self.language = self.default_language


    def get(self, group: str, key: str, vars: dict={}):
        if not group or not key:
            return None
        
        group_path = os.path.join(self.current_path, "locales", self.language, f"{group}.py")
        targeted_language = self.language
        if not os.path.exists(group_path):
            group_path = os.path.join(self.current_path, "locales", self.default_language, f"{group}.py" )
            targeted_language = self.default_language

        if not os.path.exists(group_path):
            return None
        
        # import group module in runtime yaany bnos l code msh bl awwal abel ma y2alle3 __import__
        
        module = __import__(f"stores.llm.templates.locales.{targeted_language}.{group}", fromlist=[group])

        if not module:
            return None
        
        key_attribute = getattr(module, key)
        return key_attribute.substitute(vars)

        
        
