from ..LLMInterface import LLMinterface
from openai import OpenAI
import logging
from ..LLMEnum import OpenAIEnum


class OpenAIProvider(LLMinterface):

    def __init__(self, api_key: str, api_url: str = None,
                 default_input_max_char: int = 1000, 
                 default_output_max_char: int = 1000,
                 temperature: float = 0.1,):
        
        self.api_key = api_key
        self.api_url = api_url

        self.default_input_max = default_input_max_char
        self.default_output_max = default_output_max_char
        self.default_temp = temperature

        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None

        self.client = OpenAI(
            api_key = self.api_key,
            base_url = self.api_url if self.api_url and len(self.api_url) else None
            )
        
        self.enums = OpenAIEnum
        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id: str):
        
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):

         self.embedding_model_id = model_id
         self.embedding_size = embedding_size

    def process_text(self, text: str):
        return text[:self.default_input_max].strip()

    def generate_text(self, prompt: str, chat_history: list=[], max_output_tokens: int = None,
                      temperature: float = None):
        
        if not self.client:
            self.logger.error(" OpenAI client was not set")
            return None 
        
        if not self.generation_model_id:
            self.logger.error("Generation model for OpenAI was not set")
            return None
        
        max_output_tokens = max_output_tokens if max_output_tokens else self.default_output_max
        temperature = temperature if temperature else self.default_temp

        chat_history.append(
            self.construct_prompt(prompt = prompt, role = OpenAIEnum.USER.value)
        )

        response = self.client.chat.completions.create(
            model = self.generation_model_id,
            messages = chat_history,
            max_tokens = max_output_tokens,
            temperature = temperature
        )

        if not response or not response.choices or len(response.choices) == 0 or not response.choices[0].message:
            self.logger.error(" Erro while generation with OpenAI")
            return None
        
        return response.choices[0].message.content


    def embeded_text(self, text: str, document_type: str = None):

        if not self.client:
            self.logger.error(" OpenAI client was not set")
            return None 
        
        if not self.embedding_model_id:
            self.logger.error("Embedding model for OpenAI was not set")
            return None
        
        response = self.client.embeddings.create(

            model = self.embedding_model_id,
            input = text,
        )
        
        if not response or not response.data or not len(response.data) == 0 or not response.data[0].embedding:
            self.logger.error("Error while embedding text with OpenAI")
            return None
        
        return response.data[0].embedding
    
    def construct_prompt(self, prompt: str, role: str):

        return {
            "role" : role,
            "content": self.process_text(prompt),
        }

