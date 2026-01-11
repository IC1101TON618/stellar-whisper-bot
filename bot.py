import os
from aiogram import Bot, Dispatcher, executor, types
import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import random
import hashlib
from datetime import date
user_data = {}
daily_limits = {}
main_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=False
)

main_menu.add(
    KeyboardButton("🔮 Послание дня"),
    KeyboardButton("❤️ Любовь"),
    KeyboardButton("💰 Деньги"),
)

main_menu.add(
    KeyboardButton("ℹ️ О канале")
)
HOROSCOPE_TEXTS = {
    "day": {
        "intro": [
            "Сегодня Вселенная мягко направляет тебя.",
            "Энергия дня складывается необычным образом.",
            "Этот день несёт скрытый смысл.",
            "Пространство сегодня реагирует на твои мысли.",
            "Сегодня многое будет зависеть от внутреннего настроя.",
            "День раскрывается постепенно, не спеши."
        ],
        "mood": [
            "Ты можешь чувствовать лёгкое напряжение.",
            "Настроение будет меняться волнами.",
            "Внутренний голос станет особенно заметным.",
            "Появится желание побыть в тишине.",
            "Эмоции будут тонко переплетаться.",
            "Внимание сместится на личные ощущения."
        ],
        "core": [
            "События сложатся не совсем так, как ожидалось.",
            "Небольшая деталь повлияет на ход дня.",
            "Важно доверять первому импульсу.",
            "Кто-то из окружения проявит себя иначе.",
            "Ты увидишь ситуацию под новым углом.",
            "Мелочи сегодня имеют значение."
        ],
        "detail": [
            "Это подходящий момент для осознанных решений.",
            "Лучше избегать резких слов и выводов.",
            "Не стоит торопить события.",
            "Полезно будет сделать паузу.",
            "Спокойствие станет твоим преимуществом.",
            "Интуиция подскажет верное направление."
        ],
        "advice": [
            "Сфокусируйся на том, что действительно важно.",
            "Не распыляй энергию понапрасну.",
            "Береги свои ресурсы.",
            "Прислушайся к ощущениям тела.",
            "Дай себе право на ошибку.",
            "Выбери мягкий путь."
        ],
        "final": [
            "К вечеру придёт ясность.",
            "Итог дня тебя удивит.",
            "Ты почувствуешь внутреннее облегчение.",
            "Этот день даст пищу для размышлений.",
            "Ответ станет очевидным позже.",
            "День оставит важный след."
        ]
    },

    "love": {
        "intro": [
            "Любовная энергия сегодня особенно тонкая.",
            "Сердце чувствует больше, чем разум.",
            "В отношениях намечаются изменения.",
            "Сегодня важно быть искренней.",
            "Эмоции могут выйти на поверхность."
        ],
        "mood": [
            "Может появиться чувство ожидания.",
            "Ты будешь особенно чувствительна.",
            "Настроение зависит от мелочей.",
            "Хочется тепла и внимания.",
            "Эмоциональный фон нестабилен."
        ],
        "core": [
            "Разговор многое прояснит.",
            "Прошлое может напомнить о себе.",
            "Кто-то сделает неожиданный шаг.",
            "Важно не додумывать лишнего.",
            "Ситуация требует честности."
        ],
        "detail": [
            "Лучше не давить на партнёра.",
            "Не бойся показать уязвимость.",
            "Мягкость сегодня сильнее напора.",
            "Слова имеют особый вес.",
            "Молчание тоже может быть ответом."
        ],
        "advice": [
            "Слушай не только слова.",
            "Доверься ощущениям.",
            "Не торопи события.",
            "Позволь чувствам быть.",
            "Будь бережна к себе."
        ],
        "final": [
            "К вечеру станет спокойнее.",
            "Ответ придёт сам.",
            "Сердце подскажет верно.",
            "Ты почувствуешь облегчение.",
            "Всё встанет на свои места."
        ]
    },

    "money": {
        "intro": [
            "Финансовая энергия дня нестабильна.",
            "Деньги сегодня требуют внимания.",
            "Материальные вопросы выходят на первый план.",
            "Сегодня важна расчётливость.",
            "Стоит пересмотреть приоритеты."
        ],
        "mood": [
            "Возможны сомнения.",
            "Хочется больше уверенности.",
            "Настроение зависит от цифр.",
            "Может появиться беспокойство.",
            "Фокус смещается на практичность."
        ],
        "core": [
            "Неожиданный расход возможен.",
            "Появится шанс улучшить положение.",
            "Мелкое решение повлияет на бюджет.",
            "Важно не рисковать.",
            "Стоит проявить осторожность."
        ],
        "detail": [
            "Лучше отложить крупные траты.",
            "Проверь документы и счета.",
            "Не поддавайся импульсу.",
            "Экономия сегодня оправдана.",
            "Планирование даст результат."
        ],
        "advice": [
            "Действуй обдуманно.",
            "Не спеши с выводами.",
            "Береги ресурсы.",
            "Сохраняй баланс.",
            "Деньги любят порядок."
        ],
        "final": [
            "Ситуация стабилизируется.",
            "К вечеру станет яснее.",
            "Финансовый фон выровняется.",
            "Ты почувствуешь контроль.",
            "Решение окажется верным."
        ]
    }
}
def generate_horoscope(user_id: int, zodiac: str, h_type: str):
    today = str(date.today())
    seed_str = f"{user_id}_{zodiac}_{h_type}_{today}"
    seed = int(hashlib.md5(seed_str.encode()).hexdigest(), 16)
    random.seed(seed)

    blocks = HOROSCOPE_TEXTS[h_type]

    return " ".join([
        random.choice(blocks["intro"]),
        random.choice(blocks["mood"]),
        random.choice(blocks["core"]),
        random.choice(blocks["detail"]),
        random.choice(blocks["advice"]),
        random.choice(blocks["final"]),
    ])
