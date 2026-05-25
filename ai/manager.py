import json
import logging
from collections import defaultdict, deque
from config import config
from database.database import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "universal_add",
            "description": "Додати один або кілька нових записів у базу даних. Передавай масив об'єктів у параметрі 'records'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string", 
                        "enum": [
                            "finance", "products", "routine", "habits", "events", 
                            "general_knowledge", "media_tracker", "sport_logs", "meal_plan"
                        ],
                        "description": "Назва таблиці для запису."
                    },
                    "records": {
                        "type": "array",
                        "description": "Список об'єктів з даними для додавання. Навіть якщо елемент один, він має бути всередині масиву [].",
                        "items": {
                            "type": "object",
                            "description": "Поля об'єкта відповідно до схеми таблиці."
                        }
                    }
                },
                "required": ["table_name", "records"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "universal_search",
            "description": "Пошук інформації, отримання звітів або перевірка списків за фільтрами.",
            "parameters": {
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "enum": [
                            "finance", "products", "routine", "habits", "events", 
                            "general_knowledge", "media_tracker", "sport_logs", "meal_plan"
                        ],
                        "description": "В якій таблиці шукать."
                    },
                    "filters": {
                        "type": "object",
                        "description": "Критерії пошуку (наприклад: {'status': 'buy'} або {'meal_type': 'Сніданок'})."
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
        self.history = defaultdict(lambda: deque(maxlen=50))

    async def get_response(self, user_text: str, user_id: int) -> str:
        messages = [{"role": "system", "content": config.instructions}]
        messages.extend(list(self.history[user_id]))
        
        current_user_message = {"role": "user", "content": user_text}
        messages.append(current_user_message)

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
                self.history[user_id].append(current_user_message)
                self.history[user_id].append({"role": "assistant", "content": response_message.content})
                return response_message.content

            messages.append(response_message)

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                
                logger.info(f"User {user_id} calls {function_name} with {arguments}")
                
                function_result = ""

                try:
                    if function_name == "universal_add":
                        records_list = arguments.get("records", [])
                        db.add_records_bulk(
                            table_name=arguments["table_name"],
                            user_id=user_id,
                            data_list=records_list
                        )
                        function_result = f"✅ Успішно додано {len(records_list)} запис(ів) в таблицю {arguments['table_name']}"

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
            
            final_content = second_response.choices[0].message.content
            
            self.history[user_id].append(current_user_message)
            self.history[user_id].append({"role": "assistant", "content": final_content})
            
            return final_content

        except Exception as e:
            logger.error(f"AI Manager error: {e}")
            return f"Вибач, сталася помилка при обробці запиту: {str(e)}"

ai = AIManager()