import random
import string
import time
import json

import bcrypt

from app.models import models
from app.libs import handlers

class LoginHandlers(handlers.BaseHandler):
    def get(self):
        self._render()
    
    def post(self):
        form_data = self._build_form_data()
        msg = ''
        if not form_data['username']  or not form_data['password']:
            msg = '用户名或密码不能为空'
            self._render(form_data=form_data, msg=msg)
            return
        user = models.User.get_user_by_login(form_data['username'])
        if not user:
            msg = '用户名不存在'
            self._render(form_data=form_data, msg=msg)
            return
        
        password = form_data['password']
        salt_key = str(user.salt_key)
        user_hash_pwd = str(user.hash_pwd)
        login_flag = False
        if user_hash_pwd:
            if bcrypt.hashpw((password+salt_key).encode(),
                    user_hash_pwd.encode()) == user_hash_pwd.encode():
                login_flag = True
        if not login_flag:
            msg = '用户名或者密码错误'
            self._render(form_data, msg)
            return
        sess_key = ''.join(
            random.choice(string.ascii_lowercase + string.digits) \
            for i in range(10)
        )
        session = {"id":sess_key, "time":int(time.time())}
        try:
            sessions = json.loads(user.sessions)
        except:
            sessions = list()
        if not isinstance(sessions, list):
            sessions = list()
        sessions.append(session)
        if len(sessions) > 5:
            sessions = sessions[-5:]
        user.sessions = json.dumps(sessions)
        user.save()
        self.set_cookie('session',
            user.user_name+":"+sess_key
        )
        self.redirect("/")

    def _render(self, form_data='', msg=''):
        self.render(
            'login.html',
            form_data = form_data,
            msg = msg
        )
    
    def _list_form_keys(self):
        return ['username', 'password']


class LoginOutHandlers(handlers.BaseHandler):
    def get(self):
        self.clear_cookie('session')
        self.redirect('/')