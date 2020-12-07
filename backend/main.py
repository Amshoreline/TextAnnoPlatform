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

@app.route('/create', methods=['POST'])
def create():
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8002')
