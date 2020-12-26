<template>
    <div>
        <div id="header">
        <ul class="clearfix">
            <li class="header-name">中文医疗实体和关系抽取系统</li>
            <span style="margin-right:20px">|</span>
            <li><a href="">实体抽取</a></li>
            <li><a href="">实体识别</a></li>
            <li><a href="">关系抽取</a></li>
            <li><a href="">实体标注</a></li>
            <li><a href="">关系标注</a></li>
            <li class="header-right" style="margin-right:30px"><a href="">社区</a></li>
            <li class="header-right"><a href="">咨询</a></li>
            <li class="header-right"><a href=""><a-icon style="font-size:15px" type="search" /></a>&nbsp;<input class="search" type="text" /></li>
        </ul>
        </div>
        <div id="head">
            <div class="head-content">
                <div class="head-texth">医疗实体和关系抽取系统</div>
                <div class="head-textc">
                    大量文本数据例如文本病历、医学文献等，尽管也蕴含着许多有研究价值的信息，
                    但却因为具有非结构化、专业化等特点，难以对其进行数据深度利用。<br/>
                    因此，进行纵向的病种命名实体识别及关系抽取研究，
                    归纳总结出能够快速并且在人工干预较少的情况下提取出准确信息的方法具有重要意义。
                </div>
            </div>
        </div>
        <div id="detail">
            <div class="detail-title">功能介绍</div>
            <div class="detail-list mr40">
                <img style="width:30px" src="../../public/img/icon-1.jpg" alt="">
                <div class="detail-list-title">实体标注</div>
                <div class="detail-list-content">Lorem ipsum dolor, sit amet consectetur adipisicing elit. Corporis, a?</div>
            </div>
            <div class="detail-list ">
                <img style="width:30px" src="../../public/img/icon-2.jpg" alt="">
                <div class="detail-list-title">关系标注</div>
                <div class="detail-list-content">Lorem ipsum dolor sit amet consectetur adipisicing elit. Tenetur, veritatis.</div>
            </div>
            <div class="detail-list  mr40">
                <img style="width:30px" src="../../public/img/icon-3.jpg" alt="">
                <div class="detail-list-title">实体抽取</div>
                <div class="detail-list-content">医疗知识抽取是自动化构建医学领域知识图谱的关键步骤之一，主要包括医疗命名实体识别和医疗关系抽取两个任务。</div>
            </div>
            <div class="detail-list ">
                <img style="width:30px" src="../../public/img/icon-4.jpg" alt="">
                <div class="detail-list-title">关系抽取</div>
                <div class="detail-list-content">关系抽取是信息抽取领域中的重要任务之一，目的在于抽取文本中的实体对，以及识别实体对之间的语义关系。</div>
            </div>
            <div class="detail-title">功能使用</div>
        </div>
        <div id='test' class='clearfix'>
            <div id='func_area' class=''>
                <a-button class='button' @click='create_text'>新建文本</a-button>
                <a-button class='button' @click='upload_text'>上传文本</a-button>
                <a-button class='button' @click='download_text'>下载文本</a-button>
                <a-button class='button' @click='remove_text'>删除文本</a-button>
                <a-button class='button' @click='save_anno'>保存标注</a-button>
                <a-button class='button' @click='upload_anno'>上传标注</a-button>
                <a-button class='button' @click='download_anno'>下载标注</a-button>
                <a-button class='button' @click='clear_anno'>清空标注</a-button>
                <a-dropdown class='button' style='width:196px'>
                    <a-menu slot='overlay'>
                        <a-menu-item key="1" >1st item</a-menu-item>
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
            <div id='op_area' class='clearfix'>
                <a-textarea
                    placeholder='Type your message here.'
                    v-model='content'
                    :autosize='{ minRows: 8, maxRows: 8}'
                />
                <a-button class='button' @click='instruct'>
                    帮助
                </a-button>
                <a-button class='button' style='float: right; margin-right:10px' @click='show_anno'>
                    显示标注
                </a-button>
                <a-button class='button' style='float: right' @click='show_graph'>
                    显示图谱
                </a-button>
                <br>
                <canvas id='show_area' />
            </div>
        </div>
        <div id="detail">
            <div class="detail-title" style="margin-top:60px">应用场景</div>
            <div class="detail-list-2">
                <div class="detail-box">
                    <div class="detail-list-title-2">医疗健康文本的关系抽取和属性抽取</div>
                    <div class="detail-list-content-2">Lorem ipsum dolor sit amet consectetur adipisicing elit. Facilis, quibusdam voluptates. Commodi ipsa ea libero optio magnam veniam mollitia voluptas sequi, architecto illum facilis ullam?</div>
                </div>
                <div class="detail-img"></div>
            </div>
            
            <div class="detail-title">技术特色</div>
            <div class="detail-list-1 mr80">
                <img style="width:30px" src="../../public/img/icon-1.jpg" alt="">
                <div class="detail-list-title">实体识别准确</div>
                <div class="detail-list-content">融合词法分析技术，自动识别医学文本中的疾病名称、临床表现等，识别准确率可达xx%以上</div>
            </div>
            <div class="detail-list-1 mr80">
                <img style="width:30px" src="../../public/img/icon-3.jpg" alt="">
                <div class="detail-list-title">维度丰富</div>
                <div class="detail-list-content">多种维度信息，包含实体、关系等多种维度标签，全面覆盖文章中关键信息</div>
            </div>
            <div class="detail-list-1">
                <img style="width:30px" src="../../public/img/icon-5.jpg" alt="">
                <div class="detail-list-title">识别精度高</div>
                <div class="detail-list-content">通过互联网用户行为挖掘海量训练样本，提高了算法在复杂多变的应用场景下的效果稳定性</div>
            </div>
        </div>
        <div id="footer">
            <a href="javascript: buttom1();">关于我们</a>
            &nbsp;&nbsp;&nbsp;/&nbsp;&nbsp;&nbsp;
            <a href="javascript: buttom2();">行业解决方案</a>
            &nbsp;&nbsp;&nbsp;/&nbsp;&nbsp;&nbsp;
            <a href="javascript: buttom3();">关注我们</a>
            &nbsp;&nbsp;&nbsp;/&nbsp;&nbsp;&nbsp;
            <a href="javascript: buttom4();">联系方式</a><br/>
            copyright©2020-2077
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

