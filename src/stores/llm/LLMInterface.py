from abc import ABC, abstractmethod


class LLMinterface(ABC):

# hayde l abstract method ma betnaffez shi bas ayya class badde y inheret mn llminterface majboor 
# yesta3mel hol l functions.

    # Hayde l function bte5od ayya model baddak yee (Ollama, OpenAI, coHere, ..)
    @abstractmethod
    def set_generation_model(self, model_id: str):
        pass

    # Hayde l function bte5od l embedding model
    @abstractmethod
    def set_embedding_model(self, model_id: str, embedding_size: int):
        pass


    # hayde function btrage3le text addesh tola w eza be2allef aw begeb text mafhom mneh.
    @abstractmethod
    def generate_text(self, prompt: str, chat_history: list = [], max_output_tokens: int = None,
                      temperature: float = None):
        pass

    # Hayde bta3mal embedding lal text bt7awlo la vectors
    @abstractmethod
    def embeded_text(self, text: str, document_type: str = None):
        pass

    #hayde bthadded eza l prompt ly jeye howwe so2al wala text wala w bta3mal process w bt3ed seya8to abl ma 
    # generate text yerja3 yesta5dmo

    @abstractmethod
    def construct_prompt(self, prompt: str, role: str):
        pass


