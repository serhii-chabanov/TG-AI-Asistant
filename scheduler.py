import aiohttp
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database.database import db

scheduler = AsyncIOScheduler(timezone="Europe/Copenhagen")

async def get_weather():
    url = "https://wttr.in/Viby?format=j1"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json(content_type=None)
                    
                    today_data = data['weather'][0]
                    max_temp = today_data['maxtempC']
                    min_temp = today_data['mintempC']
                    
                    hourly = today_data['hourly']
                    
                    morning_temp = hourly[3]['tempC']
                    morning_desc = hourly[3]['lang_uk'][0]['value'] if 'lang_uk' in hourly[3] else hourly[3]['weatherDesc'][0]['value']
                    
                    afternoon_temp = hourly[4]['tempC']
                    afternoon_desc = hourly[4]['lang_uk'][0]['value'] if 'lang_uk' in hourly[4] else hourly[4]['weatherDesc'][0]['value']
                    
                    evening_temp = hourly[6]['tempC']
                    evening_desc = hourly[6]['lang_uk'][0]['value'] if 'lang_uk' in hourly[6] else hourly[6]['weatherDesc'][0]['value']
                    
                    precip_chance = hourly[0]['chanceofrain']
                    
                    return (
                        f"Загалом: від <b>{min_temp}°C</b> до <b>{max_temp}°C</b>\n"
                        f"Ймовірність опадів: <b>{precip_chance}%</b>\n"
                        f"=================================\n"
                        f"Ранок (09:00): <b>{morning_temp}°C</b> ({morning_desc})\n"
                        f"Обід (12:00): <b>{afternoon_temp}°C</b> ({afternoon_desc})\n"
                        f"Вечір (18:00): <b>{evening_temp}°C</b> ({evening_desc})"
                    )
                else:
                    return f"⚠️ Помилка сервера погоди: статус {response.status}"
    except Exception as e:
        return f"⚠️ Не вдалося завантажити погоду: {e}"

async def check_upcoming_events(bot, user_id):
    now = datetime.now()
    
    max_target_time = (now + timedelta(minutes=90)).strftime("%Y-%m-%d %H:%M")
    
    query = "SELECT * FROM events WHERE reminded = 0 AND event_time <= ?"
    db.cursor.execute(query, (max_target_time,))
    
    cols = [column[0] for column in db.cursor.description]
    upcoming_events = [dict(zip(cols, row)) for row in db.cursor.fetchall()]
    
    for event in upcoming_events:
        message_text = f"⏰ <b>Завчасне нагадування! Подія через 1.5 години</b>\n\n📌 Подія: <b>{event['title']}</b>\n Час: <b>{event['event_time']}</b>"
        try:
            await bot.send_message(user_id, message_text, parse_mode="HTML")
            
            db.cursor.execute("UPDATE events SET reminded = 1 WHERE id = ?", (event['id'],))
            db.conn.commit()
        except Exception as e:
            print(f"Помилка відправки нагадування: {e}")


async def send_morning_digest(bot, user_id):
    today_date = datetime.now().strftime("%Y-%m-%d")
    
    events = db.get_records("events", user_id, filters={"event_time": today_date})
    routine = db.get_records("routine", user_id)
    habits = db.get_records("habits", user_id)  
    
    weather_info = await get_weather()
    
    digest = "<b>Ранковий дайджест O.R.I.O.N.</b>\n\n"
    digest += f"🌍 <b>Погода на сьогодні:</b>\n{weather_info}\n\n"
    
    digest += "📅 <b>Події та зустрічі на сьогодні:</b>\n"
    if events:
        for e in events:
            digest += f"• {e['title']} ({e['event_time']})\n"
    else:
        digest += "• Зустрічей чи особливих подій немає.\n"
        
    digest += "\n📝 <b>Поточні регулярні справи (Routine):</b>\n"
    if routine:
        for r in routine[:5]:
            digest += f"• {r['task_name']} (кожні {r['frequency_days']} дн.)\n"
    else:
        digest += "• Список задач порожній.\n"
        
    digest += "\n💪 <b>Твої звички та прогрес:</b>\n"
    if habits:
        for h in habits:
            digest += f"• {h['habit_name']}: [{h['progress_count']}/{h['frequency_per_week']} на тиждень]\n"
    else:
        digest += "• Звички ще не додано.\n"
        
    await bot.send_message(user_id, digest, parse_mode="HTML")


def setup_scheduler(bot, user_id):
    scheduler.add_job(send_morning_digest, "cron", hour=21, minute=59, args=[bot, user_id])
    
    scheduler.add_job(check_upcoming_events, "interval", minutes=1, args=[bot, user_id])
    
    scheduler.start()