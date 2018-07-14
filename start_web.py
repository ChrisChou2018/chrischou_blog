import tornado.ioloop
import tornado.web
from config import application_settings as settings
import tornado.log
from tornado.options import define, options
from tornado.options import parse_command_line
from app import blog
from app.ui_modules.app import view
# 解析命令行参数 如--help
parse_command_line()

define('port', 9000)

class BaseApplication(tornado.web.Application):
    def log_request(self, handler):
        log_method = tornado.log.access_log.error
        if handler.get_status() < 400:
            log_method = tornado.log.access_log.info
        elif handler.get_status() < 500:
            log_method = tornado.log.access_log.warning

        request_time = 1000.0 * handler.request.request_time()
        request_summary = "%s %s (%s)" % (handler.request.method, handler.request.uri,
                                          handler.request.remote_ip)
        log_method("%d %s %.2fms", handler.get_status(),
                   request_summary, request_time)

settings['ui_modules'] = view
app = BaseApplication(
    blog.urls,
    **settings,
)


def main(): 
    """
    如果xheaders为True，将支持把所有请求的HTTP头解析成X-Real-Ip和X-Scheme格式，
    而tornado原先将HTTP头解析成remote IP和HTTP scheme格式。
    这种格式的HTTP头在Tornado运行于反向代理或均衡负载服务器的后端时将非常有用。
    """
    app.listen(options.port, address="127.0.0.1", xheaders=True)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()