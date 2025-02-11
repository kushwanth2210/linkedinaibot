import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_community.chat_models import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.callbacks import StreamingStdOutCallbackHandler

# Load environment variables
load_dotenv()


class LanguageModels:
    def __init__(self, model="claude-3-opus-20240229"):
        """
        Initialize the LanguageModels class with a default model.
        Supports Claude, OpenAI, and Gemini models.
        """
        self.model = model
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")

    def get_model(self, temperature=0.7):
        """
        Returns an instance of the selected language model based on the model ID.
        """
        if self.model.startswith("claude"):
            return self._claude_model()
        elif self.model.startswith("gpt-4") or self.model.startswith("gpt-3"):
            return self._openai_model(temperature)
        elif self.model.startswith("gemini"):
            return self._gemini_model()
        else:
            raise ValueError(f"Unsupported model: {self.model}")

    def _claude_model(self):
        """
        Returns an Anthropic Claude model instance.
        """
        if not self.anthropic_api_key:
            raise ValueError("Missing Anthropic API Key. Check your environment variables.")
        
        return ChatAnthropic(
            model=self.model,
            anthropic_api_key=self.anthropic_api_key,
            callbacks=[StreamingStdOutCallbackHandler()],
        )

    def _openai_model(self, temperature):
        """
        Returns an OpenAI GPT model instance.
        """
        if not self.openai_api_key:
            raise ValueError("Missing OpenAI API Key. Check your environment variables.")
        
        return ChatOpenAI(
            model=self.model,
            temperature=temperature,
            openai_api_key=self.openai_api_key,
            callbacks=[StreamingStdOutCallbackHandler()],
        )

    def _gemini_model(self):
        """
        Returns a Google Gemini model instance.
        """
        if not self.gemini_api_key:
            raise ValueError("Missing Google API Key. Check your environment variables.")
        
        return ChatGoogleGenerativeAI(
            model=self.model,
            google_api_key=self.gemini_api_key,
            callbacks=[StreamingStdOutCallbackHandler()],
        )


# Example usage:
if __name__ == "__main__":
    lm = LanguageModels(model="claude-3-opus-20240229")  # Default to Claude
    model_instance = lm.get_model()
    print(f"Using model: {model_instance}")
