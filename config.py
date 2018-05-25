import os
# from app.ui_modules.app import view

db_host = os.getenv("DB_HOST", "127.0.0.1")
# db_host = os.getenv("DB_HOST", "localhost")
db_name = os.getenv("DB_NAME", "tornado_blog")
db_port = os.getenv("DB_PORT", "3306")
db_user = os.getenv("DB_USER", "root")
db_pass = os.getenv("DB_PASS", "123")



application_settings  = {
    'debug':True,
    'template_path':'app/templates',
    'static_path':'static',
    'static_url_prefix': '/static/',
    "xsrf_cookies": True,
    # 'ui_modules':view,
}