from datetime import date

def can_get_horoscope(user_id: int, h_type: str):
    today = str(date.today())

    if user_id not in daily_limits:
        daily_limits[user_id] = {}

    if daily_limits[user_id].get(h_type) == today:
        return False

    daily_limits[user_id][h_type] = today
    return True


BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    text = (
        "✨ Добро пожаловать в *Шёпот Звёзд* ✨\n\n"
        "Здесь нет случайных слов.\n"
        "Каждое послание формируется под твой знак и энергию дня.\n\n"
        "Ты сможешь получать:\n"
        "🔮 Напутствие на день\n"
        "💖 Подсказки для любви\n"
        "💰 Энергию денег и решений\n\n"
        "Перед началом мне нужно немного почувствовать тебя 🌙"
    )

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text="✨ Начать",
            callback_data="start_form"
        )
    )

    await message.answer(
        text,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
@dp.callback_query_handler(lambda c: c.data == "start_form")
async def start_form(call: types.CallbackQuery):
    await call.answer()

    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("👩 Женщина", callback_data="gender_female"),
        InlineKeyboardButton("👨 Мужчина", callback_data="gender_male")
    )

    await call.message.answer(
        "Кто ты по энергии? 🌗",
        reply_markup=keyboard
    )
@dp.callback_query_handler(lambda c: c.data.startswith("gender_"))
async def process_gender(call: types.CallbackQuery):
    user_id = call.from_user.id
    gender = call.data.split("_")[1]

    user_data[user_id] = {}
    user_data[user_id]["gender"] = gender

    await call.message.edit_text(
        "✨ Отлично.\n\nКак тебя называть?"
    )
    await call.answer()
@dp.message_handler(lambda message: message.from_user.id in user_data and "name" not in user_data[message.from_user.id])
async def get_name(message: types.Message):
    user_id = message.from_user.id
    name = message.text.strip()

    user_data[user_id]["name"] = name

    keyboard = InlineKeyboardMarkup(row_width=3)

    age_buttons = [
        InlineKeyboardButton("16–20", callback_data="age_16_20"),
        InlineKeyboardButton("21–25", callback_data="age_21_25"),
        InlineKeyboardButton("26–30", callback_data="age_26_30"),
        InlineKeyboardButton("31–35", callback_data="age_31_35"),
        InlineKeyboardButton("36–40", callback_data="age_36_40"),
        InlineKeyboardButton("41+", callback_data="age_41_plus"),
    ]

    keyboard.add(*age_buttons)

    await message.answer(
        f"Приятно познакомиться, {name} ✨\n\nВыбери свой возраст:",
        reply_markup=keyboard
    )
