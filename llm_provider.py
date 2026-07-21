import os
import json
from dotenv import load_dotenv

from google import genai
from openai import OpenAI

from google.genai import types

load_dotenv()

class LLMProvider:
    def __init__(self, provider, messages) -> None:
        self.__messages = messages
        self.__provider = provider
        self.__load_config()

    def __load_config(self) -> None:
        try:
            with open("./config.json", "r") as file:
                self.__config = json.load(file)

                self.__llm_config = self.__config[self.__provider]
                self.__configure_llm()

        except FileNotFoundError as fnfe:
            raise FileNotFoundError(f"Config File cannot be found: {fnfe}")

    def __configure_llm(self):
        self.__api_key = os.getenv("GEMINI_API_KEY" if self.__provider == "gemini" else "OPENAI_API_KEY")

        if not self.__api_key:
            raise ValueError("GEMINI_API_KEY is not set in your environment or .env file.")


    def run_gemini_llm(self) -> str:
        try:
            self._client = genai.Client(api_key = self.__api_key)
            conversations = "\n".join(f"{message['role']}: {message['content']}" for message in self.__messages)
            interaction = self._client.models.generate_content(
                model = self.__llm_config["model"],
                contents = conversations,
                config = types.GenerateContentConfig(
                    max_output_tokens = int(self.__llm_config.get("max_token", 500)),
                    temperature = float(self.__llm_config.get("temperature", 1.0)),
                    top_p = float(self.__llm_config.get("top_p", 0.8))
                )
            )
            return (interaction.text or "").strip()

        except RuntimeError as re:
            raise RuntimeError(f"Gemini LLM Failed: {re}")
    

    def run_openai_llm(self) -> str:
        try:
            self._client = OpenAI(api_key = self.__api_key)
            interaction = self._client.responses.create(
                input = self.__messages,
                model = self.__llm_config["model"],
                top_p = float(self.__llm_config.get("top_p", 0.8)),
                temperature = float(self.__llm_config.get("temperature", 1.0)),
                max_output_tokens = int(self.__llm_config.get("max_token", 500)),
            )
            return interaction.output_text.strip()

        except RuntimeError as re:
            raise RuntimeError(f"OpenAI LLM Failed: {re}")