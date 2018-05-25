import peewee
# try:
#     import config_local
# except:
#     pass
import config as config_web


database_proxy = peewee.Proxy()

db_obj = None
if not db_obj:
    db_obj = peewee.MySQLDatabase(
        config_web.db_name,
        host=config_web.db_host,
        port=int(config_web.db_port),
        user=config_web.db_user,
        password=config_web.db_pass,
        charset='utf8mb4'
    )
    database_proxy.initialize(db_obj)



class BaseModel(peewee.Model):
    class Meta:
        database = database_proxy

