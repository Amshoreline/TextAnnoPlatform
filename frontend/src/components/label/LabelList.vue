<template>
  <div>
    <Row style="height:50px" type="flex" align="middle">&nbsp;&nbsp;&nbsp;
      <Col span="1.1">
        <Button @click="showAddModal = true">新建标签</Button>
      </Col>&nbsp;&nbsp;
      <Col>
      <Button @click="exportData()"><Icon type="ios-download-outline"></Icon>&nbsp;导出为 csv 文件</Button>
      </Col>
    </Row>
    <Table highlight-row :columns="columns1" :data="data1" ref="table"></Table>

    <Modal v-model="showEditModal" title="编辑标签" @on-ok="editLabelOk">
      <Form :model="editData" :label-width="80">
        <FormItem label="标签编号">
          <Input disabled v-model="editData.id"/>
        </FormItem>
        <FormItem label="标签名">
          <Input v-model="editData.name" />
        </FormItem>
        <FormItem label="快捷键">
          <Input v-model="editData.shortcut" />
        </FormItem>
        <FormItem label="标签颜色">
          <!-- <ColorPicker v-model="editData.bg_color" size="default"/> -->
          <Select v-model="editData.bg_color" style="width:200px">
        <Option v-for="item in tag_color" :value="item" :key="item">{{ item }}</Option>
      </Select>
        </FormItem>
        <!-- <FormItem label="Text Color">
          <ColorPicker v-model="editData.text_color" size="default"/>
        </FormItem> -->
      </Form>
    </Modal>

    <!-- <Modal v-model="showAddModal" title="新增标签" @on-ok="addLabelOk">
      <CreateLabel ref="CreateLabel"></CreateLabel>
    </Modal> -->

    <Modal v-model="showAddModal" title="新增标签" @on-ok="addLabel">
      <Form :model="formItem" :label-width="100">
        <FormItem label="标签名">
          <Input v-model="formItem.name" placeholder="输入标签名"/>
        </FormItem>
        <FormItem label="快捷键">
          <Input v-model="formItem.shortcut" placeholder="由 'alt' + 您所输入的键组成" />
        </FormItem>
        <FormItem label="标签颜色">
          <!-- <ColorPicker v-model="formItem.bg_color" size="default"/> -->
          <Select v-model="formItem.bg_color" style="width:200px">
            <Option v-for="item in tag_color" :value="item" :key="item">{{ item }}</Option>
          </Select>
        </FormItem>
      </Form>
    </Modal>

    <BackTop></BackTop>
  </div>

</template>
<script>
import axios from 'axios'
// import CreateLabel from "./CreateLabel"
import URL from '../../setting'

export default {
  data() {
    return {
      showEditModal: false,
      showAddModal: false,
      queryData: {},
      columns1: [
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
            // const text_color = row.text_color
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
      data1: [],
      tag_color: ['magenta', 'red', 'volcano', 'orange', 'gold', 'yellow', 'lime', 'green', 'cyan', 'blue', 'geekblue', 'purple', 'default'],
      editData: {
        id: "",
        name: "",
        shortcut: "",
        bg_color: "",
        text_color: "",
      },
      formItem: {
        name: null,
        shortcut: null,
        bg_color: 'default',
        // text_color: "#FFFFFF"
      },
    }
  },
  mounted() {
    this.search()
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
            this.data1 = response.data.results
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
      if (this.formItem.name == null) {
        this.$Message.warning('您没有输入标签名')
        return
      }
      axios({
        method: "post",
        url: URL.create_label,
        data: this.formItem,
      })
      .then(response => {
        if (response.status === 200) {
          this.$Message.success(response.data)
          this.search()
        }
      })
      .catch(error => {
        this.$Message.error(error.toString())
      })
    },
    editLabel(row) {
      this.editData = row
      this.showEditModal = true
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
    saveLabel() {
      axios
        .post(URL.update_label, this.editData)
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
    // addLabelOk() {
    //   this.$refs.CreateLabel.addLabel(this.search)
    // },
  },
  // components: {
  //   CreateLabel,
  // },
}
</script>