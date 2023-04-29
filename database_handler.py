# in the name of GOD

import json

# {"is_hamkar": self.is_hamkar, "percent": self.percent, "credit": self.credit, "accepted_rules": 1, "is_blocked": self.blocked, "username": self.user_name, "inviter": self.inviter, "number_of_invited": self.subset_number}

def newUser(user_id = 0, is_hamkar = 0, percent = 100, credit = 0, accepted_rules = 1, is_blocked = 0, user_name = "none", inviter = 0, number_of_invited = 0):
    try:
        with open('data/users.json', 'r') as f:
            data = json.load(f)
            temp = data[str(user_id)]['percent']
        return 0
    except:
        pass
    
    with open('data/users.json', 'r') as f:
        data = json.load(f)
    data[str(user_id)] = {"is_hamkar": is_hamkar, "percent": percent, "credit": credit, "accepted_rules": 1, "is_blocked": is_blocked, "username": user_name, "inviter": inviter, "number_of_invited": number_of_invited}
    with open('data/users.json', 'w') as f:
        json.dump(data, f)
    return 1

    
def newPayment(user_id, payment_id, price, status = "waiting"):
    try:
        with open('data/payments.json', 'r') as f:
            temp = json.loads(f)[str(user_id)]
    except:
        with open('data/patments.json', 'r') as f:
            temp = json.loads(f)
        temp[str(user_id)] = {}
    
    try:
        with open('data/payments.json', 'r') as f:
            temp = json.loads(f)
        temp = temp[str(user_id)][str(payment_id)]
        return 0
    except:
        pass

    with open('data/payments.json', 'r') as f:
        data = json.load(f)
    data[str(user_id)][str(payment_id)] = {"status": status, "price": price}
    with open('data/payments.json', 'w') as f:
        json.dump(data, f)

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