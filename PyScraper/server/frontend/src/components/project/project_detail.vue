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
                        <template slot-scope="scope"><a class="link" target="_blank"
                                                        :href="scope.row.url">{{scope.row.url}}</a></template>

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
            <el-tab-pane label="解析结果列表" name="result" v-if="project_type!=='gov'">
                <el-table id='resulttable'
                          :data="computed_result_data"
                          stripe
                          style="width: 100%;"
                >
                    <!--<el-table-column prop="url" label="爬取链接">-->
                    <!--</el-table-column>-->
                    <el-table-column label="解析结果（如结果太长仅展示部分, 鼠标悬浮在结果行查看全部）">
                        <template slot-scope="scope">
                            <el-popover trigger="hover" placement="bottom-start" width="400">
                                <p class="popword">{{scope.row.full_result}}</p>
                                <div slot="reference" class="name-wrapper">
                                    <p>{{ scope.row.result }}</p>
                                </div>
                            </el-popover>
                        </template>
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

            <el-tab-pane label="政府内容检索结果" name="gov_result" v-if="project_type==='gov'">
                <el-table id='gov_resulttable'
                          :data="computed_gov_result_data"
                          stripe
                          style="width: 100%;">
                    <el-table-column label="网站链接" width="600">
                        <template slot-scope="scope">
                            <el-popover trigger="hover" placement="bottom-start" width="400">
                                <p class="popword">{{scope.row.full_url}}</p>
                                <div slot="reference" class="name-wrapper">
                                    <a class="link" target="_blank"
                                       :href="scope.row.short_url">{{scope.row.short_url}}</a>

                                </div>
                            </el-popover>
                        </template>
                    </el-table-column>
                    <el-table-column prop="reason" label="理由">
                    </el-table-column>

                    <el-table-column prop="update_timestamp" label="检索时间">
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
                project_type: '',
            }
        },
        computed: {
            computed_result_data: function () {
                let tmp_list = [];
                for (let value of this.result_data.result) {
                    let result_item = JSON.stringify(value.result);
                    let short_result_item = '';
                    if (result_item.length > 66) {
                        short_result_item = result_item.slice(0, 66) + '...';
                    }
                    let tmp_value = {
                        result: short_result_item,
                        full_result: result_item,
                        update_timestamp: value.update_timestamp,
                    }
                    tmp_list.push(tmp_value);
                }
                return tmp_list;
            },
            computed_gov_result_data: function () {
                let tmp_list = [];
                for (let value of this.result_data.result) {
                    let result_item = JSON.stringify(value.result);
                    let short_result_item = '';
                    if (result_item.length > 66) {
                        short_result_item = result_item.slice(0, 66) + '...';
                    }
                    let short_url = value.result.url;
                    if (value.result.url.length > 66) {
                        short_url = value.result.url.slice(0, 66) + '...'
                    }
                    let tmp_value = {
                        result: short_result_item,
                        full_url: value.result.url,
                        short_url: short_url,
                        reason: value.result.reason,
                        update_timestamp: value.update_timestamp,
                    }
                    tmp_list.push(tmp_value);
                }
                console.log(tmp_list);
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
                    if (this.result_data.result.length !== 0 && this.result_data.result[0].result.type !== undefined) {
                        this.project_type = this.result_data.result[0].result.type;
                    }
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
    .link {
        text-decoration: none;
    }

    .popword {
        width: 100%;
        height: auto;
        word-wrap: break-word;
        word-break: break-all;
        overflow: hidden;
    }
</style>
