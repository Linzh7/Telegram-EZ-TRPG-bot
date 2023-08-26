from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler
from log import logger

import TOKEN
import error_handler
import storage
import dice
import database

EXIST_REGEX = r'^\d* ?\d*[dD]\d+'

user_db = database.user_db

def main():
    app = ApplicationBuilder().token(TOKEN.TG_TOKEN).build()

    app.add_handler(MessageHandler(filters.Regex(EXIST_REGEX), dice.call_roll))
    app.add_handler(CommandHandler(['setspell','set'], storage.set_spell))
    app.add_handler(CommandHandler(['castspell','cast'], dice.cast_spell))

    app.add_error_handler(error_handler.update_error_handler)

    logger.info(f'[System] Bot started!')
    app.run_polling()
    user_db.close_database()

if __name__ == '__main__':
    main()

user_db.close_database()
print('[System] Database closed.')