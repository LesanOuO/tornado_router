import os
import tornado.web
import tornado.httpserver

from tornado_router import GloabelRouter


def main():
    app = tornado.web.Application(handlers=GloabelRouter.handlers,
                                  template_path=os.path.join(os.path.dirname(__file__), "template"),
                                  static_path=os.path.join(os.path.dirname(__file__), "static"),
                                  debug=True,
                                  allow_remote_access=True)
    app.listen(9000)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
