<template>
    <div id="project_detail">
        <el-tabs type="card" v-model="activeName">
            <el-tab-pane label="执行任务列表" name="task">
                <el-table id='tasktable'
                          :data="task_data.result"
                          stripe
                          style="width: 100%;"
                >
                    <el-table-column label="爬取链接" width="600">
                                                <a>{{url}}</a>

                    </el-table-column>
                    <el-table-column prop="status_code" label="响应状态码">
                    </el-table-column>
                    <el-table-column prop="update_timestamp" label="爬取时间">
                    </el-table-column>
                </el-table>
                <div id="letPaginationBottom"></div>
                <el-pagination id="ele_pagination" @size-change="task_handleSizeChange"
                               @current-change="task_handleCurrentChange"
                               :current-page="task_currentPage" :page-sizes="[5, 9, 10]" :page-size="task_pagesize"
                               layout="total, sizes, prev, pager, next, jumper" :total="task_total">
                </el-pagination>
            </el-tab-pane>
            <el-tab-pane label="解析结果列表" name="result">
                <el-table id='resulttable'
                          :data="computed_result_data"
                          stripe
                          style="width: 100%;"
                >
                    <!--<el-table-column prop="url" label="爬取链接">-->
                    <!--</el-table-column>-->
                    <el-table-column prop="result" label="解析结果（如结果太长仅展示部分）">
                    </el-table-column>
                    <el-table-column prop="update_timestamp" label="解析时间">
                    </el-table-column>
                </el-table>
                <div></div>
                <el-pagination @size-change="result_handleSizeChange" @current-change="result_handleCurrentChange"
                               :current-page="result_currentPage" :page-sizes="[5, 9, 10]" :page-size="result_pagesize"
                               layout="total, sizes, prev, pager, next, jumper" :total="result_total">
                </el-pagination>
            </el-tab-pane>

        </el-tabs>

    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: 'Project',
        created() {
            this.fetchTaskData();
            this.fetchResultData();
        },
        data() {
            return {
                activeName: 'task',
                task_data: {
                    total_count: "",
                    count: "",
                    result: [],
                },
                task_currentPage: 1,
                task_pagesize: 9,
                result_data: {
                    total_count: "",
                    count: "",
                    result: [],
                },
                result_currentPage: 1,
                result_pagesize: 9,

            }
        },
        computed: {
            computed_result_data: function () {
                let tmp_list = [];
                for (let value of this.result_data.result) {
                    let result_item = JSON.stringify(value.result)
                    if (result_item.length > 66) {
                        result_item = result_item.slice(0, 66) + '...'
                    }
                    let tmp_value = {

                        result: result_item,
                        update_timestamp: value.update_timestamp,
                    }
                    tmp_list.push(tmp_value);
                }
                return tmp_list;
            },
            task_total: function () {
                return Number(this.task_data.total_count)
            },
            result_total: function () {
                return Number(this.result_data.total_count)
            },
        },
        methods: {
            fetchTaskData() {//获取爬取任务列表
                axios.get('/task/' + this.$route.params.project_id + '?limit=' + this.task_pagesize + '&page=' + this.task_currentPage).then((response) => {
                    console.log(response.data);
                    this.task_data = response.data;
                }).catch((response) => {
                    console.log(response);
                    this.$message.error({
                        message: "获取任务列表失败啦，检查下你的网络吧"
                    });
                });
            },
            fetchResultData() {//获取解析结果列表
                axios.get('/result/' + this.$route.params.project_id + '?limit=' + this.result_pagesize + '&page=' + this.result_currentPage).then((response) => {
                    console.log(response.data);
                    this.result_data = response.data;
                }).catch((response) => {
                    console.log(response);
                    this.$message.error({
                        message: "获取解析结果列表失败啦，检查下你的网络吧"
                    });
                });
            },
            task_handleSizeChange(val) {
                this.task_pagesize = val;
                this.fetchTaskData();
                console.log(`每页 ${val} 条`);
            },
            task_handleCurrentChange(val) {
                this.task_currentPage = val;
                this.fetchTaskData();
                console.log(`当前页: ${val}`);
            },
            result_handleSizeChange(val) {
                this.result_pagesize = val;
                this.fetchResultData();
                console.log(`每页 ${val} 条`);
            },
            result_handleCurrentChange(val) {
                this.result_currentPage = val;
                this.fetchResultData();

                console.log(`当前页: ${val}`);
            }
        },


    }
</script>

<style scoped>
</style>
