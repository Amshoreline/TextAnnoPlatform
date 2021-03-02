<template>
  <div>
    <Menu mode="horizontal" theme="light" active-name="1">
      <Submenu name="1">
        <template slot="title">
          <Icon type="md-cloud-upload" />
          上传文本
        </template>
          <MenuItem name="1-1" @click.native="showAddText1 = true">新建文本上传</MenuItem>
          <MenuItem name="1-2" @click.native="showAddText2 = true">上传多个文件</MenuItem>
          <MenuItem name="1-3" @click.native="showAddText3 = true">批量上传 ( json )</MenuItem>
      </Submenu>
      <Submenu name="2">
        <template slot="title">
          <Icon type="md-download"></Icon>
          导出数据
        </template>
          <MenuItem @click.native="export_data('text')" name="2-1">导出文本</MenuItem>
          <MenuItem @click.native="export_data('ann')" name="2-2">导出实体标注</MenuItem>
          <MenuItem @click.native="export_data('ann_r')" name="2-3">导出关系标注</MenuItem>
          <MenuItem @click.native="export_data('ann_b')" name="2-4">导出实体和关系标注</MenuItem>
          <MenuItem @click.native="export_data('data')" name="2-5">导出所有信息</MenuItem>
      </Submenu>
      
      <div style="position:absolute;right:0">
      <Button @click="doDeleteAll">清空列表</Button>&nbsp;
      <Button @click="handleSelectAll(true)">设置全选</Button>&nbsp;
      <Button @click="handleSelectAll(false)">取消全选</Button>
      </div>
    </Menu>
    <br>

    <Table highlight-row :columns="columns1" :data="nowData" ref="selection">
      <template slot-scope="{ row }" slot="is_checked">
        <span v-if="row.is_checked">
          <Icon color='#33a060' type="md-checkmark" />
        </span>
        <span v-else>
          <Icon color='red' type="md-close" />
        </span>
      </template>
    </Table>

    <Row type="flex" align="middle" style="height:60px;float:right;margin-right:60px">
    <Page show-total :total="page_options.total" :page-size="page_options.page_size" :current="page_options.page" show-elevator @on-change="pageChange"></Page>
    </Row>

    <Modal v-model="showEditModal" title="编辑文本" @on-ok="ok" width="666">
      <Row justify="center">
        <Alert type="warning" show-icon closable>
          注意：如果修改了文本内容，会清空该文本的标注信息，非必要不建议修改文本内容</Alert>
      </Row>
      <Form :model="editData" :label-width="80">
        <FormItem label="文本编号">
          <Input disabled v-model="editData.id"/>
        </FormItem>
        <FormItem label="文本标题">
          <Input v-model="editData.title"/>
        </FormItem>
        <FormItem label="文本内容">
          <Input v-model="editData.content" type="textarea" :autosize="{minRows: 18,maxRows: 18}"/>
        </FormItem>
      </Form>
    </Modal>
    <Modal v-model="showAddText1" title="新建文本上传" @on-ok="create_text" width="666">
      <Form :model="addText" :label-width="56" >
        <Col span="23">
        <FormItem label="标题">
          <Input v-model="addText.title"/>
        </FormItem>
        </Col>
        <Col span="23">
        <FormItem label="内容">
          <Input v-model="addText.content" type="textarea" :autosize="{minRows: 18,maxRows: 18}"/>
        </FormItem>
        </Col>
      </Form>
    </Modal>
    <Modal v-model="showAddText2" title="上传多个文件" width="666">
      <Alert show-icon>
        文件格式
        <template slot="desc">只支持上传 txt 文件</template>
      </Alert>
      <Upload
        multiple
        type="drag"
        :action="import_data_url"
        :data="post_data"
        :format="['txt']"
        :on-format-error="handleFormatError"
        :on-success="handleSuccess1"
        :on-error="handleError"
      >
        <div style="padding: 20px 0">
          <Icon type="ios-cloud-upload" size="52" style="color: #3399ff"></Icon>
          <p>Click or drag files here to upload</p>
        </div>
      </Upload>
    </Modal>
    <Modal v-model="showAddText3" title="批量上传(json)" width="666">
      <Alert show-icon>
        文本格式
        <template slot="desc"><p style="font-family: 'Times New Roman'">文件内容格式为 json，下面可以输入每个文本标题(可选) 和内容的 key <br>
        例如每个文本都有标题和内容，对应的 key 为 "title" 和 "content"，则 json 中至少要包含这两个 key，如以下两种形式的 json 都可以：<br>
        <strong>[{<font color='red'>"title"</font>: "abc", <font color='red'>"content"</font>: "aabbcc"}, {<font color='red'>"title"</font>: "def"<font color='red'>, "content"</font>: "ddeeff"}]</strong><br>
        <strong>[{<font color='red'>"title"</font>: "abc", <font color='red'>"content"</font>: "aabbcc", "any": "...", "...": "..."}]</strong><br>
        只支持上传 txt 文件</p></template>
      </Alert>
      <Card :bordered="false">
        <p slot="title">输入每个文本所拥有 key，没有标题则无需输入</p>
        <div style="font-family: 'Times New Roman'">
        文本标题 <strong>key</strong> ：
        <Input v-model="post_data.title" placeholder="若无标题请勿输入" clearable style="width: 180px" />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <font color='red'>*</font>文本内容 <strong>key</strong> ：
        <Input v-model="post_data.content" placeholder="请输入文本内容的 key" clearable style="width: 180px" /></div>
      </Card>
      <Upload
        type="drag"
        :action="import_data_json_url"
        :data="post_data"
        :format="['txt','json']"
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
import axios from 'axios'
import URL from '../../setting'

