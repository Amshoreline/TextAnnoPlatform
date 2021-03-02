import json
import time
import random
import string

from flask import Flask, request, make_response
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
data_path = 'data.json'
data_json = json.load(open(data_path, encoding='UTF-8'))
text_json = data_json['text']
label_json = data_json['label']
# label_dict = {}
# for ann in label_json:
#     label_dict[ann['id']] = ann['name']
s = string.ascii_lowercase + '0123456789'


"""
flask被暂停时保存data_json到本地
"""
def save_data():
    data_json['text'] = text_json
    data_json['label'] = label_json
    with open(data_path, 'w', encoding='UTF-8') as f:
        f.write(json.dumps(data_json, indent=2, ensure_ascii=False))
        print('保存成功')

"""
获取文本列表
"""
@app.route('/get_text_list')
def get_text_list():
    result_json = {
        "count": len(text_json),
        "results": text_json
    }
    rst = make_response(json.dumps(result_json))
    rst.headers['Access-Control-Allow-Origin'] = '*'
    return rst

"""
新建文本
"""
@app.route('/create_text', methods=['POST'])
def create_text():
    global text_json
    params = request.get_json(silent=True)
    title = params['title']
    content = params['content']
    create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    text_json += [{
        "id": ''.join(random.sample(s,5))+str(time.time_ns())[:-2],
        "title": title,
        "content": content,
        "create_time": create_time,
        "update_time": create_time,
        "is_checked": False,
        "annotation": [],
        "relation": []
    }]
    return '创建成功'