// window.onload=function setzoom()
// {
//     let s:number;
//     if(!!window.ActiveXObject || "ActiveXObject" in window){
//         s = window.screen.width / 1600;
//     }
//     else{
//         s = window.screen.width / 1600;
//     }
//     function resize() {
//         document.body.style.transformOrigin = '0 0';
//         document.body.style.transform = 'scale(' + s + ',' + s + ')';
//         document.body.style.width = window.innerWidth / s + 'px';
//         document.body.style.height = window.innerHeight / s + 'px';
//     }
//     window.onresize = function () {
//         resize();
//     }
//     resize();
// }


</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->
<style scoped>
.clearfix::after{
	content: "";
	display: block;
	clear: both;
}
ul, li{
    list-style: none;
}
a{
    color: #fdfdfd;
}
input {
    outline-color: invert;
    outline-style: none;
    outline-width: 0px;
    border: none;
    border-style: none;
    text-shadow: none;
    -webkit-appearance: none;
    -webkit-user-select: text;
    outline-color: transparent;
    box-shadow: none;
}
.mr40{
    margin-right: 40px;
}
.mr80{
    margin-right: 80px;
}
* {
    font-family: 'microsoft yahei ui', "Microsoft YaHei", SimSun, sans-serif
}
/**顶部 */
#header{
    width: 100%;
    height: 60px;
    background-color: black;
}
#header table{
    text-align: center; 
    color: #fff; 
    font-size: 14px; 
    height: 56px
}
#header ul{
    color: #fdfdfd; 
    font-size:16px; 
    font-weight:bold;
}
#header li{
    margin-top: 11px;
    margin-right: 20px;
    display: inline-block;
}
#header .header-name{
    font-size: 22px;
    color: dodgerblue;
    cursor: pointer;
}
#header .header-right{
    font-size: 13px;
    margin-top: 18px;
    float: right;
    cursor: pointer;
}
#header .search{
    color: gray;
    height: 22px;
    display: inline-block;
    border-radius: 15px;
    box-sizing: border-box;
    padding: 0 10px;
}
/**头部图片及简介 */
#head{
    height: 350px;
    color: white;
    background-image: url('../../public/img/banner.jpg');
    background-position-x: 100%;
    background-position-y: center;
    background-repeat: no-repeat;
    background-origin: padding-box;
    background-clip: border-box;
    overflow:hidden;
    background-size: cover;
    box-sizing: border-box;
}
#head .head-content{
    overflow: hidden;
    width: 750px;
    position: absolute;
    top: 28%;
    left: 35%;
    transform: translate(-50%,-50%);
    z-index: 1;
}
#head .head-texth{
    font-size: 30px;
    letter-spacing: 2px;
}
#head .head-textc{
    margin: 30px 110px 0 0;
    font-size: 16px;
    line-height: 26px;
}
/**功能介绍 */
#detail, #test {
    width: 1000px;
    margin: 30px auto;
    /* margin-top: 50px; */
}
#detail .detail-title{
    font-size: 32px;
    text-align: center;
    margin-top: 35px;
}
#detail .detail-list{
    margin-top: 30px;
    padding: 0 10px;
    width: 480px;
    height: 120px;
    display: inline-block;
}
#detail .detail-list-title{
    display: inline-block;
    font-size: 22px;
    line-height: 30px;
    font-weight: 700;
    text-indent: 1em; 
    vertical-align:middle
}
#detail .detail-list-content{
    font-size: 14px;
    line-height: 24px;
    margin-top: 10px;
    margin-left: 52px;
}
#detail .detail-list-1{
    margin-top: 30px;
    padding: 0 10px;
    width: 280px;
    height: 100px;
    display: inline-block;
}
#detail .detail-list-2{
    margin-top: 30px;
    padding: 0 10px;
    height: 150px;
    width: 1000px;
    display: inline-block;
}
#detail .detail-box{
    /* width: 630px; */
    margin-right: 350px;
    letter-spacing: 0;
}
#detail .detail-list-title-2{
    display: inline-block;
    font-size: 22px;
    line-height: 30px;
    font-weight: 700;
    text-indent: 1em;
    margin-left: 7px;
    vertical-align:middle;
}
#detail .detail-list-content-2{
    font-size: 14px;
    line-height: 24px;
    margin-top: 10px;
    margin-left: 30px;
    float: left;
}
#detail .detail-img {
    float: right;
    width: 280px;
    height: 130px;
    -moz-background-size: cover;
    background-size: cover;
    background-image: url("../../public/img/test1.jpg");
    cursor: pointer;
    position: relative;
    right: 20px;
    top: -30px
}
/**功能区 */
#func_area {
    float: left;
    margin-left: 30px;
    width: 240px;
    height: 500px;
    background-color: #f7f7f7;
}
/**操作/显示区 */
#op_area {
    width: 700px;
    height: 500px;
    float: left;
    padding: 20px;
    background-color: #f7f7f7;
}
#show_area {
    width: 100%;
    height: 200px;
    margin-top: 20px;
    border-style: solid;
    border-color: #d9d9d9;
    border-width: 1.5px;
    border-radius: 5px;
}
.button {
    margin-top: 20px;
    margin-left: 20px;
}
/**底部 */
#footer{
    padding: 9px;
    width: 100%;
    height: 60px;
    background-color: #f3f3f5;
    margin-top: 200px;
    text-align: center
}
#footer a{
    color: dodgerblue;
}
</style>