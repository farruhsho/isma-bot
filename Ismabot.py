import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8103464151:AAFsX3M6wutGMPOlEbNsT0bI88ay_6uJh2M"
ADMIN_CHAT_ID = None  # Hozircha None, keyin chat_id ni qo‘shasiz

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📚 Ta'lim yo'nalishlari")],
        [KeyboardButton(text="☎ Call Center")],
        [KeyboardButton(text="🌍 Ijtimoiy tarmoqlar")],
        [KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    user_name = message.from_user.full_name
    await message.answer(
        f"👋 Assalomu alaykum, *{user_name}*! \nISMA Universiteti botiga xush kelibsiz! \nTanlang:",
        reply_markup=menu,
        parse_mode=ParseMode.MARKDOWN
    )

@dp.message(Command("myid"))
async def get_my_id(message: types.Message):
    chat_id = message.chat.id
    await message.answer(f"Sizning chat_id: `{chat_id}`", parse_mode=ParseMode.MARKDOWN)

@dp.message(lambda message: message.content_type == "contact")
async def get_contact(message: types.Message):
    phone_number = message.contact.phone_number
    user_name = message.from_user.full_name
    await message.answer(
        f"📞 Raxmat, *{user_name}*! Sizning telefon raqamingiz: `{phone_number}`",
        parse_mode=ParseMode.MARKDOWN
    )
    if ADMIN_CHAT_ID:
        try:
            await bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=f"Yangi foydalanuvchi telefoni:\nIsm: {user_name}\nRaqam: {phone_number}",
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            logging.error(f"Admin ga xabar yuborishda xatolik: {e}")
    else:
        logging.warning("ADMIN_CHAT_ID o‘rnatilmagan! /myid buyrug‘idan foydalanib chat_id ni oling.")

@dp.message(lambda message: message.text == "📚 Ta'lim yo'nalishlari")
async def education_programs(message: types.Message):
    text = "\n\n".join([
        "🔹 *IT* - Dasturlash va sun'iy intellekt",
        "🔹 *BA* - Biznes boshqaruvi",
        "🔹 *Turizm* - Mehmonxona va sayyohlik xizmatlari",
        "🔹 *Psixologiya* - Inson xulq-atvori va ruhiy salomatlik"
    ])
    await message.answer(
        f"📚 *Ta'lim yo'nalishlari:*\n{text}",
        parse_mode=ParseMode.MARKDOWN
    )

@dp.message(lambda message: message.text == "☎ Call Center")
async def call_center(message: types.Message):
    text = "\n".join([
        "📞 Telefon: +998 73 240 0114",
        "✉ Email: info-uz@isma.lv"
    ])
    await message.answer(
        f"☎ *Call Center ma'lumotlari:*\n{text}",
        parse_mode=ParseMode.MARKDOWN
    )

@dp.message(lambda message: message.text == "🌍 Ijtimoiy tarmoqlar")
async def social_links(message: types.Message):
    text = "\n".join([
        "🌐 [ISMA sayti](https://ismaeu.uz/)",
        "🔗 [Telegram](https://t.me/ISMA_Fergana_News)",
        "📷 [Instagram](https://www.instagram.com/ismauz/#)",
        "📘 [Facebook](https://www.facebook.com/share/18r7Bd9pbT/)"
    ])
    await message.answer(
        f"🌍 *Ijtimoiy tarmoqlar:*\n{text}",
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )

async def main():
    await bot.set_my_commands([
        types.BotCommand(command="start", description="Botni ishga tushirish"),  # "моихstart" o‘rniga "start"
        types.BotCommand(command="myid", description="Chat ID ni olish")
    ])
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())