# in the name of GOD

import json

# {"is_hamkar": self.is_hamkar, "percent": self.percent, "credit": self.credit, "accepted_rules": 1, "is_blocked": self.blocked, "username": self.user_name, "inviter": self.inviter, "number_of_invited": self.subset_number}

class newUser:
    def __init__(self, user_id = 0, is_hamkar = 0, percent = 100, credit = 0, accepted_rules = 1, is_blocked = 0, user_name = "none", inviter = 0, number_of_invited = 0):
        try:
            with open('data/users.json', 'r') as f:
                data = json.load(f)
                temp = data[str(user_id)]['percent']
            return 0
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

        with open('data/users.json', 'w+') as f:
            data = json.load(f)
            data[str(self.user_id)] = {"is_hamkar": self.is_hamkar, "percent": self.percent, "credit": self.credit, "accepted_rules": 1, "is_blocked": self.blocked, "username": self.user_name, "inviter": self.inviter, "number_of_invited": self.subset_number}
            json.dump(data, f)
        return 1


class userInfo:
    def __init__(self, user_id):
        try:
            with open('data/users.json', 'r') as f:
                data = json.load(f)
                return data[str(user_id)]
        except:
            return 0

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