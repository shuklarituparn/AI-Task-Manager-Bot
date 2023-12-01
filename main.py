import logging
from bot import initialize_the_bot as init, handlers
from telegram import Update


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)



if __name__ == '__main__':

    app = init()
    app.add_handler(handlers.conv_handler)
    app.add_handler(handlers.gen_handler)
    app.add_handler(handlers.help_handler)
    app.add_handler(handlers.delete_all_handler)
    app.run_polling(allowed_updates=Update.ALL_TYPES)