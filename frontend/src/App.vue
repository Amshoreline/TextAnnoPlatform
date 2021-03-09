<template>
	<div id='app'>
		<router-view/>
	</div>
</template>

<script>
import zh_CN from 'ant-design-vue/lib/locale-provider/zh_CN'
import InputPanel from './components/InputPanel.vue'
import MessageBox from './components/MessageBox.vue'
export default {
	name: 'app',
	data() {
		return {
			zh_CN,
		}
	},
	mounted(){
		this.$Message.config({
			top: 100,
			duration: 2,
    });
	},
	components: {
		MessageBox,
		InputPanel,
	},
}
</script>