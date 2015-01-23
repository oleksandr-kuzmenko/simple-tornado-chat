import os.path

import tornado.ioloop
import tornado.web
import tornado.websocket

from tornado.options import define, options, parse_command_line

define('port', default=8000, help='run on the given port', type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/chat', ChatHandler),
        ]
        settings = dict(
            cookie_secret="your_cookie_secret",
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            xsrf_cookies=True,
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class ChatHandler(tornado.websocket.WebSocketHandler):
    connections = set()

    def open(self):
        ChatHandler.connections.add(self)

    def on_close(self):
        ChatHandler.connections.remove(self)

    def on_message(self, msg):
        ChatHandler.send_messages(msg)

    @classmethod
    def send_messages(cls, msg):
        for conn in cls.connections:
            conn.write_message('Someone said: ' + msg)


def main():
    parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
