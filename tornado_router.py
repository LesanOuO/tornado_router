import functools
import importlib
import os
import traceback
import tornado


class Router():

    def __init__(self, base_handler, base_module='handler'):
        self._handlers = []
        self._requests = []
        self._base_handler = base_handler
        self._base_module = base_module

    @property
    def handlers(self):
        include(self._base_module)
        return self._handlers

    @property
    def requests(self):
        return self._requests

    def _auth_wrap(self, f):

        @functools.wraps(f)
        @tornado.gen.coroutine
        def auth_request(handler):
            yield handler.get_cur_user()
            yield f(handler)

        return auth_request

    def _json_wrap(self, f):

        @functools.wraps(f)
        @tornado.gen.coroutine
        def json_request(handler):
            resp = yield f(handler)
            handler.set_header('Content-Type', 'application/json')
            handler.write_json(resp)

        return json_request

    def route(self, url=None, method='get', auth=False, json=True, xsrf=True):
        if method.upper() not in tornado.web.RequestHandler.SUPPORTED_METHODS:
            raise ValueError('invalid HTTP method {} found! tornado only supports HTTP methods in {}'.format(
                method, tornado.web.RequestHandler.SUPPORTED_METHODS))

        def req_wrap(f):
            if not self._base_handler:
                raise RuntimeError('base_handler must be initialized!')

            f_url = url
            if not f_url:
                f_url = '/' + f.__name__

            req = self._json_wrap(tornado.gen.coroutine(f)) if json else tornado.gen.coroutine(f)
            req = self._auth_wrap(req) if auth else req

            flag = True
            for item in self._handlers:
                if f_url == item[0]:
                    flag = False
                    setattr(item[1], method.lower(), req)
            if flag:

                class InnerHandler(self._base_handler):
                    pass

                setattr(InnerHandler, method.lower(), req)

                if not xsrf:
                    setattr(InnerHandler, "check_xsrf_cookie", lambda self: None)

                self._handlers.append((f_url, InnerHandler))

            @functools.wraps(f)
            def request():
                pass

            self._requests.append(request)
            return request

        return req_wrap


class BaseHandler(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        tornado.web.RequestHandler.__init__(self, application, request, **kwargs)

        if self.settings['allow_remote_access']:
            self.allow_remote_access()

    def allow_remote_access(self):
        self.set_header("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        self.set_header(
            "Access-Control-Allow-Headers", "Content-Type, Depth, User-Agent, X-File-Size, "
            "X-Requested-With, X-Requested-By, If-Modified-Since, "
            "X-File-Name, Cache-Control, Token")
        self.set_header('Access-Control-Allow-Origin', '*')

    def write_error(self, status_code, **kwargs):
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            lines = []
            for line in traceback.format_exception(*kwargs["exc_info"]):
                lines.append(line)

            self.write_json(dict(traceback=''.join(lines)), status_code, self._reason)

        else:
            self.write_json(None, status_code, self._reason)

    def write_json(self, data, status_code=0, msg='success.'):
        self.finish(tornado.escape.json_encode({'code': status_code, 'msg': msg, 'data': data}))

    def is_logined(self):
        if 'Token' in self.request.headers:
            token = self.request.headers['Token']
            return self.validate_token(token)

    def validate_token(self):
        # Implementation is required
        return 'lesan'

    @tornado.gen.coroutine
    def get_cur_user(self):
        if not hasattr(self, '_cur_user'):
            self._cur_user = None
        current_user = self._cur_user
        if not current_user:
            current_user = self.is_logined()
        self._cur_user = current_user
        return self._cur_user


GloabelRouter = Router(base_handler=BaseHandler)


def include(module):
    for root, dirs, files in os.walk(module):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                module_name = file[:-3]
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                print(f"Imported module {module_name} from {file_path}")
