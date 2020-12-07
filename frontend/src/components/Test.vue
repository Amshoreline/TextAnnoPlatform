<template>
    <div id='test' >
        <a-textarea
            placeholder='Type your message here.'
            v-model='content'
            :autosize='{ minRows: 2, maxRows: 8 }'
        />
        <a-button style='margin-top: 10px; float: right' type='primary' @click='create'>
            创建文档
        </a-button>
        <a-button style='margin-top: 10px; float: left' type='primary' @click='instruct'>
            使用说明
        </a-button>
        <div id='canvas' style='width:800px;height:800px;' align='center'>
            <canvas id='bg' width=768 height=768></canvas>
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
    bg: any
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
            .finally(() => {})
    }

    create() {
        let title: any = prompt('请输入当前文本名称')
        if (title == null) {
            return
        }
        axios
            .post(
                backend_address + '/create',
                {'title': title, 'content': this.content},
            )
            .then(response => {
                alert(response.data)
            })
            .catch(error => {
                alert(error)
            })
            .finally(() => {})
    }

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
        this.bg = document.getElementById('bg') as HTMLCanvasElement
        this.context = this.bg.getContext('2d') as CanvasRenderingContext2D
        this.bg.onmousedown = this.mouseDown
        this.bg.onmouseup = this.mouseUp
        window.addEventListener('keydown', this.keyDown)
    }
}
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->
<style scoped>

</style>