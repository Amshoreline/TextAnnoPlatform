<template>
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
</template>
<script>
import axios from 'axios'
import URL from '../../setting'

export default {
  data() {
    return {
      formItem: {
        name: null,
        shortcut: null,
        bg_color: 'default',
        // text_color: "#FFFFFF"
      },
      tag_color: ['magenta', 'red', 'volcano', 'orange', 'gold', 'yellow', 'lime', 'green', 'cyan', 'blue', 'geekblue', 'purple', 'default'],
    }
  },
  methods: {
    addLabel(callback) {
      if (this.formItem.name == null) {
        this.$Message.warning('您没有输入标签名')
        return
      }
      axios({
        method: "post",
        url: URL.create_label,
        data: this.formItem,
      })
      .then(() => {
        callback()
      })
    },
  },
}
</script>
