import os.path

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.auth
import tornado.gen

from tornado.options import define, options, parse_command_line

define('port', default=8000, help='run on the given port', type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/chat', ChatHandler),
            (r'/ws', WebSocketHandler),
            (r'/login', LoginHandler),
            (r'/logout', LogoutHandler),
        ]
        settings = dict(
            cookie_secret="your_cookie_secret",
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            twitter_consumer_key='your_twitter_consumer_key',
            twitter_consumer_secret='your_twitter_consumer_secret',
            login_url='/',
            xsrf_cookies=True,
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user = self.get_secure_cookie("username")
        if user:
            user = user.decode("utf-8")
        return user


class MainHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.redirect('/chat')
        self.render('index.html')


class ChatHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('chat.html', user=self.current_user)


class WebSocketHandler(BaseHandler, tornado.websocket.WebSocketHandler):
    connections = set()

    def open(self):
        WebSocketHandler.connections.add(self)

    def on_close(self):
        WebSocketHandler.connections.remove(self)

    def on_message(self, msg):
        self.send_messages(msg)

    def send_messages(self, msg):
        for conn in self.connections:
            conn.write_message({'name': self.current_user, 'msg': msg})


class LoginHandler(tornado.web.RequestHandler, tornado.auth.TwitterMixin):
    @tornado.gen.coroutine
    def get(self):
        if self.get_argument("oauth_token", None):
            user = yield self.get_authenticated_user()
            self.set_secure_cookie('username', str(user['username']))
            self.redirect("/chat")
        else:
            yield self.authorize_redirect()


class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect("/")


def main():
    parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