@dp.callback_query_handler(lambda c: c.data.startswith("age_"))
async def process_age(call: types.CallbackQuery):
    user_id = call.from_user.id
    age = call.data.replace("age_", "")

    user_data[user_id]["age"] = age

    keyboard = InlineKeyboardMarkup(row_width=3)

    zodiac_buttons = [
        InlineKeyboardButton("♈ Овен", callback_data="zodiac_oven"),
        InlineKeyboardButton("♉ Телец", callback_data="zodiac_telec"),
        InlineKeyboardButton("♊ Близнецы", callback_data="zodiac_bliznecy"),
        InlineKeyboardButton("♋ Рак", callback_data="zodiac_rak"),
        InlineKeyboardButton("♌ Лев", callback_data="zodiac_lev"),
        InlineKeyboardButton("♍ Дева", callback_data="zodiac_deva"),
        InlineKeyboardButton("♎ Весы", callback_data="zodiac_vesy"),
        InlineKeyboardButton("♏ Скорпион", callback_data="zodiac_scorpion"),
        InlineKeyboardButton("♐ Стрелец", callback_data="zodiac_strelec"),
        InlineKeyboardButton("♑ Козерог", callback_data="zodiac_kozerog"),
        InlineKeyboardButton("♒ Водолей", callback_data="zodiac_vodoley"),
        InlineKeyboardButton("♓ Рыбы", callback_data="zodiac_ryby"),

    ]

    keyboard.add(*zodiac_buttons)

    await call.message.edit_text(
        "✨ Отлично.\n\nВыбери свой знак зодиака:",
        reply_markup=keyboard
    )
    await call.answer()
@dp.callback_query_handler(lambda c: c.data.startswith("zodiac_"))
async def process_zodiac(call: types.CallbackQuery):
    user_id = call.from_user.id
    zodiac = call.data.replace("zodiac_", "")

    user_data[user_id]["zodiac"] = zodiac

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("🌙 Получить послание", callback_data="open_horoscope")
    )

    await call.message.edit_text(
        "🌙 Анкета завершена.\n\nТеперь ты можешь получать персональные послания.",
        reply_markup=keyboard
    )
    await call.answer()
@dp.callback_query_handler(lambda c: c.data == "open_horoscope")
async def open_horoscope(call: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("🔮 Напутствие на день", callback_data="horo_day"),
        InlineKeyboardButton("❤️ Любовь", callback_data="horo_love"),
        InlineKeyboardButton("💰 Деньги", callback_data="horo_money"),
    )

    await call.message.edit_text(
        "✨ Выбери, какое послание ты хочешь получить сегодня:",
        reply_markup=keyboard
    )
    await call.answer()
@dp.callback_query_handler(lambda c: c.data == "horo_day")
async def horo_day(call: types.CallbackQuery):
    user_id = call.from_user.id
    zodiac = user_data[user_id]["zodiac"]

    text = generate_horoscope(user_id, zodiac, "day")

    await call.message.answer(
    f"🌙 *Послание дня*\n\n{text}",
    parse_mode="Markdown",
    reply_markup=main_menu
)

    await call.answer()
@dp.message_handler(lambda message: message.text == "🔮 Послание дня")
async def menu_day(message: types.Message):
    user_id = message.from_user.id

    if not can_get_horoscope(user_id, "day"):
        await message.answer(
            "🌙 Ты уже получила послание на сегодня.\nПопробуй снова завтра ✨",
            reply_markup=main_menu
        )
        return

    zodiac = user_data[user_id]["zodiac"]
    text = generate_horoscope(user_id, zodiac, "day")

    await message.answer(
        f"🌙 *Послание дня*\n\n{text}",
        parse_mode="Markdown",
        reply_markup=main_menu
    )
@dp.message_handler(lambda message: message.text == "❤️ Любовь")
async def menu_love(message: types.Message):
    user_id = message.from_user.id

    if not can_get_horoscope(user_id, "love"):
        await message.answer(
            "❤️ Любовное послание на сегодня уже было.\nЗавтра будет новое ✨",
            reply_markup=main_menu
        )
        return

    zodiac = user_data[user_id]["zodiac"]
    text = generate_horoscope(user_id, zodiac, "love")

    await message.answer(
        f"❤️ *Любовное послание*\n\n{text}",
        parse_mode="Markdown",
        reply_markup=main_menu
    )
@dp.message_handler(lambda message: message.text == "💰 Деньги")
async def menu_money(message: types.Message):
    user_id = message.from_user.id

    if not can_get_horoscope(user_id, "money"):
        await message.answer(
            "💰 Финансовое послание на сегодня уже получено.\nНовый прогноз — завтра ✨",
            reply_markup=main_menu
        )
        return

    zodiac = user_data[user_id]["zodiac"]
    text = generate_horoscope(user_id, zodiac, "money")

    await message.answer(
        f"💰 *Финансовое послание*\n\n{text}",
        parse_mode="Markdown",
        reply_markup=main_menu
    )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
