from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (ContextTypes, CommandHandler, ConversationHandler, MessageHandler, filters)

from bot.Database import database as db
from bot import ai_helper

SELECTING, ADD_TASK, REMOVE_TASK, CALL_AI = range(4)  # Объявление состояний для нашего telegram-бота

"""Клавиатура, с помощью которой пользователь будет взаимодействовать с нашим ботом"""
keyboard = [
    [("Добавь задачи к списке"),
     ("Удалить из списка")],
    [("Зови помощника")]
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """

    :param update: Получение обновлений со стороны telegram
    :param context:Контекст относительно того, кто отправляет текст, человек,бот и т.д.
    :return: Возвращает состояние "выбор", которое используется в функции обработчика диалога
    """
    text = ("""
Добро пожаловать в бот для составления списка дел!! 
Этот бот также поможет тебе управлять твоими задачами! 
Пиши /help чтобы узнать больше!  
    """)

    markUP = ReplyKeyboardMarkup(keyboard)
    await update.message.reply_text(text=text, reply_markup=markUP)
    return SELECTING


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """

    :param update:Получение обновлений со стороны telegram
    :param context:Контекст относительно того, кто отправляет текст, человек,бот и т.д.
    :return: Возвращает текст со всеми командами справки
    """
    await context.bot.send_message(chat_id=update.effective_chat.id, text="""
    Используйте следующие команды чтобы работать с ботом

1. /start   чтобы снова запустить бот
2. /help    Чтобы получить помочь
3. /gen   Чтобы узнать как работает бот
4. /delete_all Чтобы убрать все задачи из списка
""")


async def gen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """

    :param update: Получение обновлений со стороны telegram
    :param context: Контекст относительно того, кто отправляет текст, человек,бот и т.д.
    :return: Возвращает текст со всеми командами справки
    """
    await context.bot.send_message(chat_id=update.effective_chat.id, text="""
когда вы войдете в режим  (добавления/Удаление) задачи, все, что вы введете, будет (Добавлено/Удалено) (в базу данных/От базы Данных),для выхода из режима введите End
Пока бот не получит команду end, он будет оставаться в заданном режиме

    1. Добавь задачи к списке: Чтобы войди в режиме добавление задачи
    2. Удалить из списка: Чтобы войди в режиме удаление задачи из списка
    3. Зови помощника:  Чтобы звать своего помощника (По-умолчанию его зовут Аади)
    4. Покажи задачи:  Чтобы увидеть все свои задачи
    """)


async def task_selector(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """

    :param update: Получение обновлений со стороны telegram
    :param context:Контекст относительно того, кто отправляет текст, человек,бот и т.д.
    :return: Возвращает состояние "выбор", которое используется в функции обработчика диалога
    """
    text = update.message.text.lower()


    if text == "добавь задачи к списке":
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Отправь задачи которые хочешь добавь к списке, отправь end чтобы отменить")
        return ADD_TASK
    elif text == "удалить из списка":
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Отправь задачи которые хочешь удалить из списка, отправь end чтобы "
                                            "отменить")
        return REMOVE_TASK
    elif text == "зови помощника":
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Зову вашего помощника, подождите, пока он ответит на ваши вопросы! "
                                            "отправь end чтобы отменить")
        return CALL_AI

    return SELECTING


async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """

    :param update: Получение обновлений со стороны telegram
    :param context:Контекст относительно того, кто отправляет текст, человек,бот и т.д.

    в конце отправляет сообщение и добавляет данная задача в базу данных
    """
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Задача добавлено, если еще есть отправь, или отправь 'end'")
    db.add_data_to_database(update, context)


async def delete_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """

    :param update: Получение обновлений со стороны telegram
    :param context:Контекст относительно того, кто отправляет текст, человек,бот и т.д.

    Убирает все задачи из базы данных для данного ползователя
    """
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Убираем все задачи из списка")
    await db.delete_all_tasks(update, context)


async def remove_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """

    :param update: Получение обновлений со стороны telegram
    :param context:Контекст относительно того, кто отправляет текст, человек,бот и т.д.

    Убирает данную задачу из базы данных
    """
    await db.delete_task(update, context)
    return SELECTING


async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """

    :param update: Получение обновлений со стороны telegram
    :param context:Контекст относительно того, кто отправляет текст, человек,бот и т.д.

    Функция, которая вызывает помощник по искусственному интеллекту
    """
    await ai_helper.ai_help(update, context)


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """

    :param update: Получение обновлений со стороны telegram
    :param context:Контекст относительно того, кто отправляет текст, человек,бот и т.д.
    :return: Сообщает обработчику диалога, что пользователь хочет завершить работу с ботом, и закрывает соединение с базой данных
    """
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Пока пока!")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Был рад вам помочь!")
    await db.show_all_the_task(update, context)
    db.close_the_connection(context, update)
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        SELECTING: [
            MessageHandler(filters.Regex(
                "^(Добавь задачи к списке|добавь задачи к списке|Удалить из списка|удалить из списка|Зови помощника|зови помощника)$"),
                task_selector),
        ],
        ADD_TASK: [
            MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^End|end$")), add_task),

        ],
        REMOVE_TASK: [
            MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^End|end$")), remove_task),
        ],
        CALL_AI: [
            MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^End|end$")), ask_ai),
        ],

    },
    fallbacks=[MessageHandler(filters.Regex("^End|end$"), end)],
    name='my_conv',
    persistent=True,
)

help_handler = CommandHandler('help', help)
gen_handler = CommandHandler('gen', gen)
delete_all_handler = CommandHandler('delete_all', delete_all)
