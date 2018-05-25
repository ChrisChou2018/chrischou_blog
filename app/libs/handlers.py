import json
import tornado.web
from app.models import models

class BaseHandler(tornado.web.RequestHandler):
    def _list_form_keys(self):
        return list()
    
    def _build_form_data(self):
        form_data = dict()
        for key in self._list_form_keys():
            form_data[key] = self.get_argument(key, "")
        return form_data
    
    def get_current_user(self):
        cookie_data = self.get_cookie("session")
        if not cookie_data:
            return None

        try:
            user_name, session_id = cookie_data.split(":")
        except:
            return None

        member = models.User.get_user_by_sess(user_name, session_id)
        return member