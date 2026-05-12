import os, json
from dotenv import load_dotenv
from groq import Groq
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

load_dotenv()


class Settings:
    """Class for centralised settings usage"""
    
    def __init__(self):
        self.tg_token: str = os.getenv("TG_TOKEN", "")
        self.groq_key: str = os.getenv("GROQ_KEY", "")
        
        self.user_1 = int(os.getenv("USER_ID_1", 0))
        self.user_2 = int(os.getenv("USER_ID_2", 0))
        self.allowed_users: list[int] = [self.user_1, self.user_2]

        self.db_name: str = os.getenv("DB_NAME", "database/main.db")

        self.instructions: str = self._load_instructions()

        self.groq_client = Groq(api_key=self.groq_key)
        self.bot = Bot(
            token=self.tg_token, 
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )


    def _load_instructions(self) -> str:
        """Inner method for reading instructions"""
        
        try:
            with open("instuctions.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("system_instruction", "You a smart homelab asistant.")
        except FileNotFoundError:
            print("⚠️ File instuctions.json not found! Default promt will be used.")
            return "You a smart homelab asistant."

config = Settings()