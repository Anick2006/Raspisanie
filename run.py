import asyncio
from aiogram import Bot, Dispatcher, types
from datetime import datetime, timedelta
import pytz
import sqlite3
import aioschedule

API_TOKEN = '6179636739:AAEhy5zFGSZ4VQbG-Oie0MmiHklb4lX1ZYE'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Создаем подключение к базе данных
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Создаем таблицу для хранения user_ids, если она еще не существует
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (user_id INTEGER PRIMARY KEY)''')
conn.commit()

# Сообщения для каждого дня недели
daily_messages = {
    0: "Расписание для понедельника\n1)АНГЛИЙСКИЙ ЯЗЫК\n2)АЛГЕБРА\n3)ХИМИЯ\n4)ХИМИЯ\n5)БИОЛОГИЯ\n6)БИОЛОГИЯ",
    1: "Расписание для вторника\n1)ЛИТЕРАТУРА\n2)ИНФОРМАТИКА\n3)РУССКИЙ ЯЗЫК\n4)УЗБЕКСКИЙ ЯЗЫК\n5)ФИЗИКА\n6)ВОСПИТАНИЕ",
    2: "Расписание для среды\n1)БИОЛОГИЯ\n2)БИОЛОГИЯ\n3)ГЕОМЕТРИЯ\n4)АНГЛИЙСКИЙ ЯЗЫК\n5)АЛГЕБРА\n6)БИОЛОГИЯ",
    3: "Расписание для четверга\n1)ЧГБТ\n2)УЗБЕКСКИЙ ЯЗЫК\n3)АНГЛИЙСКИЙ ЯЗЫК\n4)ФИЗРА\n5)ХИМИЯ\n6)ХИМИЯ",
    4: "Расписание для пятницы\nПОЛНОСТЬЮ АНГЛИЙСКИЙ ЯЗЫК",
    5: "Расписание для субботы\nПОЛНОСТЬ ХИМИЯ"
}

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    await message.reply("Привет! Теперь вы подписаны на ежедневные уведомления.")

async def send_daily_message():
    now = datetime.now(pytz.timezone('Asia/Tashkent'))
    weekday = now.weekday()
    if weekday in daily_messages:
        message = daily_messages[weekday]
        cursor.execute("SELECT user_id FROM users")
        user_ids = cursor.fetchall()
        for user_id in user_ids:
            try:
                await bot.send_message(user_id[0], message)
            except Exception as e:
                print(f"Не удалось отправить сообщение пользователю {user_id[0]}: {e}")

async def scheduler():
    aioschedule.every().day.at("06:00").do(send_daily_message)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def main():
    asyncio.create_task(scheduler())
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
