import asyncio
import logging
import os
import sys
import edge_tts

from aiogram import Bot, Dispatcher, F, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    BotCommand,
    FSInputFile,
)


from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")


dp = Dispatcher()


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Boshlash"),
        BotCommand(command="help", description="Yordam"),
        BotCommand(command="about", description="Bot haqida"),
    ]
    await bot.set_my_commands(commands)


async def ovoz(matn, filename, voice):
    max_len = 300
    chunks = [matn[i:i + max_len] for i in range(0, len(matn), max_len)]
    temp_files = []

    for i, chunk in enumerate(chunks):
        temp_name = f"chunk_{i}.mp3"
        tts = edge_tts.Communicate(chunk, voice)
        await tts.save(temp_name)
        temp_files.append(temp_name)

    with open(filename, "wb") as out:
        for f in temp_files:
            with open(f, "rb") as inp:
                out.write(inp.read())
            os.remove(f)


menu = [
    "👨‍🦰 Sardor 🇺🇿", "👩 Madina 🇺🇿",
    "👨‍🦱 Ahmet 🇹🇷", "👩 Emel 🇹🇷",
    "👨‍🦰 Dmitry 🇷🇺", "👩 Svetlana 🇷🇺",
    "👨‍🦰 Neural 🇺🇸", "👩 Jenny 🇺🇸",
    "👨 Ryan 🇺🇸", "👩 Sonia 🇺🇸",
    "👩 Emma 🇬🇧", "👨 Brian 🇬🇧",
    "👨‍🦱 Hamed 🇸🇦", "👩‍🦱 Zariyah 🇸🇦",
]

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=menu[0]), KeyboardButton(text=menu[1])],
        [KeyboardButton(text=menu[2]), KeyboardButton(text=menu[3])],
        [KeyboardButton(text=menu[4]), KeyboardButton(text=menu[5]),
        [KeyboardButton(text=menu[6]), KeyboardButton(text=menu[7])],
        [KeyboardButton(text=menu[8]), KeyboardButton(text=menu[9])],
        [KeyboardButton(text=menu[10]), KeyboardButton(text=menu[11])],
        [KeyboardButton(text=menu[12]), KeyboardButton(text=menu[13])],
    ],
    resize_keyboard=True,
)

voices = {
    menu[0]: "uz-UZ-SardorNeural",
    menu[1]: "uz-UZ-MadinaNeural",
    menu[2]: "tr-TR-AhmetNeural",
    menu[3]: "tr-TR-EmelNeural",
    menu[4]: "ru-RU-DmitryNeural",
    menu[5]: "ru-RU-SvetlanaNeural",
    menu[6]: "en-US-GuyNeural",
    menu[7]: "en-US-JennyNeural",
    menu[8]: "en-US-RyanNeural",
    menu[9]: "en-US-SoniaNeural",
    menu[10]: "en-GB-EmmaNeural",
    menu[11]: "en-GB-BrianNeural",
    menu[12]: "ar-SA-HamedNeural",
    menu[13]: "ar-SA-ZariyahNeural",
}

users = {}


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        f"Assalomu alaykum, {html.bold(message.from_user.full_name)}!\n\n"
        "🔊 Ovoz tanlang:",
        reply_markup=keyboard,
    )

@dp.message(Command("help"))
async def help_cmd(message: Message):

    await message.answer("📲 Mening Telegramim: @davronbek_17_09")

@dp.message(Command("about"))
async def about_cmd(message: Message):
    await message.answer(
        "🤖 Bu ovozli bot!\n"
        "🛠 edge-tts texnologiyasi asosida ishlaydi.\n"
        "📖 Matn yuboring — bot uni ovozga aylantirib beradi."
    )

@dp.message(F.text.in_(menu))
async def choose_voice(message: Message):
    users[message.from_user.id] = voices[message.text]
    await message.answer("✅ Ovoz tanlandi. Endi matn yuboring.")

@dp.message(F.text)
async def text_handler(message: Message):
    if message.from_user.id not in users:
        await message.answer("⚠️ Avval /start bosib ovoz tanlang.")
        return

    voice = users[message.from_user.id]
    filename = f"voice_{message.chat.id}_{message.message_id}.mp3"

    try:
        await ovoz(message.text, filename, voice)
        await message.answer_voice(FSInputFile(filename), caption="🔊 Tayyor!")
    except Exception as e:
        logging.error(e)
        await message.answer("❌ Xatolik yuz berdi.")
    finally:
        if os.path.exists(filename):
            os.remove(filename)


async def main():
    logging.info("Bot ishga tushdi")
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await set_commands(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())



