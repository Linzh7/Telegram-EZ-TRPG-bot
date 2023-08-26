import re
from database import user_db
from message_processer import *

EXIST_REGEX = r'^\d* ?\d*[dD]\d+'

def process_dice_command(dice_command):
    return dice_command.replace(';', '\n').replace('.', ' ').replace(',', ' ')

def format_dice_command(dice_command):
    return dice_command.replace('\n', '; ')

async def set_spell(update, context):
    username, user_id = get_username_id(update.message)

    if len(context.args)==2:
        dice_command = process_dice_command(context.args[1])
        if re.match(EXIST_REGEX, dice_command):
            previous_value = user_db.set_user_command(user_id, context.args[0], dice_command)
            await update.message.reply_text(f'@{username}, your spell <b>{context.args[0]}</b> has been set to <code>{format_dice_command(dice_command)}</code> from <code>{previous_value}</code>.', parse_mode='HTML')
        else:
            await update.message.reply_text(f'Invalid spell command! Please add a valid dice command.', parse_mode='HTML')
    else:
        await update.message.reply_text(f'Use /setspell &lt;spell trigger&gt; &lt;spell command&gt; to set your spell. \r\nMulti-spell could be set by add a semicolon between commands. No space in your dice command(s). \r\nIf space are needed, e.g., "2 2d4+2", please replace the space here with period or comma, i.e., "1.2d4+5,attact;2,d6*2,def" are allowed.', parse_mode='HTML')

async def get_spell_list(update, context):
    username, user_id = get_username_id(update.message)
    spell_list = user_db.get_user_dict(user_id)
    response = f'@{username}, your spell list:\r\n'
    for spell_name, spell_command in spell_list.items():
        response += f'<b>{spell_name}</b>: <code>{format_dice_command(spell_command)}</code>\r\n'
    await update.message.reply_text(response, parse_mode='HTML')