export default {
  data() {
    return {
      import_data_url: URL.import_data,
      import_data_json_url: URL.import_data_json,
      post_data: {
        title: '',
        content: 'content',
      },
      showEditModal: false,
      showAddText1: false,
      showAddText2: false,
      showAddText3: false,
      columns1: [
        // {
        //   type: 'selection',
        //   width: 60,
        //   align: 'center',
        // },
        {
          title: '',
          width: 80,
          align: 'center',
          render: (h, params) => {
            return h('span', params.index + (this.page_options.page - 1) * this.page_options.page_size + 1)
          },
        },
        {
          title: '是否标注',
          width: 100,
          slot: 'is_checked',
          align: 'center',
        },
        // {
        //   title: "ID",
        //   key: "id",
        //   width: 185,
        // },
        {
          title: "标题",
          key: "title",
          width: 190,
        },
        {
          title: "文本内容",
          key: "content",
          tooltip: true,
          minWidth: 400,
        },
        {
          title: '创建时间',
          key: 'create_time',
          width: 190,
        },
        {
          title: '修改时间',
          key: 'update_time',
          width: 190,
        },
        {
          title: "操作",
          key: "action",
          width: 250,
          // fixed: 'right',
          // align: "center",
          // 编辑和删除按钮
          render: (h, params) => {
            return h("div", [
              h(
                "Button",
                {
                  props: {
                    type: "success",
                    size: "default",
                  },
                  style: {
                    marginRight: "7px",
                  },
                  on: {
                    click: () => {
                      this.$router.push(
                        {
                          name: 'ann',
                          query: {
                            page: `${this.page_options.page}`,
                            index: `${params.index}`,
                          },
                        },
                      )
                      // console.log(`${params.index}`);
                    },
                  },
                },
                "标注",
              ),
              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "default",
                  },
                  style: {
                    marginRight: "7px",
                  },
                  on: {
                    click: () => {
                      this.editDocument(params.row)
                    },
                  },
                },
                "编辑",
              ),
              h(
                "Button",
                {
                  props: {
                    type: "error",
                    size: "default",
                  },
                  on: {
                    click: () => {
                      this.doDelete(params.row)
                    },
                  },
                },
                "删除",
              ),
            ])
          },
        },
      ],
      data1: [],
      nowData: [],
      page_options: {
        total: 0,
        page: 1,
        page_size: 10,
      },
      addText: {
        title: "",
        content: "",
      },
      editData: {
        id: "",
        title: "",
        content: "",
        create_time: "",
        update_time: "",
        annotations: [],
      },
      count: 0,
    }
  },
  mounted() {
    this.search()
  },
  methods: {
    handleSuccess(response) {
      this.$Message.success("成功上传 " + response.data + ' 个文本')
      this.search()
    },
    handleSuccess1(response) {
      this.$Message.success("上传成功")
      this.search()
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
    export_data(type) {
      this.$Loading.start()
      axios
        .get(
          URL.export + `_${type}`,
          {
            responseType: "text",
          },
        )
        .then(response => {
          let time = this.formatDate()
          const fileName = `${type}_${time}.txt`
          let fileURL = window.URL.createObjectURL(new Blob([JSON.stringify(response.data, null, 2)]))
          let fileLink = document.createElement("a")
          fileLink.href = fileURL
          fileLink.setAttribute(
            "download",
            fileName,  // 不知道为什么时间的分隔符变了
          )
          document.body.appendChild(fileLink)
          fileLink.click()
          this.$Loading.finish()
        }).catch(error => {
          this.$Loading.error()
        })
    },
    formatDate() {
      let date = new Date()
      let year = date.getFullYear()
      let month = date.getMonth() + 1 // 月份是从0开始的
      let day = date.getDate()
      let hour = date.getHours()
      let min = date.getMinutes()
      let sec = date.getSeconds()
      let newTime = year + '-' +
        month + '-' +
        day + ' ' +
        hour + ':' +
        min + ':' +
        sec
      return newTime
    },
    // 新建文本 */
    create_text() {
      if (this.addText.title == "") {
        return
      }
      axios
        .post(
          URL.create_text,
          {
            'title': this.addText.title,
            'content': this.addText.content,
          },
        )
        .then(response => {
          this.$Message.info(response.data)
          this.search()
        })
        .catch(error => {
          alert(error)
        })
      this.addText = {
        title: "",
        content: "",
      }
    },
    // 文本全选 */
    handleSelectAll(status) {
      this.$refs.selection.selectAll(status)
    },
    clearAll() {
      axios
      .get(URL.delete_text + `?id=all`)
      .then(response => {
        if (response.status === 200) {
          this.$Message.success(response.data)
          this.search()
        }
      })
      .catch(error => {
        this.$Message.error(error.toString())
      })
      .then(() => {})
    },
    // 获取文本列表 */
    search() {
      this.$Loading.start()
      axios
        .get(URL.get_text_list)
        .then(response => {
          if (response.status === 200) {
            this.data1 = response.data.results
            this.page_options.total = response.data.count
            // 循环展示页面刚加载时需要的数据条数
            this.nowData = []
            let begin = (this.page_options.page - 1) * this.page_options.page_size
            for (let i = 0; i < this.page_options.page_size && i + begin < this.page_options.total; i++) {
              this.nowData.push(this.data1[i + begin])
            }
          }
          this.$Loading.finish()
        })
        .catch(error => {
          this.$Loading.error()
          this.$Message.error(error.toString())
        })
        .then(() => {})
    },
    // 换页 */
    pageChange(index) {
      this.page_options.page = index
      // 需要显示开始数据的index,(因为数据是从0开始的，页码是从1开始的，需要-1)
      let _start = (index - 1) * this.page_options.page_size
      // 需要显示结束数据的index
      let _end = index * this.page_options.page_size
      // 截取需要显示的数据
      this.nowData = this.data1.slice(_start, _end)
    },
    // 编辑文本 */
    editDocument(row) {
      this.editData = row
      this.showEditModal = true
    },
    // 删除文本 */
    deleteDocument(row) {
      axios
        .get(URL.delete_text + `?id=${row.id}`)
        .then(response => {
          if (response.status === 200) {
            this.$Message.success(response.data)
            this.search()
          }
        })
        .catch(error => {
          this.$Message.error(error.toString())
        })
        .then(() => {})
    },
    // 是否确认删除 */
    doDelete(row) {
      this.$Modal.confirm({
        content: `确认删除文本<font color="blue"> ${row.title}</font> ？`,
        onOk: this.deleteDocument.bind(null, row),
      })
    },
    doDeleteAll() {
      this.$Modal.confirm({
        content: `确认删除所有文本吗？`,
        onOk: this.clearAll.bind(null),
      })
    },
    // 保存文本 */
    ok() {
      this.saveDocument()
    },
    // 保存文本 */
    saveDocument() {
      axios
        .post(URL.update_text, this.editData)
        .then(response => {
          if (response.status === 200) {
            this.$Message.info(response.data)
            this.search()
          }
        })
        .catch(error => {
          this.$Message.error(error.toString())
        })
        .then(() => {})
    },
  },
}
</script>
<style scoped>
.demo-drawer-profile{
  font-size: 16px;
}

</style>