from .LLMEnum import LLEnum
from .providers import CoHereProvider, OpenAIProviders

class LLMProviderFactory:

    def __init__(self, config: dict):
        self.config = config

    def create(self, provider_name: str ):

        if provider_name == LLEnum.OPENAI.value:
            return OpenAIProviders(

                api_key = self.config.OPENAI_API_KEY,
                api_url = self.config.OPENAI_API_URL,
                default_input_max = self.config.default_input_max_char,
                default_output_max = self.config.default_output_max_char,
                default_temp = self.config.temperature,
            )

        if provider_name == LLEnum.COHERE.value:
            return CoHereProvider(

                api_key = self.config.COHERE_API_KEY,
                default_input_max_char = self.config.default_input_max_char,
                default_output_max_char = self.config.default_output_max,
                default_temp = self.config.temperature




            )

        return None
            

