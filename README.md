# Telegram-EZ-TRPG-bot

- no command or mark needed.
- support multi-action in one message.
- support store user-define commands (spells) and cast them.

Therefore, please set this bot as admin.


## message formats

### One action
```
[times] [amount of dice]d<dice sides>[equation] [extra text]
```

Do not add space in equation, i.e., `d4*2+1` is allowed and `d4 * 2 + 1` is not allowed.

**Examples:**
- `d8`
- `1d4`
- `2 d10`
- `6 2d100`
- `3 d12*2+4`
- `1 4d100*2+10 attact`

### multi-action
```
[times] [amount of dice]d<dice sides>[equation] [extra text]
[times] [amount of dice]d<dice sides>[equation] [extra text]
```

The only thing you need is start with a new line.

**Examples:**
input:
```
3 2d10*3+5 att
2 d4 def
```
output:
```
@User, you have 2 action(s):
att: 3 2d10*3+5 att
0-0# 6[4+2]*3+5 = 23
0-1# 9[5+4]*3+5 = 32
0-2# 11[9+2]*3+5 = 38
def: 2 d4 def
1-0# 3[3] = 3
1-1# 4[4] = 4
```

## command formats

### set spell

User should replace any space in the command part with either '.' or ',', because telegram will consider space as a args spliter. If you want to set multi-command, add ';' between them instead of Return (NewLind).

You can set your own spells by:

- `set`
- `setspell`

For example,
input:
```
/set morning 1.4d10*2+10.getup;2.4d6+4,fallasleep
```
output:
```
@xxx, your spell morning has been set to 1 4d10*2+10 getup
2 4d6+4 fallasleep from None.
```

### cast spell

- `cast`
- `castspell`

For example,
after setting the `morning` spell,
```
/cast morning
```
output:
```
@xxx, you have 2 action(s):
getup: 1 4d10*2+10 getup
0-0# 19[2+10+5+2]*2+10 = 48
fallasleep: 2 4d6+4 fallasleep
1-0# 21[6+4+5+6]+4 = 25
1-1# 16[4+2+5+5]+4 = 20
```


