import shelve

USER_DB_PATH = 'user'

# with shelve.open(USER_DB_PATH, writeback=True) as user_db:
class UserDB:
    def __init__(self):
        self.user_db = shelve.open(USER_DB_PATH, writeback=True)

    def close_database(self):
        self.user_db.close()

    def sync_user_db(self):
        self.user_db.sync()

    def set_user_dict(self, user_id, key, value):
        if str(user_id) not in self.user_db.keys():
            self.user_db[str(user_id)] = {}
        previous_value = self.user_db[str(user_id)].get(key)
        if previous_value != value:
            self.user_db[str(user_id)][key] = value
            self.sync_user_db()
            return previous_value

    def set_user_command(self, user_id, trigger, command):
        self.set_user_dict(user_id, trigger, command)
        self.sync_user_db()

    def get_user_command(self, user_id, trigger):
        if str(user_id) not in self.user_db.keys():
            return None
        return self.user_db[str(user_id)][trigger]
    
user_db = UserDB()