<template>
  <div class="layout" style="margin:10px 0">
    <Layout>
      <Sider ref="side" hide-trigger collapsible :collapsed-width="0" v-model="is_collapsed" width="400" :style="{background: '#fff'}">
        <!-- <Sider hide-trigger width="380" :style="{background: '#fff'}"> -->
        <Menu :active-name="row_index" theme="light" width="auto" :style="{height:'100%'}">
          <MenuGroup title="　　　　　　　　 　标注文本">
            <MenuItem v-for="(doc, index) in cur_data" :name="index.toString()" :key=index :data-preview-id="index" @click.native="rowChange(index)">
              <span style="max-height:41px; width:100%;display:block;overflow:hidden;text-align:justify">
                <Icon type="ios-checkmark" size='24' color="#33a060" v-show="doc.is_checked"/>{{ doc.content.slice(0, 100) }}
              </span>
            </MenuItem>
            <br>
            <Row type="flex" align="middle" justify="center">
            <Page size="small" :total="page_options.total" :page-size="page_options.page_size" :current="page_options.page" show-elevator @on-change="pageChange"></Page>
            </Row>
            <br>
          </MenuGroup>
        </Menu>
      </Sider>

      <Layout>
        <Content :style="{padding: '10px', background: '#fff'}">
          <!-- 文本 -->
          <Card>
            <!-- 标签 -->
            <div slot="title" style="text-align:center">
              <Row align="middle">
                <Col span='1'>
                  <Icon @click.native="collapsedSider" :class="rotateIcon" type="md-menu" size="26" style="cursor:pointer;color:#a0a0a0"></Icon>
                </Col>
                <Col span='23'>
                  <Span v-for="(label, index) in labels" :key="index">
                    <a v-shortkey.once="label? label.shortcut.split('+'): ''" @shortkey="annotate(label.id)">
                      <Tag @click.native="annotate(label.id)" :color="label.bg_color" size='large' style="font-size:16px">
                        {{ label.name }}{{ label.shortcut? ' - '+label.shortcut: '' }}
                      </Tag>
                    </a>&nbsp;
                  </Span>
                  <Poptip trigger="hover" title="提示" word-wrap width='150' content="标签 - 快捷键；在标注上单击右键可取消标注" placement="right-start">
                    <Icon size='20' type="ios-help-circle-outline" />
                  </Poptip>
                </Col> 
              </Row>
            </div>
            <div id='textContainer' @click="setSelectedRange()" style="position:relative;line-height:2.5em;">
              <span
                  v-for="(para, index) in chunks"
                  :key="index"
                  :style="{
                    color:tag_color[para.bg_color].color,
                    borderWidth:'1px',
                    borderStyle:'solid',
                    borderColor:tag_color[para.bg_color].borderColor,
                    borderRadius:'5px',
                    padding:'5px',
                    backgroundColor:tag_color[para.bg_color].background,
                  }"
                  :class="{tag: para.bg_color!='#fff'}"  
                  :id="para.id"
                  v-on:contextmenu.prevent="removeAnnotation(para.bg_color, para.id)"
                  v-on:click="MarkNode"
                >{{para.text}}</span>
            </div>
          </Card>
          <!-- 按钮 -->
          <Row style="margin:15px 0" justify="center" type="flex" align="middle">
            <Tooltip content="标记为已完成标注" placement="bottom-start">
              <Button type="success" ghost @click="checkAnnotation()">
                <Icon type="md-checkmark" /> &nbsp;Check&nbsp;&nbsp;
              </Button>&nbsp;&nbsp;
            </Tooltip>
            
            <Tooltip content="标记为未完成标注" placement="bottom-start">
              <Button type="warning" ghost @click="uncheckAnnotation">
              <Icon type="md-close" /> Uncheck 
              </Button>&nbsp;&nbsp;
            </Tooltip>

            <Tooltip content="选择两个实体可建立关系" placement="bottom-start">
              <Button type="primary" ghost @click="addRelationship">增加关系</Button>&nbsp;&nbsp;
            </Tooltip>

            <Button type="primary" ghost @click="showLinks">隐藏关系</Button>&nbsp;&nbsp;

            <Tooltip content="点击上传 json 格式文件实现标注" placement="bottom-start">
              <Button type="primary" ghost @click="show_modal = true">上传标注</Button>&nbsp;&nbsp;
            </Tooltip>

            <Poptip confirm title="您确认清空该文本的关系标注吗？" @on-ok="clearAnn(0)">
              <Button type="primary" ghost>清空关系</Button>&nbsp;&nbsp;
            </Poptip>

            <Poptip confirm title="您确认清空该文本的所有标注吗？" @on-ok="clearAnn(1)">
              <Button type="primary" ghost>清空标注</Button>&nbsp;&nbsp;
            </Poptip>
            <!-- <Button type="primary" ghost>预测实体</Button>&nbsp;&nbsp; -->
            <!-- <Button type="primary" ghost>预测关系</Button> -->
          </Row>
          <!-- 显示 -->
          <Row>
            <Col span="24">
              <Card style="height:100%;">
                <span style="margin:0 10px 0px 5px"><Icon type="md-paper-plane" /></span>实体显示
                <div style="margin:8px 0;"></div>
                <div style="margin-left:7px">
                  <Tag style="margin-right:10px" v-for="(para, index) in entities" :key="index" class="tag1" :color="para.bg_color" size='medium'>{{para.text}}</Tag>
                </div>
              </Card>
            </Col>
          </Row>
          <Row style="margin-top:10px">
            <Col span="24">
              <Card style="height:100%;">
                <span style="margin:0 10px 0 8px"><Icon type="ios-pulse" /></span>关系显示
                <div style="margin:8px 0;"></div>
                <div style="padding-left:7px">
                  <Tag class='tag1' style='height:36px;line-height:32px;margin-right:10px' v-for="(para, index) in relations" :key='index' >
                    <Tag type="border" color="primary" size='medium'>{{para.source}}</Tag>
                    <span style="font-size:12px;color:blue">&nbsp;&nbsp;{{para.label}}</span><Icon type="md-arrow-dropright" color='blue' />&nbsp;
                    <Tag type="border" color="primary" size='medium'>{{para.target}}</Tag>
                  </Tag>
                </div>
              </Card>
            </Col>
          </Row>
          <Card style="margin-top:10px">
            <div id="graph" style="text-align:center; width:100%;  min-height:600px;">
            </div>
          </Card>
        </Content>
      </Layout>
    </Layout>

    <Modal v-model="show_modal" title="批量上传(json)" width="828">
      <Alert show-icon>
        标注格式
        <template slot="desc"><p style="font-family: 'Times New Roman'">文件内容格式为 json，每个标注必须有起始位置、终止位置、标签类型三个键，下面可以输入每个键的名字 <br>
        例如三个键对应的 key 为 "start_offset"、"end_offset"、"label_type"：<br>
        <strong>[{<font color='red'>"start_offset"</font>: "1", <font color='red'>"end_offset"</font>: "3", <font color='red'>"label_type"</font>: "测试1"}, {<font color='red'>"start_offset"</font>: "7", <font color='red'>"end_offset"</font>: "12", <font color='red'>"label_type"</font>: "测试2"}]</strong>
        <br><font color='red'>如果标签类型不存在会自动创建，超过文本长度的标注会被舍弃，只支持上传 txt 文件</font></p></template>
      </Alert>
      <Card :bordered="false">
        <p slot="title">输入每个文本所拥有 key，没有标题则无需输入</p>
        <div style="font-family: 'Times New Roman'">
          <Input style="display:none" v-model="post_data.text_id"/>
          <font color='red'>* </font>起始位置 <strong>key</strong> ：
          <Input v-model="post_data.start_offset_key" clearable style="width: 120px" />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          <font color='red'>* </font>终止位置 <strong>key</strong> ：
          <Input v-model="post_data.end_offset_key" clearable style="width: 120px" />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          <font color='red'>* </font>标签 <strong>key</strong> ：
          <Input v-model="post_data.label_type_key" clearable style="width: 120px" />
        </div>
      </Card>
      <Upload
        type="drag"
        :action="upload_ann_url"
        :data="post_data"
        :format="['txt']"
        :on-format-error="handleFormatError"
        :on-success="handleSuccess"
        :on-error="handleError"
      >
        <div style="padding: 20px 0">
          <Icon type="ios-cloud-upload" size="52" style="color: #3399ff"></Icon>
          <p>Click or drag files here to upload</p>
        </div>
      </Upload>
    </Modal>
    
    <BackTop></BackTop>
  </div>
