import message_processer
import random_dice

class Combat:
    def __init__(self) -> None:
        self.players = []
        self.queue = []
        self.current_player_index = -1

    def sort_queue(self):
        self.queue = sorted(self. queue, key=lambda x: x[0], reverse=True)

    def join(self, initiative, character_name):
        if character_name in self.players:
            return False
        self.queue.append((initiative, character_name))
        self.players.append(character_name)
        self.sort_queue()
        return True

    def query_str(self):
        response = '\r\n'.join([f'[{i+1}] {character_name}: {initiative}' for i, (initiative, character_name) in enumerate(self.queue)])
        return response


current_combat = None

async def start_combat(update, context):
    global current_combat
    current_combat = Combat()
    await update.message.reply_text('[Combat] Combat started!')

async def join_combat(update, context):
    global current_combat
    if current_combat is None:
        await update.message.reply_text('[Combat] No combat started yet!')
    else:
        # dexterity modifier are required
        if len(context.args) == 1 or len(context.args) == 2:
            character_name = context.args[1] if len(context.args) == 2 else message_processer.get_username_id(update.message)[0]
            # early return if character_name is already in the combat
            if character_name in current_combat.players:
                await update.message.reply_text(f'@{character_name} has already joined the combat.')
                return
            
            dexterity_modifier = int(context.args[0])
            result = random_dice.roll_dice(1, 20)
            initiative = result[0] + dexterity_modifier
            current_combat.join(initiative, character_name)
            await update.message.reply_text(f'@{character_name} has joined the combat with <b>{initiative}</b> ({result}+{dexterity_modifier}).', parse_mode='HTML')
        else:
            await update.message.reply_text(f'Use <code>/joincombat</code> &lt;dexterity modifier&gt; [character name] to join the combat.', parse_mode='HTML')
        # current_combat.join(update, context)

async def query_combat(update, context):
    global current_combat
    if current_combat is None:
        await update.message.reply_text('[Combat] No combat started yet!')
    else:
        await update.message.reply_text(current_combat.query_str(), parse_mode='HTML')

async def end_combat(update, context):
    global current_combat
    if current_combat is None:
        await update.message.reply_text('[Combat] No combat started yet!')
    else:
        current_combat = None
        await update.message.reply_text('[Combat] Combat ended!')

async def next_turn(update, context):
    global current_combat
    if current_combat is None:
        await update.message.reply_text('[Combat] No combat started yet!')
    else:
        current_combat.current_player_index += 1
        current_combat.current_player_index %= len(current_combat.players)
        await update.message.reply_text(f'[Combat] Current turn: {current_combat.queue[current_combat.current_player_index][1]}')

async def previous_turn(update, context):
    global current_combat
    if current_combat is None:
        await update.message.reply_text('[Combat] No combat started yet!')
    else:
        current_combat.current_player_index -= 1
        current_combat.current_player_index %= len(current_combat.players)
        await update.message.reply_text(f'[Combat] Undo, current turn: {current_combat.queue[current_combat.current_player_index][1]}')