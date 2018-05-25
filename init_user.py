import bcrypt
import random
import string
from app.models import models
import json



def regist_user():
    user_name = None
    pass_word = None
    while True:
        user_name = input('用户名>>>')
        pass_word = input('密码>>>')
        pass_word2 = input('确认密码>>>')
        if pass_word != pass_word2:
            continue
        else:
            break
    random_salt_key = ''.join(random.choice(string.ascii_lowercase + string.digits) \
        for i in range(8)
    )
    haspwd = bcrypt.hashpw((pass_word+random_salt_key).encode(), bcrypt.gensalt())
    models.User.create(
        user_name = user_name,
        hash_pwd = haspwd,
        sessions = json.dumps(list()),
        salt_key = random_salt_key,
    )

regist_user()