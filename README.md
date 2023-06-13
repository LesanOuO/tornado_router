# tornado_router plus

This project is an enhancement of [tornado_router](https://github.com/ginking/tornado_router)

Decorator based router for Tornado Web Framework that help reduce development time.

## Features

* RESTful support

The original author's project does not provide RESTful style support.

```python
@router.route("index")
@router.route("index", "post")
```

* JWT Token auth

```python
@router.route(auth=True)
```

* JSON request
```python
@router.route(json=True)
```

* Auto import

You just need to create a handler folder in the root of your project to automatically scan for all decorators

```python
app = tornado.web.Application(handlers=GloabelRouter.handlers)
```

* Usage

For more information on how to use it, please refer to the example folder