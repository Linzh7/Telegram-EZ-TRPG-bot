import re
import random
from database import user_db

DICE_REGEX = r'^(\d+ )?(\d+)?[dD](\d+)(\S*) ?(\S*)?$'

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

async def call_roll(update, context):
    text = update.message.text
    username = update.message.from_user.username if update.message.from_user.username else update.message.from_user.first_name
    response = roll(username, text)
    await update.message.reply_text(response, parse_mode='HTML')

async def cast_spell(update, context):
    # username = update.message.from_user.username if update.message.from_user.username else update.message.from_user.first_name
    username = update.message.chat.username if update.message.chat.username else update.message.chat.first_name
    user_id = update.message.chat.id
    for spell_name in context.args:
        spell_command = user_db.get_user_command(user_id, spell_name)
        if spell_command:
            response = roll(username, spell_command)
            await update.message.reply_text(response, parse_mode='HTML')
        else:
            await update.message.reply_text(f'@{username}, your spell <b>{spell_name}</b> is not set.', parse_mode='HTML')

def roll(username, text):
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

    return response
