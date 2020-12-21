<template>
    <div id='test' >
        <div id='func_area'>
            <a-button class='button' @click='create_text'>新建文本</a-button>
            <a-button class='button' @click='upload_text'>上传文本</a-button>
            <a-button class='button' @click='download_text'>下载文本</a-button>
            <a-button class='button' @click='remove_text'>删除文本</a-button>
            <a-button class='button' @click='save_anno'>保存标注</a-button>
            <a-button class='button' @click='upload_anno'>上传标注</a-button>
            <a-button class='button' @click='download_anno'>下载标注</a-button>
            <a-button class='button' @click='clear_anno'>清空标注</a-button>
            <a-dropdown class='button' style='width:190px'>
                <a-menu slot='overlay'>
                    <a-menu-item key="1">1st item</a-menu-item>
                    <a-menu-item key="2">2nd item</a-menu-item>
                    <a-menu-item key="3">3rd item</a-menu-item>
                </a-menu>
                <a-button>
                    选择文本 <a-icon type="down" />
                </a-button>
            </a-dropdown>
            <a-button class='button' @click='add_entity'>增加实体</a-button>
            <a-button class='button' @click='predict_entity'>预测实体</a-button>
            <a-button class='button' @click='remove_entity'>删除实体</a-button>
            <a-button class='button' @click='edit_entity'>编辑实体</a-button>
            <a-button class='button' @click='add_relation'>增加关系</a-button>
            <a-button class='button' @click='predict_relation'>预测关系</a-button>
            <a-button class='button' @click='remove_relation'>删除关系</a-button>
            <a-button class='button' @click='edit_relation'>编辑关系</a-button>
        </div>
        <div id='op_area'>
            <a-textarea
                placeholder='Type your message here.'
                v-model='content'
                :autosize='{ minRows: 6, maxRows: 6}'
            />
            <a-button class='button' @click='instruct'>
                帮助
            </a-button>
            <a-button class='button' style='float: right' @click='show_anno'>
                显示标注
            </a-button>
            <a-button class='button' style='float: right' @click='show_graph'>
                显示图谱
            </a-button>
            <br>
            <canvas id='show_area' />
        </div>
    </div>
</template>

<script lang='ts'>
import { Component, Prop, Vue } from 'vue-property-decorator'

// Tools and functions
import axios from 'axios'
declare const Buffer: any


let backend_address: string = 'http://localhost:8002'


// Block right
// function blockright(oEvent: any) {
//     if (window.event) {
//         oEvent = window.event
//         oEvent.returnValue = false
//     } else {
//         oEvent.preventDefault()
//     }
// }
// window.onload = () => {document.oncontextmenu = blockright}

// The main class
@Component
export default class Test extends Vue {
    show_area: any
    context: any
    content: string = ''

    instruct() {
        axios
            .post(backend_address + '/get_instruction', {})
            .then(response => {
                alert(response.data)
            })
            .catch(error => {
                alert(error)
            })
    }

    create_text() {
        let title: any = prompt('请输入当前文本名称')
        if (title == null) {
            return
        }
        axios
            .post(
                backend_address + '/create_text',
                {'title': title, 'content': this.content},
            )
            .then(response => {
                alert(response.data)
            })
            .catch(error => {
                alert(error)
            })
    }

    upload_text() {}

    download_text() {}

    remove_text() {}

    save_anno() {}

    upload_anno() {}

    download_anno() {}

    clear_anno() {}

    choose_text() {}

    add_entity() {}

    predict_entity() {}

    remove_entity() {}

    edit_entity() {}

    add_relation() {}

    predict_relation() {}

    remove_relation() {}

    edit_relation() {}

    show_anno() {}

    show_graph() {}

    mouseDown(e: any) {
        console.log(e.offsetX, e.offsetY)
    }

    mouseUp(e: any) {
        // do nothing
    }

    keyDown(e: any) {
        console.log(e.key)
    }

    mounted() {
        // Initialize components
        this.show_area = document.getElementById('show_area') as HTMLCanvasElement
        this.context = this.show_area.getContext('2d') as CanvasRenderingContext2D
        this.show_area.onmousedown = this.mouseDown
        this.show_area.onmouseup = this.mouseUp
        window.addEventListener('keydown', this.keyDown)
        this.show_area.width = 600
        this.show_area.height = 210
    }
}
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->
<style scoped>
#func_area {
    width: 210px;
    height: 400px;
    border-style: solid;
    border-color: black;
    border-width: 1.5px;
    position: absolute;
    top: 30px;
    left: 30px;
}
#op_area {
    width: 600px;
    height: 400px;
    border-style: solid;
    border-color: blue;
    border-width: 0px;
    position: absolute;
    top: 30px;
    left: 260px;
}
#show_area {
    margin-top: 10px;
    border-style: solid;
    border-color: black;
    border-width: 1.5px;
}
.button {
    margin-top: 10px;
    margin-left: 10px;
}
</style>