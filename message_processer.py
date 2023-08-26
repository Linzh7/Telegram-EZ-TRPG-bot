
def get_username_id(messages):
    if str(messages.chat.type) == 'private':
        return messages.chat.username if messages.chat.username else messages.chat.first_name, messages.chat.id
    else:
        return messages.from_user.username if messages.from_user.username else messages.from_user.first_name, messages.from_user.id