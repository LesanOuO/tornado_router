from tornado_router_plus import GloabelRouter


@GloabelRouter.route(method='get', url='/', auth=True)
def index(handler):
    return 'hello tornado!'


@GloabelRouter.route()
def login(handler):
    return 'hello login'
