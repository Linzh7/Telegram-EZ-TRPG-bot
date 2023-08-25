import sys
import re
import html
import json
import random
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import logging
import traceback
from telegram import Update

TOKEN = ''

EXIST_REGEX = r'^\d* ?\d*[dD]\d+'
DICE_REGEX = r'^(\d+ )?(\d+)?[dD](\d+)(\S*) ?(\S*)?$'

formatter = logging.Formatter('====> %(asctime)s | %(name)s | %(levelname)s | %(message)s')
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)
file_handler = logging.FileHandler('roll.log')
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

logging.basicConfig(
        handlers = [stream_handler,file_handler],
        level=logging.DEBUG,
    )
logging.getLogger("httpx").setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)

def split_element(input_str):
    # 'd10+100 attact' -> ('', '', 'd10', '+100', 'attact')
    # '1d10*2+5 magic' -> ('', '1', '10', '*2+5', 'magic')
    # '4 20d10+100' ->  ('4 ', '20', '10', '+100', '')
    ele_list = re.findall(DICE_REGEX, input_str)
    return ele_list[0]

def roll_dice(dice_num, dice_sides):
    return [random.randint(1, dice_sides) for _ in range(dice_num)]

def compute_equation(value, equation):
    try:
        return eval(f'{value}{equation}')
    except Exception as e:
        raise Exception('Invalid equation!')

async def roll(update, context):
    text = update.message.text
    username = update.message.from_user.username if update.message.from_user.username else update.message.from_user.first_name
    multi_action_text = text.split('\n')
    try:
        response = f'@{username}, you have {len(multi_action_text)} action(s):\r\n'
        
        for action_index, dice_text in enumerate(multi_action_text):

            ele = split_element(dice_text)
            times = int(ele[0]) if ele[0] else 1
            dice_num = int(ele[1]) if ele[1] else 1
            dice_sides = int(ele[2]) if ele[2] else 4
            equation = ele[3] if ele[3] else ''
            action = ele[4] if ele[4] else f'Action {action_index+1}#'

            if len(multi_action_text) > 1:
                response += f'<b>{action}</b>: '
            response += f'<i>{dice_text}</i>\n'

            if dice_num > 1000:
                raise Exception('Too many dice! Please use less than 1000 dice.')
            for roll_index in range(times):
                dice_result = roll_dice(dice_num, dice_sides)
                sum_dice_result = sum(dice_result)
                final_result = compute_equation(sum_dice_result,equation)
                dice_result_text = '+'.join([str(i) for i in dice_result])

                response += f'{action_index}-{roll_index}# {sum_dice_result}[{dice_result_text}]{equation} = <b>{final_result}</b>\r\n'

    except Exception as e:
        response = f'@{username}: <b>Invalid equation!</b>\r\n'
        if dice_num and dice_num > 1000:
            response += str(e) + '.\r\n'
        response += ('For example: <code>d4</code>, or<code>3d6</code>, or <code>1d20+5</code>, or <code>d12</code>, or <code>5 2d100*2+10</code>, or <code>5 2d100*2+10[NewLine]1d20+5</code>\r\n\r\n')

    await update.message.reply_text(response, parse_mode='HTML')

async def bad_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Raise an error to trigger the error handler."""
    await context.bot.wrong_method_name()


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Exception while handling an update:", exc_info=context.error)
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )
    logger.error(message)
    # await context.bot.send_message(text=message, parse_mode='HTML')
    # await update.message.reply_text(text=message, parse_mode='HTML')


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.Regex(EXIST_REGEX), roll))
    app.add_error_handler(error_handler)

    app.run_polling()

if __name__ == '__main__':
    main()