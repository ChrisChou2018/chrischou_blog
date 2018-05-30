import string
import random
import time
import datetime
import json

import tornado.web
import tornado.escape
import bcrypt

from app.libs import handlers
from app.models import models
from app.libs import decorators



class IndexHandlers(handlers.BaseHandler):
    def get(self):
        current_page =  self.get_argument('page', 1)
        article_type_id = self.get_argument('article_type', None)
        filter_args = None
        article_list = models.Ariticle.select()
        type_count_dict = models.Ariticle.get_article_type_count()
        type_dict = dict(models.Ariticle.type_choices)
        if article_type_id:
            filter_args = '&article_type={0}'.format(article_type_id)
            search_value = (models.Ariticle.article_type == article_type_id)
            article_list = models.Ariticle. \
                get_article_list(current_page, search_value)
            article_count  = models.Ariticle.get_article_count(search_value)
        else:
            article_list = models.Ariticle.get_article_list(current_page)
            article_count = models.Ariticle.get_article_count()
        if '?' in self.request.uri:
            url = self.request.uri.split('?')[0]
        else:
            url = self.request.uri
        about_text = models.User.get_about_text_by_user_name('chris')
        self.render(
            'index.html', 
            type_dict = type_dict,
            type_count_dict = type_count_dict,
            article_list = article_list,
            article_count = article_count,
            article_content_list = article_list,
            current_page = current_page,
            filter_args = filter_args,
            url = url,
            about_text = about_text
        )


def remove_xss(text):
    text = str(text).replace('<script>', ''). \
        replace('/<script>', '').replace('alert', '')
    return text

class AddArticleHandlers(handlers.BaseHandler):
    @decorators.login_verification
    def get(self):
        ariticle_type = models.Ariticle.type_choices
        self.render(
            'editor.html',
            ariticle_type = ariticle_type,
            article_obj = None,
            article_content_obj = None
        )

    @decorators.login_verification
    def post(self):
        data = self._build_form_data()
        data['article_title'] = remove_xss(data['article_title'])
        data['article_content'] = remove_xss(data['article_content'])
        data['article_type'] = int(data['article_type'])
        data['create_time'] = datetime.datetime.now()
        article_content = data.pop('article_content')
        article_obj = models.Ariticle.create_article(data)
        content_data = {
            'content': article_content,
            'article_id': article_obj.article_id
        }
        models.ArticleContent.create_content(content_data)
        self.write(json.dumps({'status' : True}))
        
    def _list_form_keys(self):
        return ['article_title', 'article_type', 'article_content']


class ArticleContentHandlers(handlers.BaseHandler):
    def get(self):
        article_type = models.Ariticle.type_choices
        article_id = self.get_argument('article_id')
        article_obj = models.Ariticle.get_by_id(article_id)
        type_count_dict = models.Ariticle.get_article_type_count()
        about_text = models.User.get_about_text_by_user_name('chris')
        self.render(
            'article_content.html',
            article_type = article_type,
            article_obj = article_obj,
            type_count_dict = type_count_dict,
            about_text = about_text
        )


class EditorArticleHandlers(handlers.BaseHandler):
    def get(self):
        article_id = self.get_argument('article_id')
        article_content_obj = models.ArticleContent. \
            get_content_by_article_id(article_id)
        article_obj = models.Ariticle. \
            get_article_by_article_id(article_id)
        article_content_obj = article_content_obj
        ariticle_type = models.Ariticle.type_choices
        self.render(
            'editor.html',
            ariticle_type = ariticle_type,
            article_obj = article_obj,
            article_content_obj = article_content_obj
        )
    
    def post(self):
        data = self._build_form_data()
        article_id = self.get_argument('article_id')
        data['article_title'] = remove_xss(data['article_title'])
        data['article_content'] = remove_xss(data['article_content'])
        data['article_type'] = int(data['article_type'])
        article_content = data.pop('article_content')
        models.Ariticle.update_article_by_article_id(article_id, data)
        content_data = {
            'content': article_content,
        }
        models.ArticleContent.update_content_by_article_id(article_id, content_data)
        self.write(json.dumps({'status' : True}))
    
    def _list_form_keys(self):
        return ['article_title', 'article_type', 'article_content']


class DeleteArticleHandler(handlers.BaseHandler):
    def post(self):
        article_id = self.get_argument('article_id')
        models.Ariticle.delete_by_id(article_id)
        models.ArticleContent.delete_content_by_article_id(article_id)
        self.write({'status':True})


class JsEditorAboutHandler(handlers.BaseHandler):
    def get(self):
        user_id = self.current_user.user_id
        about_text = models.User.get_about_text_by_user_id(user_id)
        self.write({'data': about_text, 'status': True})
    
    def post(self):
        about_text = self.get_argument('about')
        user_id = self.current_user.user_id
        models.User.update_abount_text_by_user_id(about_text, user_id)
        self.write({'status': True})