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
    data['number_of_users'] += 1
    with open('data/users.json', 'w') as f:
        json.dump(data, f)
    return 1

def editUser(user_id, key, val):
    try:
        with open('data/users.json', 'r') as f:
            data = json.load(f)
        data[str(user_id)][key] = val
        with open('data/users.json', 'w') as f:
            json.dump(data, f)
        return True
    except:
        return False

def getUsers(user_type="All"): # available types: All, Hamkar, Normal
    with open('data/users.json', 'r') as f:
        data = json.load(f)
        return data
    

def userInfo(user_id):
    with open('data/users.json', 'r') as f:
        data = json.load(f)
        try:
            return data[str(user_id)]
        except:
            return 'NoSuchUser'


def newPayment(user_id, payment_id, price, status = "waiting"):
    try:
        with open('data/payments.json', 'r') as f:
            temp = json.load(f)[str(user_id)]
    except:
        with open('data/payments.json', 'r') as f:
            temp = json.load(f)
        temp[str(user_id)] = {}
        with open('data/payments.json', 'w') as f:
            json.dump(temp, f)
    
    try:
        with open('data/payments.json', 'r') as f:
            temp = json.load(f)
        temp = temp[str(user_id)][str(payment_id)]
        return 0
    except:
        pass

    with open('data/payments.json', 'r') as f:
        data = json.load(f)
    data[str(user_id)][str(payment_id)] = {"status": status, "price": price}
    with open('data/payments.json', 'w') as f:
        json.dump(data, f)
    return 1

def getPayment(user_id, payment_id=0):
    try:
        with open('data/payments.json', 'r') as f:
            data = json.load(f)
            if data[str(user_id)] == {}:
                return []
            else:
                if payment_id != 0:
                    return data[str(user_id)][str(payment_id)]
                else:
                    return data[str(user_id)]
    except:
        return []

def editPayment(user_id, payment_id, price, status="ok"):
    try:
        with open('data/payments.json', 'r') as f:
            data = json.load(f)
        data[str(user_id)][str(payment_id)] = {"status": status, "price": price}
        with open('data/payments.json', 'w') as f:
            json.dump(data, f)
        return 1
    except:
        return 0

def getPackages():
    with open('data/packages.json', 'r') as f:
        data = json.load(f)
    return data


def addConfigs(package_id, config_id):
    try:
        with open('data/configs.json', 'r') as f:
            data = json.load(f)
        data[str(package_id)].append(config_id)
        with open('data/configs.json', 'w') as f:
            json.dump(data, f)
        return 'Done'
    except:
        return 'Error'


def removeAllConfigs(package_id):
    try:
        with open('data/configs.json', 'r') as f:
            data = json.load(f)
        data[str(package_id)].clear()
        with open('data/configs.json', 'w') as f:
            json.dump(data, f)
        return True
    except:
        return 'Error'


def getConfig(package_id, user_id):
    with open('data/configs.json', 'r') as f:
        data = json.load(f)
    try:
        if len(data[str(package_id)]["available"]) == 0:
            return 'NoConfig'
        config_id = data[str(package_id)]["available"].pop(0)
        data[str(package_id)]['sold'][str(config_id)] = user_id
        with open('data/configs.json', 'w') as f:
            json.dump(data, f)
        return config_id
    except:
        return 'Error'