"""
更新文本
"""
@app.route('/update_text', methods=['POST'])
def update_text():
    global text_json
    new_text = request.get_json(silent=True)
    new_text['update_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    new_text.pop('_index')
    new_text.pop('_rowKey')

    for i, item in enumerate(text_json):
        # print(item['id'], new_text['id'],item['id'] == new_text['id'])
        if item['id'] == new_text['id']:
            if item['content'] != new_text['content']: # 当修改了文本，应该删掉所有的标注和关系
                new_text['annotation'] = []
                new_text['relation'] = []
            text_json[i] = new_text
            return '修改成功'
    return '修改失败'

"""
删除文本
"""
@app.route('/delete_text')
def delete_text():
    global text_json
    id = request.args["id"]
    if id == 'all':
        text_json = []
        return '已删除所有文本'
    for i, item in enumerate(text_json):
        if item['id'] == id:
            text_json.pop(i)
            return "删除成功"
    return '删除失败'

"""
获取标签列表
"""
@app.route('/get_label_list')
def get_label_list():
    result_json = {
        "count": len(label_json),
        "results": label_json
    }
    rst = make_response(json.dumps(result_json))
    rst.headers['Access-Control-Allow-Origin'] = '*'
    return rst

"""
创建标签
"""
@app.route('/create_label', methods=['POST'])
def create_label():
    global label_json
    params = request.get_json(silent=True)
    name = params['name']
    shortcut = params['shortcut']
    bg_color = params['bg_color']
    create_label_local(name, shortcut, bg_color)
    return '创建成功'

def create_label_local(name, shortcut, bg_color):
    global label_json
    create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    id = random.choice(s) + str(time.time_ns())[:-2]
    label_json += [{
        "id": id,
        "name": name,
        "shortcut": shortcut,
        "bg_color": bg_color,
        "create_time": create_time,
        "update_time": create_time
    }]
    return id

"""
更新标签
"""
@app.route('/update_label', methods=['POST'])
def update_label():
    global label_json
    new_label = request.get_json(silent=True)
    new_label['update_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    new_label.pop('_index')
    new_label.pop('_rowKey')
    for i, item in enumerate(label_json):
        if item['id'] == new_label['id']:
            label_json[i] = new_label
            # label_dict[new_label['id']] = new_label['name']
            return '更新成功'
    return '更新失败'

"""
删除标签
"""
@app.route('/delete_label')
def delete_label():
    global label_json
    id = request.args["id"] # 标签的id
    for i, item in enumerate(label_json):
        if item['id'] == id:
            label_json.pop(i)
            break
    # 还要把文本里有这个标签的标注去掉
    for i, text in enumerate(text_json):
        anns = text['annotation']
        for j, ann in enumerate(anns):
            if ann['label_id'] == id:
                text_json[i]['annotation'].pop(j)
    return '删除成功'

"""
更新标注
"""
@app.route('/update_ann', methods=['POST'])
def update_ann():
    global text_json
    new_text = request.get_json(silent=True)
    new_text['update_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    new_text['annotation'] = json.loads(new_text['annotation'])
    new_text['relation'] = json.loads(new_text['relation'])
    for i, item in enumerate(text_json):
        if item['id'] == new_text['id']:
            text_json[i] = new_text
            return '更新成功'
    return '更新失败'

"""
批量导入(json)
"""
@app.route('/import_data_json', methods=['POST'])
def import_data_json():
    global text_json
    title_key = request.form['title']
    content_key = request.form['content']
    file = request.files['file']
    params = json.load(file)
    if(title_key!=""):
        for text in params:
            title = text[title_key]
            content = text[content_key]
            create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            text_json += [{
                "id": ''.join(random.sample(s,5))+str(time.time_ns())[:-2],
                "title": title,
                "content": content,
                "create_time": create_time,
                "update_time": create_time,
                "is_checked": False,
                "annotation": [],
                "relation": []
            }]
    else:
        for text in params:
            content = text[content_key]
            create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            text_json += [{
                "id": ''.join(random.sample(s,5))+str(time.time_ns())[:-2],
                "title": "(无标题)",
                "content": content,
                "create_time": create_time,
                "update_time": create_time,
                "is_checked": False,
                "annotation": [],
                "relation": []
            }]
    return str(len(params))

"""
选择文件导入文本(txt)
"""
@app.route('/import_data', methods=['POST'])
def import_data():
    global text_json
    file = request.files['file']
    # print(file)

    title = file.filename
    content = file.read().decode()
    create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    text_json += [{
        "id": ''.join(random.sample(s,5))+str(time.time_ns())[:-2],
        "title": title,
        "content": content,
        "create_time": create_time,
        "update_time": create_time,
        "is_checked": False,
        "annotation": [],
        "relation": []
    }]
    return ''


"""上传标注"""
@app.route('/upload_ann', methods=['POST'])
def upload_ann():
    global text_json
    text_id = request.form['text_id']
    start_offset_key = request.form['start_offset_key']
    end_offset_key = request.form['end_offset_key']
    label_type_key = request.form['label_type_key']
    file = request.files['file']
    params = json.load(file)
    anns = []
    text_index = -1

    for i, text in enumerate(text_json):
        if text['id'] == text_id:
            text_index = i
            break
    text = text_json[text_index]['content']
    limit = len(text)
    for ann in params:
        start_offset = ann[start_offset_key]
        if start_offset>=limit: # 超过文本长度的去掉
            continue
        end_offset = ann[end_offset_key]
        label_type = ann[label_type_key]
        label_id = ''

        for label in label_json:
            if label['name'] == label_type:
                label_id = label['id']
                break
        # 如果没有这个标签，会自动创建一个默认颜色，无快捷键的标签
        if label_id == '':
            label_id = create_label_local(label_type, '', 'default')

        anns += [{
            "id": ''.join(random.sample(s,4))+'-'+str(time.time_ns())[:13]+'-'+''.join(random.sample(s,5)),
            "label_id": label_id,
            "label_type": label_type,
            "entity": text[start_offset: end_offset],
            "start_offset": int(start_offset),
            "end_offset": int(end_offset)
        }]

    text_json[text_index]['annotation'] = anns
    return str(len(params))

"""
导出文本
"""
@app.route('/export_text')
def export_text():
    result_json = []
    for text in text_json:
        result_json += [{
            "id": text['id'],
            "title": text['title'],
            "content": text['content']
        }]

    return json.dumps(result_json, indent=2)

"""
导出实体标注
"""
@app.route('/export_ann')
def export_ann():
    result_json = []
    for i, text in enumerate(text_json):
        annotation = text['annotation']
        anns = []
        if(len(annotation)!=0):
            for i, ann in enumerate(annotation):
                anns += [{
                    'label_type': ann['label_type'],
                    'entity': ann['entity']
                }]
            result_json += [{
                "text": text['content'],
                "entities": anns
            }]

    return json.dumps(result_json, indent=2)

"""
导出关系标注
"""
@app.route('/export_ann_r')
def export_ann_r():
    result_json = []
    for i, text in enumerate(text_json):
        relation = text['relation']
        anns = []
        if(len(relation)!=0):
            for i, ann in enumerate(relation):
                anns += [{
                    "source": ann['source_entity'],
                    "target": ann['target_entity'],
                    "label": ann['label']
                }]
            result_json += [{
                "text": text['content'],
                "annotations": anns
            }]

    return json.dumps(result_json, indent=2)

"""
导出实体和关系标注
"""
@app.route('/export_ann_b')
def export_ann_b():
    result_json = []
    for i, text in enumerate(text_json):
        relation = text['relation']
        anns1, anns2 = [], []
        flag = False
        if(len(relation)!=0):
            flag = True
            for i, ann in enumerate(relation):
                anns2 += [{
                    "source": ann['source_entity'],
                    "target": ann['target_entity'],
                    "label": ann['label']
                }]

        annotation = text['annotation']
        if (len(annotation) != 0):
            flag = True
            for i, ann in enumerate(annotation):
                anns1 += [{
                    'label_type': ann['label_type'],
                    'entity': ann['entity']
                }]
        if flag:
            result_json += [{
                "text": text['content'],
                "entities": anns1,
                "relations": anns2
            }]

    return json.dumps(result_json, indent=2)

"""
导出所有信息
"""
@app.route('/export_data')
def export_data():
    return json.dumps(text_json, indent=2)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8002')
    save_data()
