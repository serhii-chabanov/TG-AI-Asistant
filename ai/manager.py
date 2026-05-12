import json
import logging
from config import config
from database.database import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "universal_add",
            "description": "Додати новий запис у базу даних. Використовуй для фінансів, продуктів, звичок тощо.",
            "parameters": {
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string", 
                        "enum": ["finance", "products", "routine", "habits", "events", "general_knowledge"],
                        "description": "Назва таблиці для запису."
                    },
                    "data": {
                        "type": "object",
                        "description": "Словник з даними. Наприклад: {'amount': 100, 'record_type': 'expense', 'category': 'Food'}"
                    }
                },
                "required": ["table_name", "data"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "universal_search",
            "description": "Пошук інформації, отримання звітів або перевірка списків.",
            "parameters": {
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "enum": ["finance", "products", "routine", "habits", "events", "general_knowledge"],
                        "description": "В якій таблиці шукати."
                    },
                    "filters": {
                        "type": "object",
                        "description": "Критерії пошуку (наприклад: {'status': 'buy'} або {'category': 'Food'})."
                    }
                },
                "required": ["table_name"]
            }
        }
    }
]

class AIManager:
    def __init__(self):
        self.client = config.groq_client
        self.model = "llama-3.3-70b-versatile"

    async def get_response(self, user_text: str, user_id: int) -> str:
        messages = [
            {"role": "system", "content": config.instructions},
            {"role": "user", "content": user_text}
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto"
            )

            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            if not tool_calls:
                return response_message.content

            messages.append(response_message)

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                
                logger.info(f"User {user_id} calls {function_name} with {arguments}")
                
                function_result = ""

                try:
                    if function_name == "universal_add":
                        db.add_record(
                            table_name=arguments["table_name"],
                            user_id=user_id,
                            data=arguments["data"]
                        )
                        function_result = f"✅ Успішно додано в таблицю {arguments['table_name']}"

                    elif function_name == "universal_search":
                        records = db.get_records(
                            table_name=arguments["table_name"],
                            user_id=user_id,
                            filters=arguments.get("filters")
                        )

                        function_result = json.dumps(records, ensure_ascii=False)

                except Exception as db_error:
                    logger.error(f"Database error: {db_error}")
                    function_result = f"❌ Помилка бази даних: {str(db_error)}"

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": function_result
                })

            second_response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            
            return second_response.choices[0].message.content

        except Exception as e:
            logger.error(f"AI Manager error: {e}")
            return f"Вибач, сталася помилка при обробці запиту: {str(e)}"

ai = AIManager()