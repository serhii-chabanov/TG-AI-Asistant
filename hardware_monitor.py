import os
import asyncio
import logging
from database.database import db

logger = logging.getLogger(__name__)

CPU_TEMP_LIMIT = 70.0  
CHECK_INTERVAL = 30    

THERMAL_ZONE_PATH = "/sys/class/thermal/thermal_zone0/temp"

async def get_aml_cpu_temp():
    """Зчитування температури процесора для архітектури Amlogic на Armbian"""
    if os.path.exists(THERMAL_ZONE_PATH):
        try:
            with open(THERMAL_ZONE_PATH, "r") as f:
                raw_temp = f.read().strip()
                return float(raw_temp) / 1000.0
        except Exception as e:
            logger.error(f"Помилка читання файлу температури Armbian: {e}")
    return None

async def check_hardware(bot, admin_id):
    while True:
        try:
            cpu_temp = await get_aml_cpu_temp()

            if cpu_temp and cpu_temp >= CPU_TEMP_LIMIT:
                msg = f"🚨 КРИТИЧНИЙ ПЕРЕГРІВ X96: CPU {cpu_temp:.1f}°C! Систему буде вимкнено через 10 секунд!"
                logger.error(msg)
                
                db.add_record("logs", admin_id, {"level": "CRITICAL", "message": msg})
                
                await bot.send_message(admin_id, msg)
                await asyncio.sleep(10)
                
                os.system("sudo shutdown -h now") 
                
        except Exception as e:
            logger.error(f"Hardware monitor error: {e}")
            
        await asyncio.sleep(CHECK_INTERVAL)