import express from 'express';
import * as path from 'path'
import * as fs from 'fs-extra'
import axios from 'axios'


const app = express();
const port = 3000;

let image_name: string
let data_sended: boolean


let annotations = {
    'last_update': 0,
    'data': []
}

function write_json(file_path: string) {
    let buf: string = JSON.stringify(annotations, null, 4)
    fs.removeSync(file_path)
    fs.writeFileSync(file_path, buf)
    console.log('write file_path = ', file_path)
}

function read_annotations(file_path: string) {
    let res: any = JSON.parse(fs.readFileSync(file_path, 'utf8'))
    console.log('Get annotations')
    annotations = res
    return annotations
}

function read_image_list() {
    let image_list_path: string = path.resolve('server/') + '/info/image_list.json'
    let res: any = JSON.parse(fs.readFileSync(image_list_path, 'utf8'))
    return res
}

function read_image(file_path: string) {
    let res: any = fs.readFileSync(file_path)
    return res
}

function request_prediciton(request_image_name: string, bbox: any, res: any) {
    let base_path: string = ''
    let image_data = ''
    // if (image_name == request_image_name && data_sended) {
    //     image_data = ''
    // } else {
    //     image_name = request_image_name
    //     base_path = path.resolve('server/') + '/img'
    //     image_data = read_image(base_path + '/' + request_image_name)
    // }
    axios
        .post('http://localhost:8888/get_pred', {'image_name': request_image_name, 'image': image_data, 'bbox': bbox})
        .then(response => {
            data_sended = true
            console.log(response.data)
            res.json(response.data)
        })
        .catch(error => {
            console.log(error)
        })
        .finally(() => {})
}
/*
An example of 'annotations':
{
    'last_update': 1,
    'data': [
        {
            'bbox': {
                'xmin': 250,
                'ymin': 150,
                'width': 300,
                'height': 300
            },
            'path': [
                { 'x': 425, 'y': 215},
                { 'x': 443, 'y': 205},
                { 'x': 460, 'y': 215},
                { 'x': 460, 'y': 235},
                { 'x': 443, 'y': 245},
                { 'x': 425, 'y': 235}
            ]
        }
    ]
}
*/

// TODO: It would be better if the front end sent the image's name for all of its requests.
// Get an image
// Done
app.get('/get_image', (req: any, res: any) => {
    res.header('Access-Control-Allow-Origin', '*');
    let base_path: string = path.resolve('server/') + '/img'
    image_name = req.query.image_name
    data_sended = false
    console.log('Get image: ' + image_name)
    let image_data = read_image(base_path + '/' + image_name)
    console.log(image_data)
    res.json(image_data)
})

// Get annotations
// Done
app.get('/get_anno', (req: any, res: any) => {
    res.header('Access-Control-Allow-Origin', '*');
    let base_path: string = path.resolve('server/') + '/json'
    console.log('Get anno: ' + req.query.image_name)
    let json_name: string = req.query.image_name.split('.')[0] + '.json'
    read_annotations(base_path + '/' + json_name)
    console.log('last_update: ' + annotations['last_update'])
    res.json(annotations['data'])
})

// Save annotations
// Done
app.get('/save_anno', (req: any, res: any) => {
    console.log('save_anno', req.query.image_name)
    annotations['last_update'] += 1
    annotations['data'] = JSON.parse(req.query.anno)
    let base_path: string = path.resolve('server/') + '/json'
    let json_name: string = image_name.split('.')[0] + '.json'
    write_json(base_path + '/' + json_name)
})

// Get image list
// Done
app.get('/get_image_list', (req: any, res: any) => {
    res.header('Access-Control-Allow-Origin', '*');
    console.log('get image list')
    let image_list = read_image_list()
    console.log(image_list)
    res.json(image_list)
})

// Get bbox prediction
app.get('/get_bbox_pred', (req: any, res: any) => {
    res.header('Access-Control-Allow-Origin', '*');
    request_prediciton(req.query.image_name, req.query.bbox, res)
})

app.get('/update_anno', (req: any, res: any) => {
    console.log('update_anno')
    res.header('Access-Control-Allow-Origin', '*');
    let annotation = JSON.parse(req.query.anno)
    axios
        .post('http://localhost:8888/update_pred', {'image_name': req.query.image_name, 'bbox': annotation['bbox'], 'anno': annotation['path']})
        .then(response => {
            console.log(response.data)
            res.json(response.data)
        })
        .catch(error => {
            console.log('update_anno error')
        })
        .finally(() => {})
})

// These are example functions

// let messages = {
//     last_update: 1,
//     data: [{name: 'admin', text: 'Welcome to the chat room.'}],
// };

// function write(file_path: string) {
//     let buf: string[] = []
//     buf.push('hello')
//     buf.push('world')
//     fs.removeSync(file_path)
//     fs.writeFileSync(file_path, buf.join('\n'))
//     console.log('write file_path = ', file_path)
// }

// app.get('/get', (req: any, res: any) => {
//     res.header('Access-Control-Allow-Origin', '*');
//     res.json(messages);
// });

// app.get('/new', (req: any, res: any) => {
//     res.header('Access-Control-Allow-Origin', '*');
//     let ip: string = req.headers['x-forwarded-for'] || req.connection.remoteAddress;
//     if (ip === '::1') {
//         ip = '127.0.0.1';
//     }
//     // tslint:disable-next-line: no-unused-expression
//     messages.last_update = Date.now();
//     messages.data.push({
//         name: ip,
//         text: req.query.data,
//     });
//     res.send('Ok');
//     // req.query.color1 === 'red'  // true
//     // req.query.color2 === 'blue' // true
//     // console.log('here');
//     // console.log(req.body.data);
//     // res.end('Ok');
//     // var user_name=req.body.user;
//     // var password=req.body.password;
//     // console.log('User name = '+user_name+', password is '+password);
//     // res.end('yes');
// });

// tslint:disable-next-line: no-console
app.listen(port, () => console.log(`Example app listening on port ${port}!`));