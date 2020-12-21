import os
import re
import json
import numpy as np

from flask import Flask, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# cors = CORS(app, resources={r"/test": {"origins": "*"}})
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/get_instruction', methods=['POST'])
def get_set_list():
    return 'Hello World! 暂无使用说明'

@app.route('/create_text', methods=['POST'])
def create_text():
    params = request.get_json(silent=True)
    title = params['title']
    content = params['content']
    if not os.path.exists('txts'):
        os.mkdir(txts)
    if os.path.exists(f'txts/{title}.txt'):
        return '创建失败，文件已存在！'
    else:
        with open(f'txts/{title}.txt', 'w') as writer:
            writer.write(content)
        return '创建成功'

@app.route('', method=['POST'])
def _():
    return 'not implemented'


@app.route('upload_text', method=['POST'])
def upload_text():
    return 'not implemented'


@app.route('download_text', method=['POST'])
def download_text():
    return 'not implemented'


@app.route('remove_text', method=['POST'])
def remove_text():
    return 'not implemented'


@app.route('save_anno', method=['POST'])
def save_anno():
    return 'not implemented'


@app.route('upload_anno', method=['POST'])
def upload_anno():
    return 'not implemented'


@app.route('download_anno', method=['POST'])
def download_anno():
    return 'not implemented'


@app.route('choose_text', method=['POST'])
def choose_text():
    return 'not implemented'


@app.route('predict_entity', method=['POST'])
def predict_entity():
    return 'not implemented'


@app.route('predict_relation', method=['POST'])
def predict_relation():
    return 'not implemented'


@app.route('show_anno', method=['POST'])
def show_anno():
    return 'not implemented'


@app.route('show_graph', method=['POST'])
def show_graph():
    return 'not implemented'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8002')
