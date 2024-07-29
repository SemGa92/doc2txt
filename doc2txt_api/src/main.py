import os
import time
from flask import (
    Flask,
    request,
    jsonify
    )
from pydantic import ValidationError
from utils.auth import my_auth
from utils.my_logging import LOGGER
from models.document import Document
from controllers.doc_mgr import process_doc

app = Flask(__name__)
app.config['DEBUG'] = os.getenv('MY_DEBUG')


@app.route('/', methods=['GET'])
def alive():
    return jsonify({'success': True}), 200


@app.route('/to-txt', methods=['POST'])
@my_auth
def to_txt():
    start_time = time.perf_counter()
    body = request.get_json()

    try:
        doc = Document(**body)
        text = process_doc(doc)
    except Exception as e:
        LOGGER.error(str(e))
        return jsonify({'success': False, 'error': str(e)}), 400

    end_time = time.perf_counter()
    print(f"Run time: {end_time - start_time} seconds", flush=True)

    return jsonify({'success': True, 'text': text}), 200


if __name__ == '__main__':
    app.run(
        host = '0.0.0.0', #default port 5000
        threaded = True
        )
