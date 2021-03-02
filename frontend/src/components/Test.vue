<template>
  <div class="layout">
    <Layout>
      <Header :style="{position: 'fixed', width: '100%', background:'#fff', height:'62px'}" style="z-index:1000">
        <Menu mode="horizontal" theme="light" :active-name="($route.path).split('/')[1][0]">
          <div class="layout-nav">
              <MenuItem name="t" to='/text'>
                <!-- <router-link to="/text" tag="div"> -->
                  <Icon type="ios-navigate"></Icon>&nbsp;&nbsp;文本管理&nbsp;&nbsp;
                <!-- </router-link> -->
              </MenuItem>
              <MenuItem name="l" to='/label'>
                <!-- <router-link to="/label" tag="div"> -->
                  <Icon type="ios-keypad"></Icon>&nbsp;&nbsp;标签管理&nbsp;&nbsp;
                <!-- </router-link> -->
              </MenuItem>
              <MenuItem name="a" to='/ann?page=1&index=0'>
                <!-- <router-link to="/ann" tag="div"> -->
                  <Icon type="ios-analytics"></Icon>&nbsp;&nbsp;文本标注&nbsp;&nbsp;
                <!-- </router-link> -->
              </MenuItem>
              <Button style="position:fixed;right:50px;top:15px" @click="showDrawer = true"><Icon type="ios-help-circle-outline" />&nbsp;帮助&nbsp;</Button>
          </div>
        </Menu>
      </Header>
      <Content id='main' class="main" :style="{margin: '76px 12px 0 12px',paddingLeft:'10px',paddingRight:'10px', background: '#fff'}">
        <router-view/>
      </Content>
      <Footer class="layout-footer-center">2021-2027 &copy; carpe diem</Footer>
    </Layout>
    <Drawer :draggable='true'  width="640" v-model="showDrawer" title='使用引导'>
      <p :style="pStyle">文本管理</p>
      <!-- <Divider>文本管理</Divider> -->
      <div class="demo-drawer-profile">
        <List>
          <ListItem><Icon type="ios-arrow-dropright" /> &nbsp;
          多种方式上传文本，其中批量上传需要注意文件的格式</ListItem>
          <ListItem><Icon type="ios-arrow-dropright" /> &nbsp;
          多种方式导出系统数据，包括文本和标注</ListItem>
          <ListItem><Icon type="ios-arrow-dropright" /> &nbsp;
          实现文本的编辑和删除</ListItem>
        </List>
      </div>
      <br />
      <p :style="pStyle">标签管理</p>
      <div class="demo-drawer-profile">
        <List>
          <ListItem><Icon type="ios-arrow-dropright" /> &nbsp;
          可以创建、编辑、删除标签，自定义标签的快捷键</ListItem>
          <ListItem><Icon type="ios-arrow-dropright" /> &nbsp;
          标签拥有美观、丰富的样式
          </ListItem>&nbsp;&nbsp;&nbsp;&nbsp;
          <Row type="flex">
            <Col>
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              <Tag class="tag" color="magenta" size='medium'>magenta</Tag>&nbsp;&nbsp;
              <Tag class="tag" color="red" size='medium'>red</Tag>&nbsp;&nbsp;
              <Tag class="tag" color="volcano" size='medium'>volcano</Tag>&nbsp;&nbsp;
              <Tag class="tag" color="orange" size='medium'>orange</Tag>&nbsp;&nbsp;
              <Tag class="tag" color="gold" size='medium'>gold</Tag>&nbsp;&nbsp;
              <Tag class="tag" color="yellow" size='medium'>yellow</Tag><br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              <Tag class="tag" color="lime" size='medium'>lime</Tag>&nbsp;&nbsp;
              <Tag class="tag" color="green" size='medium'>green</Tag>&nbsp;&nbsp;
              <Tag class="tag" color="cyan" size='medium'>cyan</Tag>&nbsp;&nbsp;
              <Tag class="tag" color="blue" size='medium'>blue</Tag>&nbsp;&nbsp;
              <Tag class="tag" color="geekblue" size='medium'>geekblue</Tag>&nbsp;&nbsp;
              <Tag class="tag" color="purple" size='medium'>purple</Tag>
            </Col>
          </Row>
        </List>
      </div>
      <br />
      <p :style="pStyle">实体标注</p>
      <div class="demo-drawer-profile">
        <List>
            <ListItem><Icon type="ios-arrow-dropright" /> &nbsp;
            可以使用自定义的<font color='blue'>快捷键</font>标注实体，<font color='blue'>右键</font>标注可以删除，方便快捷</ListItem>
            <ListItem><Icon type="ios-arrow-dropright" /> &nbsp;
            可以先使用<font color='blue'>预测实体</font>功能实现自动标注</ListItem>
            <ListItem><Icon type="ios-arrow-dropright" /> &nbsp;
            一键清除当前文本的实体标注</ListItem>
        </List>
      </div>
      <br />
      <p :style="pStyle">关系标注</p>
      <div class="demo-drawer-profile">
        <List>
            <ListItem><Icon type="ios-arrow-dropright" /> &nbsp;
            点击已标注的实体，<font color='blue'>蓝色框</font>表示源，<font color='red'>红色框</font>表示目标</ListItem>
            <ListItem><Icon type="ios-arrow-dropright" /> &nbsp;
            点击【增加关系】可以实现二者的关系标注</ListItem>
            <ListItem><Icon type="ios-arrow-dropright" /> &nbsp;
            点击连接线上的标签可以修改关系标签</ListItem>
            <ListItem><Icon type="ios-arrow-dropright" /> &nbsp;
            点击连接线可以实现删除关系</ListItem>
            <ListItem><Icon type="ios-arrow-dropright" /> &nbsp;
            可以先使用<font color='blue'>预测关系</font>功能实现自动标注</ListItem>
            <ListItem><Icon type="ios-arrow-dropright" /> &nbsp;
            显示实体关系图谱</ListItem>
        </List>
      </div>
      <br />
      <p :style="pStyle">关于我们</p>
      <div class="demo-drawer-profile about">
        <Row>
            Email：carpe@diem.com
        </Row>
        <Row>
            Phone Number：+86 18888888888
        </Row>
        <Row>
            GitHub：<a href="#" target="_blank">https://github.com</a>
        </Row>
      </div>
    </Drawer>
  </div>
</template>

<script lang='ts'>
export default {
  data() {
    return {
      showDrawer: false,
      pStyle: {
          fontSize: '18px',
          color: 'rgba(0,0,0,0.85)',
          lineHeight: '24px',
          display: 'block',
          marginBottom: '16px',
      },
    }
  },
}
</script>

<style scoped>
.layout{
  border: 1px solid #d7dde4;
  background: #f5f7f9;
  position: relative;
  border-radius: 4px;
  overflow: hidden;
}
.layout-nav{
  width: 396px;
  margin: 0 auto;
}
.layout-footer-center{
  text-align: center;
}
.tag {
  -moz-user-select:none; /* Firefox私有属性 */
  -webkit-user-select:none; /* WebKit内核私有属性 */
  -ms-user-select:none; /* IE私有属性(IE10及以后) */
  -khtml-user-select:none; /* KHTML内核私有属性 */
  -o-user-select:none; /* Opera私有属性 */
  user-select:none; /* CSS3属性 */
  cursor: pointer;
}
.demo-drawer-profile{
  font-size: 16px;
}
.about{
  font-family: 'Times New Roman', Times, serif;
  letter-spacing: 1px;
}
</style>