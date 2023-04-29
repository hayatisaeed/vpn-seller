# in the name of GOD

import json

# if mode = edit, you can send special variable to edit # must return a dictionary
def user_info(user_id, is_hamkar = 0, percent = 100, credit = 0, accepted_rules = 1, is_blocked = 0, user_name = "none", inviter = 0, number_of_invited = 0, mode = "write", var = "none"):
    if mode == "edit":
        pass
    else:
        pass

class userInfo:
    def __init__(self, user_id):
        with open('data/users.json', 'r') as f:
            try:
                data = json.load(f)[user_id]
            except:
                return 'NoSuchUser'
            self.user_id = user_id
            self.user_name = data['username']
            self.is_hamkar = data['is_hamkar']
            self.percent = data['percent']
            self.credit = data['credit']
            self.blocked = data['is_blocked']
            self.inviter = data['inviter']
            self.subset_number = data['number_of_invited']
    def edit_user(self, user_id, key, value):
        with open('data/users.json', 'w') as f:
            data = json.load(f)
            try:
                temp = data[user_id]
                try:
                    temp = data[user_id][key]
                    data[user_id][key] = value
                    json.dump(data, f)
                    return True
                except:
                    return 'NoSuchKey'
            except:
                return 'NoSuchUser'
    def new_user(self, user_id, is_hamkar = 0, percent = 100, credit = 0, accepted_rules = 1, is_blocked = 0, user_name = "none", inviter = 0, number_of_invited = 0):
        with open('data/users.json', 'r') as f:
            data = json.load(f)
            try:
                temp = data[user_id]['percent']
                return 'UserExists'
            except:
                pass
            self.user_id = user_id
            self.user_name = user_name
            self.is_hamkar = is_hamkar
            self.percent = percent
            self.credit = credit
            self.blocked = is_blocked
            self.inviter = inviter
            self.subset_number = number_of_invited
            data[user_id] = {"is_hamkar": self.is_hamkar, "percent": self.percent, "credit": self.credit, "accepted_rules": 1, "is_blocked": self.blocked, "username": self.user_name, "inviter": self.inviter, "number_of_invited": self.subset_number}
            json.dump(data, f)
            return True

def payment(uid, pid, price, status = "waiting"):
    with open('data/payments.json', 'w') as f:
        pass

def configs():
    pass

def messages():
    pass

def bot():
    pass

def servers():
    pass

def user_configs():
    pass

def user_info():
    pass

def users():
    pass