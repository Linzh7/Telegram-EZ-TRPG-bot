import re
from database import user_db

EXIST_REGEX = r'^\d* ?\d*[dD]\d+'

def process_dice_command(dice_command):
    return dice_command.replace(';', '\n').replace('.', ' ').replace(',', ' ')

async def set_spell(update, context):
    username = update.message.chat.username if update.message.chat.username else update.message.chat.first_name
    user_id = update.message.chat.id
    if len(context.args)==2:
        dice_command = process_dice_command(context.args[1])
        if re.match(EXIST_REGEX, dice_command):
            previous_value = user_db.set_user_command(user_id, context.args[0], dice_command)
            await update.message.reply_text(f'@{username}, your spell <b>{context.args[0]}</b> has been set to <code>{dice_command}</code> from <code>{previous_value}</code>.', parse_mode='HTML')
        else:
            await update.message.reply_text(f'Invalid spell command! Please add a valid dice command.', parse_mode='HTML')
    else:
        await update.message.reply_text(f'Use /setspell &lt;spell trigger&gt; &lt;spell command&gt; to set your spell. \r\nMulti-spell could be set by add a semicolon between commands. No space in your dice command(s). \r\nIf space are needed, e.g., "2 2d4+2", please replace the space here with period or comma, i.e., "1.2d4+5,attact;2,d6*2,def" are allowed.', parse_mode='HTML')

# async def cast_spell(update, context):
#     username = update.message.from_user.username if update.message.from_user.username else update.message.from_user.first_name
#     if len(context.args)==1:
#         spell_command = user_db.get_user(username).get(context.args[0])
#         if spell_command:
#             await update.message.reply_text(f'@{username}, your spell <b>{context.args[0]}</b> is <code>{spell_command}</code>.', parse_mode='HTML')
#         else:
#             await update.message.reply_text(f'@{username}, your spell <b>{context.args[0]}</b> is not set.', parse_mode='HTML')
#     else:
#         raise Exception(f'Use /cast <spell trigger> to cast your spell.')