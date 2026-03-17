from pathlib import Path
from unicodedata import name

from flask import Flask, Response, abort, jsonify, request

from charindex import InvertedIndex

STATIC_PATH = Path(__file__).parent.absolute() / 'static'

app = Flask(__name__)


def init(app: Flask) -> None:
    app.config['INDEX'] = InvertedIndex()
    app.config['FORM_HTML'] = (STATIC_PATH / 'form.html').read_text()


init(app)


@app.get('/search')
def search() -> Response:
    q = request.args.get('q')
    if not q:
        abort(422, description='Missing required query string parameter: q')

    chars = sorted(app.config['INDEX'].search(q))
    payload = [{'char': c, 'name': name(c)} for c in chars]
    return jsonify(payload)


@app.get('/')
def form() -> Response:
    return Response(app.config['FORM_HTML'], mimetype='text/html')
