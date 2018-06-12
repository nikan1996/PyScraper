<template>
    <div>
        <el-collapse v-model="activeNames" @change="handleChange">
            <el-collapse-item title="项目数量" name="1">
                <div>目前总共拥有{{statistics.project_num}}个项目。</div>
            </el-collapse-item>
            <el-collapse-item title="爬取数据总量" name="2">
                <div>目前总共爬取了{{statistics.all_result_num}}条数据。</div>
            </el-collapse-item>
            <el-collapse-item title="访问页面总量" name="3">
                <div>目前总共爬取了{{statistics.all_task_num}}个页面。</div>
            </el-collapse-item>
            <el-collapse-item title="显示正在运行的项目数量" name="4">
                <div>目前正在运行的项目数量为{{statistics.running_project_num}}。</div>
            </el-collapse-item>
        </el-collapse>
    </div>
</template>
<script>
    import axios from 'axios';

    export default {
        name: "Index",
        created() {
            this.fetchData();
        },
        data() {
            return {
                activeNames: ['1', '2', '3', '4'],
                statistics: {
                    project_num: '',
                    all_result_num: '',
                    all_task_num: '',
                    running_project_num: '',
                }
            };
        },
        methods: {
            fetchData() {
                axios.get('/statistics').then((response) => {
                    this.statistics = response.data;
                }).catch((response) => {
                    console.log(response);
                    this.$message.error({
                        message: "获取统计情况失败啦，检查下你的网络吧"
                    });
                });
            },
            handleChange(val) {
                console.log(val);
            }
        }
    }
</script>