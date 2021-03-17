<template>
  <div>
    <Row style="height:50px" type="flex" align="middle">&nbsp;&nbsp;&nbsp;
      <Col span="1.1">
        <Button @click="show_add_modal = true">新建标签</Button>
      </Col>&nbsp;&nbsp;
      <Col>
      <Button @click="exportData()"><Icon type="ios-download-outline"></Icon>&nbsp;导出为 csv 文件</Button>
      </Col>
    </Row>
    
    <Table highlight-row :columns="columns" :data="data" ref="table"></Table>

    <Modal v-model="show_edit_modal" title="编辑标签" @on-ok="editLabelOk">
      <Form :model="edit_data" :label-width="80">
        <FormItem label="标签编号">
          <Input disabled v-model="edit_data.id"/>
        </FormItem>
        <FormItem label="标签名">
          <Input v-model="edit_data.name" />
        </FormItem>
        <FormItem label="快捷键">
          <Input v-model="edit_data.shortcut" readonly="readonly" placeholder="" style="width: 200px; margin-right: 10px"/>
          <Button type="primary" @click="updateSK">点击设置快捷键</Button>
        </FormItem>
        <FormItem label="标签颜色">
          <!-- <ColorPicker v-model="edit_data.bg_color" size="default"/> -->
          <Select v-model="edit_data.bg_color" style="width:200px">
        <Option v-for="item in tag_color" :value="item" :key="item"
          :style="{background: tag_color_map[item].background, color: tag_color_map[item].color, borderWidth: '1px', borderStyle: 'solid', borderColor: tag_color_map[item].borderColor, lineHeight: '18px', marginBottom: '3px', textAlign: 'center'}"
        >
          {{ item }}
        </Option>
      </Select>
        </FormItem>
        <!-- <Form_item label="Text Color">
          <ColorPicker v-model="edit_data.text_color" size="default"/>
        </Form_item> -->
      </Form>
    </Modal>

    <!-- <Modal v-model="show_add_modal" title="新增标签" @on-ok="addLabelOk">
      <CreateLabel ref="CreateLabel"></CreateLabel>
    </Modal> -->

    <Modal v-model="show_add_modal" title="新增标签" @on-ok="addLabel">
      <Form :model="form_item" :label-width="70" :style={}>
        <FormItem label="标签名">
          <Input v-model="form_item.name" placeholder="输入标签名"/>
        </FormItem>
        <FormItem label="快捷键">
          <Input v-model="form_item.shortcut" readonly="readonly" placeholder="" style="width: 200px; margin-right: 10px"/>
          <Button type="primary" @click="updateSK">点击设置快捷键</Button>
        </FormItem>
        <FormItem label="标签颜色">
          <!-- <ColorPicker v-model="form_item.bg_color" size="default"/> -->
          <Select v-model="form_item.bg_color" style="width:200px">
            <Option v-for="item in tag_color" :value="item" :key="item"
              :style="{background: tag_color_map[item].background, color: tag_color_map[item].color, borderWidth: '1px', borderStyle: 'solid', borderColor: tag_color_map[item].borderColor, lineHeight: '18px', marginBottom: '3px', textAlign: 'center'}">
              {{ item }}
            </Option>
          </Select>
        </FormItem>
      </Form>
    </Modal>

    <Modal v-model="show_short_key" @on-ok="setShortKey">
      <div style="text-align: center;">
        请直接键入您想设置的快捷键<br/> (只支持 单键 或 双组合键)<br/><br/>
        <div style="font-size: 20px; min-height: 50px">{{shortkey}}</div>
      </div>
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
      show_edit_modal: false,
      show_add_modal: false,
      show_short_key: false,
      last: '',
      cur: '',
      shortkey: '',
      input_short_key: '',
      tag_color: ['magenta', 'red', 'volcano', 'orange', 'gold', 'yellow', 'lime', 'green', 'cyan', 'blue', 'geekblue', 'purple', 'default'],
      tag_color_map: {
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
      columns: [
        // {
        //   type: 'selection',
        //   width: 60,
        //   align: 'center',
        // },
        {
          title: '',
          width: 70,
          render: (h, params) => {
            return h('span', params.index + 1)
          },
          align: 'center',
        },
        {
          title: "标签名",
          key: "name",
          sortable: true,
          minWidth: 220,
        },
        {
          title: "示例",
          key: "example",
          minWidth: 220,
          render: (h, params) => {
            const row = params.row
            // const bg_color = row.bg_color
            return h(
              "Tag",
              {
                props: {
                  color: row.bg_color,
                  size: 'medium',
                },
              },
              row.name,
            )
          },
        },
         {
          title: "快捷键",
          key: "shortcut",
          sortable: true,
          width: 100,
        },
        {
          title: "颜色",
          key: "bg_color",
          sortable: true,
          width: 120,
        },
        {
          title: '创建时间',
          key: 'create_time',
          sortable: true,
          width: 220,
        },
        {
          title: '修改时间',
          key: 'update_time',
          sortable: true,
          width: 220,
        },
        {
          title: "操作",
          key: "action",
          width: 200,
          // fixed: 'right',
          // 编辑和删除按钮
          render: (h, params) => {
            return h("div", [
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
                      this.editLabel(params.row)
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
      data: [],
      edit_data: {
        id: "",
        name: "",
        shortcut: "",
        bg_color: "",
      },
      form_item: {
        name: null,
        shortcut: null,
        bg_color: 'default',
      },
    }
  },
  mounted() {
    this.search()
    let _this = this
    document.onkeydown = (e) => {
      if (_this.show_edit_modal || _this.show_add_modal) {
        if (_this.show_short_key) {
          e.preventDefault()
          let sk = e.key.toLowerCase()
          switch (sk) {
            case 'control': sk = 'ctrl'; break
            case 'command': sk = 'ctrl'; break
          }
          // 长按返回
          if (_this.last == sk || _this.cur == sk) {
            return
          }
          // 输入组合键
          if ((e.altKey || e.shiftKey || e.ctrlKey) && /^[0-9a-zA-Z]$/.test(sk)) {
            if (e.altKey) {
              _this.last = 'alt+'
            } else if (e.shiftKey) {
              _this.last = 'shift+'
            } else {
              _this.last = 'ctrl+'
            }
            _this.cur = sk
          } else if (/^[0-9a-zA-Z]$/.test(sk)) { // 非组合 0-9 a-z
            _this.last = sk
            _this.cur = ''
          }
          _this.shortkey = _this.last + _this.cur
        }
      }
    }
  },
  methods: {
    // 导出原始数据 */
    exportData() {
      this.$refs.table.exportCsv({
        filename: '标签列表',
      })
    },
    search() {
      this.$Loading.start()
      axios
        .get(URL.get_label_list)
        .then(response => {
          if (response.status === 200) {
            this.data = response.data.results
            this.$Loading.finish()
          }
        })
        .catch(error => {
          this.$Loading.error()
          this.$Message.error(error.toString())
        })
        .then(() => {})
    },
    addLabel() {
      if (this.form_item.name == null) {
        this.$Message.warning('您没有输入标签名')
        return
      }
      axios({
        method: "post",
        url: URL.create_label,
        data: this.form_item,
      })
      .then(response => {
        if (response.status === 200) {
          this.$Message.success(response.data)
          this.search()
          this.form_item = {
            name: null,
            shortcut: null,
            bg_color: 'default',
          }
        }
      })
      .catch(error => {
        this.$Message.error(error.toString())
      })
    },
    // 点击设置快捷键
    updateSK() {
      this.show_short_key = true
      if (this.show_add_modal) {
        this.shortkey = this.form_item.shortcut
      } else {
        this.shortkey = this.edit_data.shortcut
      }
    },
    // 检查快捷键冲突
    checkShortKey(sk) {
      let label_list = this.data
      console.log(label_list)
      for (let i = 0, l = label_list.length; i < l; ++i) {
        if (sk == label_list[i].shortcut) {
          return false
        }
      }
      return true
    },
    setShortKey() {
      this.last = ''
      this.cur = ''
      if (!this.checkShortKey(this.shortkey)) {
        this.$Message.warning('快捷键冲突')
        return
      }
      if (this.show_add_modal) {
        this.form_item.shortcut = this.shortkey
      } else {
        this.edit_data.shortcut = this.shortkey
      }
    },
    saveLabel() {
      axios
        .post(URL.update_label, this.edit_data)
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
    editLabel(row) {
      // 这里不能直接 = row
      this.edit_data = {
        id: row.id,
        name: row.name,
        shortcut: row.shortcut,
        bg_color: row.bg_color,
        // text_color: row.text_color,
      }
      this.show_edit_modal = true
    },
    deleteLabel(row) {
      axios
        .get(URL.delete_label + `?id=${row.id}`)
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
    doDelete(row) {
      this.$Modal.confirm({
        content: `确认删除标签 <font color="blue">${row.name}</font> ？`,
        onOk: this.deleteLabel.bind(null, row),
      })
    },
    editLabelOk() {
      this.saveLabel()
    },
  },
}
</script>