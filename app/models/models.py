import peewee
from app.models import base_model
import json
from peewee import fn

class User(base_model.BaseModel):
    user_id = peewee.AutoField(primary_key=True)
    user_name = peewee.CharField()
    hash_pwd = peewee.CharField()
    about = peewee.CharField(default='')
    salt_key = peewee.CharField()
    sessions = peewee.CharField()


    class Meta:
        db_table = "app_user"


    @classmethod
    def get_user_by_login(cls, user_name):
        try:
            return User.get(User.user_name==user_name)
        except User.DoesNotExist:
            return None

    @classmethod
    def get_user_by_sess(cls, user_name, session_id):
        user = None
        sessions = None

        try:
            user = User.get(User.user_name == user_name)
            sessions = json.loads(user.sessions)
        except:
            return None

        if not user or not sessions or not isinstance(sessions, list):
            return None

        for session in sessions:
            if isinstance(session, dict) and session.get("id") \
                    and session["id"] == session_id:
                return user
        return None
    
    @classmethod
    def get_about_text_by_user_id(cls, user_id):
        try:
            obj = cls.get(cls.user_id == user_id)
            text = obj.about
            return text
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def get_about_text_by_user_name(cls, user_name):
        try:
            obj = cls.get(cls.user_name == user_name)
            text = obj.about
            return text
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def update_abount_text_by_user_id(cls, about, user_id):
        cls.update(about = about).where(cls.user_id == user_id).execute()


class Ariticle(base_model.BaseModel):
    article_id = peewee.AutoField(primary_key = True)
    article_title = peewee.CharField()
    type_choices = (
        (0, 'python'),
        (1, 'mysql'),
        (2, 'tornado'),
        (3, 'django'),
        (4, 'peewee'),
        (5, 'jquery'),
        (6, 'html/css'),
        (7, 'java_script'),
        (8, '个人随笔')
    )
    article_type = peewee.SmallIntegerField(choices = type_choices)
    create_time = peewee.DateTimeField()


    class Meta:
        db_table = "app_article"
    

    @classmethod
    def create_article(cls, data):
        return cls.create(**data)

    @classmethod
    def update_article_by_article_id(cls, article_id, data):
        cls.update(**data).where(cls.article_id == article_id).execute()

    @classmethod
    def get_article_list(cls, current_page, search_value=None):
        article_list = None
        if search_value is not None:
            article_list = cls.select().where(search_value). \
                order_by(-cls.article_id).paginate(int(current_page), 10)
        else:
            article_list = cls.select().order_by(-cls.article_id). \
                paginate(int(current_page), 10)
        return article_list
    
    @classmethod
    def get_article_count(cls, search_value=None):
        article_count = None
        if search_value:
            article_count = cls.select().where(search_value).count()
        else:
            article_count = cls.select().count(cls._meta.database)
        return article_count
    
    @classmethod
    def get_article_type_count(cls):
        return cls.select(cls.article_type, fn.COUNT(cls.article_type). \
            alias('ct')).group_by(cls.article_type).dicts()
    
    @classmethod
    def get_article_by_article_id(cls, article_id):
        try:
            return cls.get(cls.article_id == article_id)
        except cls.DoesNotExist:
            return None


class ArticleContent(base_model.BaseModel):
    content_id = peewee.AutoField(primary_key = True)
    article_id = peewee.BigIntegerField()
    content = peewee.TextField()

    
    class Meta:
        db_table = "app_article_content"

    @classmethod
    def get_content_by_article_id(cls, article_id):
        try:
            return ArticleContent.get(ArticleContent.article_id==article_id)
        except User.DoesNotExist:
            return None

    @classmethod
    def create_content(cls, data):
        cls.create(**data)
    
    @classmethod
    def update_content_by_article_id(cls, article_id, data):
        cls.update(**data).where(cls.article_id == article_id).execute()
    
    @classmethod
    def delete_content_by_article_id(cls, article_id):
        cls.delete().where(cls.article_id == article_id).execute()