</template>
<script>
import $ from 'jquery'
import axios from 'axios'
import URL from '../../setting'

export default {
  data() {
    return {
      show_modal: false,
      show_plumb: true,
      is_collapsed: false,
      upload_ann_url: URL.upload_ann,
      post_data: {
        text_id: '',
        label_type_key: 'label_type',
        start_offset_key: 'start_offset',
        end_offset_key: 'end_offset',
      },
      my_echarts: null,
      jsPlumb: null,
      jsplumb_setting: { // 很多连接线，它们的样式是相同的，所以定义一个默认配置
        Anchor: 'Top', // Anchor:['Top', 'Bottom'],'Continuous',
        Connector: 'Flowchart',
        Container: 'textContainer',
        // ConnectionsDetachable: false, // 鼠标不能拖动删除线||节点是否可以用鼠标拖动使其断开，默认为true。即用鼠标连接上的连线，也可以使用鼠标拖动让其断开。设置成false，可以让其拖动也不会自动断开。
        // DeleteEndpointsOnDetach: false, // 删除线的时候节点不删除
        Endpoint: 'Blank', // Endpoint: ["Dot", {height: 3, width: 3}],
        // EndpointStyle: {radius: 3, fill: "#666"}, // 线端点的样式
        PaintStyle : {strokeWidth: 2, stroke : "#2f54eb" }, // 线宽和颜色
        HoverPaintStyle: {strokeWidth: 3, stroke : "#f5222d"},
        MaxConnections: -1,
      },
      turn: '1',
      source: null,
      targe: null,
      tag_color: {
        'magenta': {
          color: '#eb2f96',
          background: '#fff0f6',
          borderColor: '#ffadd2',
        },
        'red': {
          color: '#f5222d',
          background: '#fff1f0',
          borderColor: '#ffa39e',
        },
        'volcano': {
          color: '#fa541c',
          background: '#fff2e8',
          borderColor: '#ffbb96',
        },
        'orange': {
          color: '#fa8c16',
          background: '#fff7e6',
          borderColor: '#ffd591',
        },
        'gold': {
          color: '#faad14',
          background: '#fffbe6',
          borderColor: '#ffe58f',
        },
        'yellow': {
          color: '#fadb14',
          background: '#feffe6',
          borderColor: '#fffb8f',
        },
        'lime': {
          color: '#a0d911',
          background: '#fcffe6',
          borderColor: '#eaff8f',
        },
        'green': {
          color: '#52c41a',
          background: '#f6ffed',
          borderColor: '#b7eb8f',
        },
        'cyan': {
          color: '#13c2c2',
          background: '#e6fffb',
          borderColor: '#87e8de',
        },
        'blue': {
          color: '#1890ff',
          background: '#e6f7ff',
          borderColor: '#91d5ff',
        },
        'geekblue': {
          color: '#2f54eb',
          background: '#f0f5ff',
          borderColor: '#adc6ff',
        },
        'purple': {
          color: '#722ed1',
          background: '#f9f0ff',
          borderColor: '#d3adf7',
        },
        'default': {
          color: '#515a6e',
          background: '#f7f7f7',
          borderColor: '#e8eaec',
        },
        '#fff': {
          color: '#515a6e',
          background: '#fff',
          borderColor: '#fff',
        },
      },
      page_options: {
        total: 0,
        page: 1 * this.$route.query.page,
        page_size: 10,
      },
      row_index: this.$route.query.index,
      entity: '',
      start_offset: 0,
      end_offset: 0,
      data: [],
      cur_data: [
        {
          id: 0,
          title: "",
          content: "",
          annotation: [],
          relation: [],
          is_checked: false,
          create_time: "",
          update_time: "",
        }, // 空集合active-name无效的解决方案
      ],
      labels: [],
      document_info: {},
    }
  },
  methods: {
    handleSuccess(response) {
      this.queryLabel()
      this.query()
      // this.$Message.success("已上传 " + response.data + ' 个标注')
    },
    handleError(response) {
      this.$Message.error("上传失败: json解析错误")
    },
    handleFormatError(file) {
      this.$Notice.warning({
        title: '文件格式错误',
        desc: '文件【' + file.name + '】格式错误，请选择 .txt 或 .json',
      })
    },
    // 隐藏侧边文本
    collapsedSider() {
      this.$refs.side.toggleCollapse()
      let _this = this
      let t = window.setInterval(() => {
        _this.jsPlumb.repaintEverything()
      }, 20)
      window.setTimeout(() => {
        window.clearTimeout(t)
      }, 300)
    },
    // 换行
    rowChange(index) {
      this.row_index = index.toString()
      this.document_info = this.cur_data[index]
      this.document_info.annotation = this.cur_data[index].annotation
      this.document_info.relation = this.cur_data[index].relation
      this.$route.query.index = index + ''
      // 改变地址
      let url = window.location.href
      let valiable = url.split('&')[0] + '&index=' + index
      window.history.pushState({}, 0, valiable)
      this.post_data.text_id = this.document_info.id
      this.refreshGraph()
    },
    // 换页
    pageChange(index) {
      this.row_index = "0"
      this.page_options.page = index
      // 需要显示开始数据的index,(因为数据是从0开始的，页码是从1开始的，需要-1)
      let _start = (index - 1) * this.page_options.page_size
      // 需要显示结束数据的index
      let _end = index * this.page_options.page_size
      // 截取需要显示的数据
      this.cur_data = this.data.slice(_start, _end)
      this.document_info = this.data[_start] // 第一条数据
      this.$route.query.page = index
      // 改变地址
      let url = window.location.href
      let valiable = url.split('?')[0] + '?page=' + index + '&index=' + this.row_index
      window.history.pushState({}, 0, valiable)
      this.refreshGraph()
    },
    // 请求文本标注
    async query() {
      this.$Loading.start()
      await axios
        .get(
          URL.get_text_list,
        )
        .then(response => {
          if (response.status === 200) {
            this.data = response.data.results // 所有数据
            this.page_options.total = response.data.count // 总数
            let begin = (this.page_options.page - 1) * this.page_options.page_size
            let now = begin + this.row_index * 1
            this.document_info = this.data[now] // 第一条数据
            this.document_info.annotation = this.data[now].annotation // 第一条数据的标注
            this.document_info.relation = this.data[now].relation // 第一条数据的标注
            this.cur_data = [] // 当前数据
            for (let i = 0; i < this.page_options.page_size && i + begin < this.page_options.total; i++) {
              this.cur_data.push(this.data[i + begin])
            }
          }
          this.$Loading.finish()
          this.post_data.text_id = this.document_info.id
        })
        .catch(error => {
          this.$Loading.error()
          this.$Message.error(error.toString())
        })
        .then(() => {})
    },
    // 请求标签
    async queryLabel() {
      await axios
        .get(URL.get_label_list)
        .then(response => {
          if (response.status === 200) {
            this.labels = response.data.results
          }
        })
        .catch(error => {
          this.$Message.error(error.toString())
        })
        .then(() => {})
    },
    // 获取label的信息 */
    getLabelById(label_id) {
      for (let label of this.labels) {
        if (label.id === label_id) {
          return label
        }
      }
    },
    createRandomId() {
      return (Math.random() * 10000000).toString(16).substr(0, 4) + '-' + (new Date()).getTime() + '-' + Math.random().toString().substr(2, 5)
    },
    // 当选中了文本后，能够得到start/end_offset
    setSelectedRange() {
      if (window.getSelection()) {
        const range = window.getSelection().getRangeAt(0)
        const preSelectionRange = range.cloneRange()
        preSelectionRange.selectNodeContents(event.target.parentElement)
        preSelectionRange.setEnd(range.startContainer, range.startOffset)
        let start = preSelectionRange.toString().length
        let end = start + range.toString().length
        this.entity = window.getSelection().toString()
        this.start_offset = start
        this.end_offset = end
      }
    },
    // 判断范围是否合理
    validRange() {
      if (this.start_offset === this.end_offset) { // 没有距离
        return false
      }
      if ( // 超过边界
        this.start_offset > this.document_info.content.length ||
        this.end_offset > this.document_info.content.length ||
        this.start_offset < 0 || this.end_offset < 0
      ) {
        return false
      }
      // 交叉的
      let arr = this.document_info.annotation.concat()
      for (let e of arr) {
        if (e.start_offset < this.end_offset && e.end_offset > this.start_offset) {
          this.removeAnnotation(true, e.id)
          // return false
        }
      }
      return true
    },
    // 添加标注
    annotate(id) {
      if (this.validRange()) {
        this.document_info.annotation.push(
          {
            id: this.createRandomId(),
            label_id: id, // Expected property shorthand in object literal
            label_type: this.getLabelById(id).name,
            entity: this.entity,
            start_offset: this.start_offset,
            end_offset: this.end_offset,
          },
        )
        this.updateAnnotation()
      }
      // else {
      //   this.$Message.error('标注有误')
      // }
    },
    // 更新标注
    updateAnnotation() {
      let postData = JSON.parse(JSON.stringify(this.document_info))
      postData.annotation = JSON.stringify(this.document_info.annotation)
      postData.relation = JSON.stringify(this.document_info.relation)
      axios
      .post(URL.update_ann, postData)
      .then(response => {
        if (response.status === 200) {
          return
        }
      })
      .catch(error => {
        this.$Message.error(error.toString())
      })
      .then(() => {})
    },
    // 右键取消标注：文字颜色，第几条，offset
    removeAnnotation(isAnn, id) {
      if (isAnn) { // 判断如果是标注
        for (let [index, annotation] of Object.entries(this.document_info.annotation)) {
          if (annotation.id === id) {
            $(this.source).removeClass('source')
            $(this.target).removeClass('target')
            this.source = null
            this.target = null
            this.document_info.annotation.splice(index, 1)
            break
          }
        }
        this.document_info.relation = this.document_info.relation.filter(
          e => {
            return (e.source !== id && e.target !== id)
          },
        )
        this.updateAnnotation()
      }
    },
    // 标记文本
    checkAnnotation() {
      this.document_info.is_checked = true
      this.updateAnnotation()
    },
    // 取消标记
    uncheckAnnotation() {
      this.document_info.is_checked = false
      this.updateAnnotation()
    },
    // 标记关系结点
    MarkNode(event) {
      let el = $(event.currentTarget)
      if (el.hasClass('tag')) {
        if (this.turn === '1') {
          $(this.source).removeClass('source')
          this.source = event.currentTarget
          el.addClass('source')
          this.turn = '2'
        } else if (this.turn === '2') {
          $(this.target).removeClass('target')
          this.target = event.currentTarget
          el.addClass('target')
          this.turn = '1'
        }
      } else {
        $(this.source).removeClass('source')
        $(this.target).removeClass('target')
        this.turn = '1'
      }
    },
    // 增加关系
    addRelationship() {
      let s = $(this.source)
      let t = $(this.target)
      let s_id = s.attr('id')
      let t_id = t.attr('id')
      if (!(s.hasClass('source') && t.hasClass('target')) || s_id == t_id) {
        this.$Message.warning('请选择两个实体')
        return
      }
      let r_id = this.createRandomId()
      let _this = this
      this.jsPlumb.connect({
        source: s_id,
        target: t_id,
        overlays: [
          ['Arrow', {width: 8, length: 8, location: 1}],
          ['Custom', {
            create: (component) => {
              return $("<span style='background-color: white; padding:4px 4px;line-height:1em;border-radius:7px;color:#2f54eb;font-weight:bold;font-family:serif;'>(desc)</span>")
            },
            events: {
              click: (labelOverlay, originalEvent) => {
                _this.updateRelationship(labelOverlay.getElement(), labelOverlay.id)
              },
              contextmenu: (labelOverlay, originalEvent) => {
                originalEvent.preventDefault()
                _this.jsPlumb.deleteConnection(labelOverlay.component)
                _this.removeRelation(labelOverlay.id)
              },
            },
            location: 0.5,
            id: r_id + 'r',
          }],
        ],
      })

      this.document_info.relation.push(
        {
          id: r_id,
          source: s_id,
          target: t_id,
          source_entity: s.text(),
          target_entity: t.text(),
          label: '(desc)',
        },
      )
      this.updateAnnotation()
    },
    // 删除关系
    removeRelation(id) {
      for (let [index, relation] of Object.entries(this.document_info.relation)) {
        if (relation.id + 'r' === id) {
          this.document_info.relation.splice(index, 1)
          break
        }
      }
      this.updateAnnotation()
      this.$Message.success('删除成功')
    },
    // 点击关系标签，可以修改
    updateRelationship(e, id) {
      let index = 0
      let label = ''
      for (let relation of this.document_info.relation) {
        if (relation.id + 'r' === id) {
          break
        }
        index++
      }
      this.$Modal.confirm({
        render: (h) => {
          return h('Input', {
            props: {
              value: this.value,
              autofocus: true,
              placeholder: '请输入关系',
            },
            on: {
              input: (val) => {
                label = val
              },
            },
          })
        },
        onOk: () => {
          this.$Message.success('设置成功')
          e.innerHTML = label
          this.document_info.relation[index].label = label
          this.updateAnnotation()
        },
      })
    },
    // 清空标注
    clearAnn(type) {
      if (type === 0) {
        this.document_info.relation = []
      } else {
        this.document_info.annotation = []
        this.document_info.relation = []
      }
      this.jsPlumb.reset()
      this.updateAnnotation()
      this.$Message.success('已清空')
    },
    // 连接所有关系
    connectionAll() {
      let _this = this
      if (this.document_info.relation) {
        this.document_info.relation.forEach( (value) => { // function(value)
          _this.jsPlumb.connect({
            source: value.source,
            target: value.target,
            overlays: [
              ['Arrow', {width: 8, length: 8, location: 1}],
              ['Custom', {
                create: (component) => {
                  return $("<span style='background-color: white; padding:4px 4px;line-height:1em;border-radius:7px;color:#2f54eb;font-weight:bold;font-family:serif;'>" + value.label + "</span>")
                },
                events: {
                  click: (labelOverlay, originalEvent) => {
                    _this.updateRelationship(labelOverlay.getElement(), labelOverlay.id)
                  },
                  contextmenu: (labelOverlay, originalEvent) => {
                    originalEvent.preventDefault()
                    _this.jsPlumb.deleteConnection(labelOverlay.component)
                    _this.removeRelation(labelOverlay.id)
                  },
                },
                location: 0.5,
                id: value.id + 'r',
              }],
            ],
          })
          // _this.jsPlumb.draggable(value.source) 加上又报错
          // _this.jsPlumb.draggable(value.target)
        })
      }
    },
    // 显示/隐藏关系连接
    showLinks() {
      if (this.show_plumb) {
        this.jsPlumb.reset()
        this.show_plumb = false
      } else {
        this.connectionAll()
        this.show_plumb = true
      }
    },
    // 清空原来的连接重新连接
    overLinks() {
      let _this = this
      this.$nextTick(() => {
        _this.jsPlumb.reset()
        _this.connectionAll()
      })
    },
    // 点击刷新关系图
    refreshGraph() {
      let _categories = []
      let nodes = []
      let _links = []
      let ann = this.document_info.annotation
      let res = this.document_info.relation
      let len1 = this.labels.length
      let len2 = ann.length
      let len3 = res.length
      for (let i = 0; i < len1; i++) {
        let label_id = this.labels[i].id
        _categories[i] = {
          id: label_id,
          name: this.labels[i].name,
        }
        nodes.push({
          id: this.labels[i].id,
          name: this.labels[i].name.substr(0, 5),
          desc: this.labels[i].name,
          symbolSize: 80,
          label: {
            normal: {
              position: 'inside',
            },
          },
          category: i,
        })
        // 标签对应的实体
        for (let j = 0; j < len2; ++j) {
          if (ann[j].label_id == label_id) {
            let node_name = ann[j].entity
            if (node_name.length > 3) {
              node_name = node_name.substr(0, 3) + "..."
            }
            nodes.push({
              id: ann[j].id,
              name: node_name,
              desc: ann[j].entity,
              symbolSize: 50,
              category: i,
            })
            _links.push({
              source: label_id,
              target: ann[j].id,
              name: '',
            })
          }
        }
      }
      for (let i = 0; i < len3; ++i) {
        let r = res[i]
        _links.push({
          source: r.source,
          target: r.target,
          name: r.label,
        })
      }
      let option = this.my_echarts.getOption()
      option.series[0].data = nodes
      option.series[0].links = _links
      option.series[0].categories = _categories
      this.my_echarts.hideLoading()
      this.my_echarts.setOption(option)
    },
    myEcharts() {
      let _this = this
      let option = {
        // 调色盘
        // color: ['#dd6b66', '#759aa0', '#e69d87', '#8dc1a9', '#ea7e53', '#eedd78', '#73a373', '#73b9bc', '#7289ab', '#91ca8c','#f49f42'],
        color: ['#c23531', '#2f4554', '#61a0a8', '#d48265', '#91c7ae', '#749f83',  '#ca8622', '#bda29a', '#6e7074', '#546570', '#c4ccd3'],
        // color: ['#37A2DA', '#32C5E9', '#67E0E3', '#9FE6B8', '#FFDB5C', '#ff9f7f',
        // '#fb7293', '#E062AE', '#E690D1', '#e7bcf3', '#9d96f5', '#8378EA', '#96BFFF'],
        // 鼠标放上去节点提示框的配置
        tooltip: {
          formatter: (x) => {
            return x.data.desc
          },
        },
        // 工具箱
        toolbox: {
          // 显示工具箱
          show: true,
          x: '1px',
          y: '30px',
          orient: 'vertical',
          feature: {
            dataView: {
              readOnly: true,
              show: true,
              title: '',
              lang: ['', '关闭', '刷新'],
              optionToContent: (opt) => {
                let relas = _this.document_info.relation
                if (relas) {
                  let table = '<table width="666px" style="line-height: 36px;"><thead><tr>'
                              + '<th width="222px">实体1</th>'
                              + '<th width="222px">实体2</th>'
                              + '<th width="222px">关系</th>'
                              + '</tr></thead><tbody'
                  for (let i = 0, l = relas.length; i < l; i++) {
                    let rela = relas[i]
                    table += '<tr>'
                      + '<td>' + rela.source_entity + '</td>'
                      + '<td>' + rela.target_entity + '</td>'
                      + '<td>' + rela.label + '</td>'
                      + '</tr>'
                  }
                  table += '</tbody></table>'
                  return '<fieldset style="width:666px; margin: 0 auto"><legend>关系数据视图</legend>' + table + '</fieldset>'
                }
              },
            },
            myRefresh: {
                show: true,
                title: '刷新关系图',
                icon: 'path://M3.8,33.4 M47,18.9h9.8V8.7 M56.3,20.1 C52.1,9,40.5,0.6,26.8,2.1C12.6,3.7,1.6,16.2,2.1,30.6 M13,41.1H3.1v10.2 M3.7,39.9c4.2,11.1,15.8,19.5,29.5,18 c14.2-1.6,25.2-14.1,24.7-28.5',
                onclick: () => {
                  _this.refreshGraph()
                },
            },
            saveAsImage: {
              show: true,
              title: '保存为图片',
            },
          },
        },
        // 标签列表
        legend: [{
          x: 'left', //图例位置
          // data: _categories.map((a) => {
          //   return a.name
          // }),
        }],
        series: [{
          type: 'graph', // 类型:关系图
          layout: 'force', // 图的布局，类型为力导图
          symbolSize: 30, // 调整节点的大小，不过也可以在data里面分类设置
          roam: true,
          draggable: true, // 是否可拖拽
          focusNodeAdjacency: true, // 当鼠标移动到节点上，突出显示节点以及节点的边和邻接节点
          legendHoverLinks: true, // 是否启用图例 hover(悬停) 时的联动高亮
          edgeSymbol: ['circle', 'arrow'], // 边的两端的形状
          edgeSymbolSize: [2, 10], // 边两端的标记类型
          edgeLabel: { // 边上的文字
            normal: {
              textStyle: { // 文字样式
                fontSize: 16,
                color: '#4b565b',
              },
              show: true,
              formatter: (x) => { // 通过回调函数设置连线上的标签
                return x.data.name
              },
            },
          },
          symbol: 'circle',
          symbolSize: 50, // [100, 30]
          force: {
            repulsion: [100, 1000], // 节点之间的斥力因子。支持数组表达斥力范围，值越大斥力越大。
            edgeLength: [10, 220],
            gravity : 0.15, // 节点受到的向中心的引力因子。该值越大节点越往中心点
          },
          // 连线的样式
          lineStyle: {
            normal: {
              width: 2,
              color: '#4b565b',
              curveness: 0.3,
            },
          },
          // 节点的文字
          label: {
            normal: {
              show: true,
              // position : 'top',
              textStyle : { //标签的字体样式
                color : '#f0f0f0', //字体颜色
                //fontStyle : 'normal',//文字字体的风格 'normal'标准 'italic'斜体 'oblique' 倾斜
                //fontWeight : 'normal',//'normal'标准'bold'粗的'bolder'更粗的'lighter'更细的或100 | 200 | 300 | 400...
                //fontFamily : 'sans-serif', //文字的字体系列
                fontSize : 16, //字体大小
                width: 10,
                overflow: 'truncate',
                textBorderColor: '#676767',
                textBorderWidth: 2,
              },
              // formatter: function(params) { // 回调函数，你期望节点标签上显示什么
              //   return params.data.label
              // },
            },
          },
          // 数据(节点)
          // data: nodes,
          // links: _links,
          // categories: _categories,
        }],
      }
      this.my_echarts.setOption(option)
      this.refreshGraph()
    },
    async init() {
      await this.queryLabel()
      await this.query()
      let echarts = require('echarts')
      this.my_echarts = echarts.init(document.getElementById('graph'))
      this.myEcharts()
    },
  },
  mounted() {
    this.init()
    this.jsPlumb = this.$jsPlumb.getInstance(this.jsplumb_setting) // 不放init里
    // 窗口大小改变时重新画 */
    let _this = this
    window.addEventListener('resize', () => {
      _this.jsPlumb.repaintEverything()
    })
  },
  computed: {
    // 把标注按offset排列 */
    sortedEntityPositions() {
      if (this.document_info.annotation == null) {
        return null
      }
      return this.document_info.annotation.sort((a, b) => a.start_offset - b.start_offset)
    },
    // 切分标注 */
    chunks() {
      let sorted_annotation = this.sortedEntityPositions
      let res = []
      if (sorted_annotation == null) {
        // res.push(
        //   {
        //     id: '',
        //     text: this.document_info.content.slice(),
        //     bg_color: "#fff",
        //   },
        // )
        // this.jsPlumb.reset()
        return res
      }
      let left = 0
      for (let tuple of sorted_annotation) {
        // let res = []
        // tuple是一个标注
        // 标注开始位置正好是左边
        if (tuple.start_offset == left) {
          res.push(
            {
              // 把对应的offset和文本截下来
              id: tuple.id,
              start_offset: tuple.start_offset,
              end_offset: tuple.end_offset,
              text: tuple.entity,
              // this.document_info.content.slice(
              //   tuple.start_offset,
              //   tuple.end_offset
              // )
              bg_color: this.getLabelById(tuple.label_id) ? this.getLabelById(tuple.label_id).bg_color : '#fff',
            },
          )
          left = tuple.end_offset
        } else if (tuple.start_offset > left) {
          res.push(
            {
              id: '',
              start_offset: left,
              end_offset: tuple.start_offset,
              text: this.document_info.content.slice(left, tuple.start_offset),
              bg_color: "#fff",
            },
          )
          res.push(
            {
              id: tuple.id,
              start_offset: tuple.start_offset,
              end_offset: tuple.end_offset,
              // text: this.document_info.content.slice(
              //   tuple.start_offset,
              //   tuple.end_offset
              // ),
              text: tuple.entity,
              bg_color: this.getLabelById(tuple.label_id) ? this.getLabelById(tuple.label_id).bg_color : '#fff',
            },
          )
          left = tuple.end_offset
        }
      }
      if (left < this.document_info.content.length) {
        res.push(
          {
            id: '',
            start_offset: left,
            end_offset: this.document_info.content.length,
            text: this.document_info.content.slice(left),
            bg_color: "#fff",
          },
        )
      }
      // 加在这里可以 */
      this.overLinks()
      return res
    },
    entities() {
      let sorted_annotation = this.sortedEntityPositions
      let res = []
      if (sorted_annotation === null) {
        res.push(
          {
            label_type: '',
            text: '',
            bg_color: "#fff",
          },
        )
        return res
      }
      if (sorted_annotation.length >= 1) {
        for (let tuple of sorted_annotation) {
          res.push(
            {
              label_type: tuple.label_type,
              text: tuple.entity,
              bg_color: this.getLabelById(tuple.label_id) ? this.getLabelById(tuple.label_id).bg_color : '#fff',
            },
          )
        }
      }
      return res
    },
    relations() {
      let res = []
      if (this.document_info.relation) {
        for (let tuple of this.document_info.relation) {
          res.push(
            {
              source: tuple.source_entity,
              target: tuple.target_entity,
              label: tuple.label,
            },
          )
        }
      }
      return res
    },
    rotateIcon() {
      return this.is_collapsed ? 'rotate-icon' : ''
    },
  },
}
</script>
<style scoped>
.layout {
  border: 1px solid #d7dde4;
  background: #fff;
  position: relative;
  border-radius: 4px;
  overflow: hidden;
}
.ivu-card {
  font-size: 16px;
  text-align: justify;
}
.rotate-icon{
  transform: rotate(-90deg);
}
.demo-split{
  /* height: 110px; */
  border: 1px solid #dcdee2;
}
.demo-split-pane{
  padding: 10px;
}      
.tag {
  /*caption-side: -moz-user-select:none;
  -webkit-user-select: none; 
  -ms-user-select: none;
  -khtml-user-select: none; 
  -o-user-select:none;
  user-select:none; */
  cursor: pointer;
}
.tag1 {
  -moz-user-select: none; /* Firefox私有属性 */
  -webkit-user-select: none; /* WebKit内核私有属性 */
  -ms-user-select: none; /* IE私有属性(IE10及以后) */
  -khtml-user-select: none; /* KHTML内核私有属性 */
  -o-user-select: none; /* Opera私有属性 */
  user-select: none; /* CSS3属性 */
}
.tag:hover {
  background: #fff !important;
}
.source {
  border: 2px dashed blue !important;
  box-sizing: border-box;
}
.target {
  border: 2px dashed red !important;
}
</style>