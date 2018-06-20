<template>
    <div>
        <el-form>
            <label>引用地址</label>
            <br>
            <br>
            <a :href="location_data.previous_url" target="_blank">{{location_data.previous_url}}</a>
            <br>

            <br>

            <label>源码定位</label>
            <br>

            <div id='code_text'>

                {{location_data.head}}
                <div v-html="location_data.body"></div>
                {{location_data.foot}}
            </div>
        </el-form>
    </div>
</template>

<script>
    import ElForm from "../../../node_modules/element-ui/packages/form/src/form.vue";
    import axios from 'axios';

    export default {
        props: ['result_id', 'location_type'],
        name: 'code_location',
        created() {
            this.fetch_code_location();
        },
        data() {
            return {
                result_id: '',
                location_type: 'cache',
                location_data: {'previous_url': '', 'content': ''},
            }
        },
        computed: {},
        methods: {
            fetch_code_location() {
                let url = this.$route.fullPath;
                axios.get(url).then((response) => {
                    console.log(response.data);
                    this.location_data = response.data;
                }).catch((response) => {
                    console.log(response);
                    this.$message.error({
                        message: "获取定位源码失败啦，检查下你的网络吧"
                    });
                });
            }
        },


    }
</script>

<style scoped>
    #code_text {
        width: 900px;
        height: 480px;
        border: 1px solid #ccc;
        padding: 5px;
        overflow: auto;
    }

</style>
