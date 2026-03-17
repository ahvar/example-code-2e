# Mojifinder: Unicode character search examples

Examples from _Fluent Python, Second Edition_—Chapter 22, _Asynchronous Programming_.

## How to run `web_mojifinder.py`

`web_mojifinder.py` is a Web application built with _[FastAPI](https://fastapi.tiangolo.com/)_.
To run it, first install _FastAPI_ and an ASGI server.
The application was tested with _[Uvicorn](https://www.uvicorn.org/)_.

```
$ pip install fastapi uvicorn
```

Now you can use `uvicorn` to run the app.

```
$ uvicorn web_mojifinder:app
```

Finally, visit http://127.0.0.1:8000/ with your browser to see the search form.


## Flask version: `web_mojifinder_flask.py`

`web_mojifinder_flask.py` provides the same `/` and `/search?q=...` behavior using
[Flask](https://flask.palletsprojects.com/) instead of FastAPI.

Install dependencies:

```
$ pip install -r requirements-flask.txt
```

Run with Gunicorn:

```
$ gunicorn web_mojifinder_flask:app
```

Then open http://127.0.0.1:8000/.

### FastAPI vs Flask in this example

- **Server-rendered page + JSON endpoint:** both frameworks can do this equally well.
- **Decorators:** both use route decorators (`@app.get(...)`).
- **Type hints and response-model validation:** FastAPI has first-class support. Flask
  does not validate/serialize from type hints by default.
- **OpenAPI/Swagger docs:** FastAPI generates them automatically. Flask can do it with
  extensions such as `flask-smorest`, `flask-openapi3`, or `apispec`, but that is extra setup.
- **Missing query parameter behavior:** FastAPI returns `422` automatically for required
  params; in Flask we return `422` explicitly.
- **Async I/O model:** FastAPI runs on ASGI (typically Uvicorn/Hypercorn) and is designed
  for native async endpoints. Flask is a WSGI framework; Flask 2+ accepts `async def`
  views, but execution still goes through WSGI workers and does not provide the same
  high-concurrency async model as ASGI.

### About Gunicorn and async options

- `gunicorn web_mojifinder_flask:app` runs Flask via WSGI workers.
- For async-heavy workloads, common options are:
  - use FastAPI (or another ASGI framework) with Uvicorn/Hypercorn workers;
  - keep Flask and pair Gunicorn with alternative worker classes (`gevent`, `eventlet`) if
    your stack supports cooperative I/O.

### Traefik as edge router / load balancer

Using Traefik in front of Flask+Gunicorn or FastAPI+Uvicorn is a recommended production
pattern for TLS termination, routing, load balancing, and static asset handling.
In this tiny sample, serving `static/form.html` directly from the app keeps setup simple.


## Directory contents

These files can be run as scripts directly from the command line:

- `charindex.py`: libray used by the Mojifinder examples. Also works as CLI search script.
- `tcp_mojifinder.py`: TCP/IP Unicode search server. Depends only on the Python 3.9 standard library. Use a telnet application as client.
- `web_mojifinder_bottle.py`: Unicode Web service. Depends on `bottle.py` and `static/form.html`. Use an HTTP browser as client.

This program requires an ASGI server to run it:

- `web_mojifinder.py`: Unicode Web service. Depends on _[FastAPI](https://fastapi.tiangolo.com/)_ and `static/form.html`.

This program is a Flask WSGI app usually run with Gunicorn:

- `web_mojifinder_flask.py`: Unicode Web service. Depends on _[Flask](https://flask.palletsprojects.com/)_ and `static/form.html`.

Support files:

- `bottle.py`: local copy of the single-file _[Bottle](https://bottlepy.org/)_ Web framework.
- `requirements.txt`: list of dependencies for `web_mojifinder.py`.
- `requirements-flask.txt`: list of dependencies for `web_mojifinder_flask.py`.
- `static/form.html`: HTML form used by the `web_*` examples.
- `README.md`: this file 🤓
