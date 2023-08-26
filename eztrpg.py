from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler
from log import logger

from dotenv import dotenv_values

import error_handler
import storage
import dice
import combat
import database

EXIST_REGEX = r'^\d* ?\d*[dD]\d+'

config = dotenv_values(".env")

user_db = database.user_db

def main():
    app = ApplicationBuilder().token(config['TG_TOKEN']).build()

    app.add_handler(MessageHandler(filters.Regex(EXIST_REGEX), dice.call_roll))
    app.add_handler(CommandHandler(['setspell','set'], storage.set_spell))
    app.add_handler(CommandHandler(['castspell','cast'], dice.cast_spell))
    app.add_handler(CommandHandler(['spelllist','list'], storage.get_spell_list))

    app.add_handler(CommandHandler(['startcombat','start'], combat.start_combat))
    app.add_handler(CommandHandler(['querycombat','query'], combat.query_combat))
    app.add_handler(CommandHandler(['joincombat','join'], combat.join_combat))
    app.add_handler(CommandHandler(['endcombat','end'], combat.end_combat))
    app.add_handler(CommandHandler(['nextturn','next'], combat.next_turn))
    app.add_handler(CommandHandler(['previousturn','previous'], combat.previous_turn))

    app.add_error_handler(error_handler.update_error_handler)

    logger.info(f'[System] Bot started!')
    app.run_polling()
    user_db.close_database()

if __name__ == '__main__':
    main()

user_db.close_database()
print('[System] Database closed.')