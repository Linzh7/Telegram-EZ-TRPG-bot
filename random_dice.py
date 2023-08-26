import random

def roll_dice(dice_num, dice_sides):
    return [random.randint(1, dice_sides) for _ in range(dice_num)]