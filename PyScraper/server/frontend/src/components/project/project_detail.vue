<template>
    <div id="project_detail">
        <el-tabs type="card" v-model="activeName">
            <el-tab-pane label="已爬取网站列表" name="task">
                <el-table id='tasktable'
                          :data="computed_task"
                          stripe
                          style="width: 100%;"
                >
                    <el-table-column label="爬取链接" width="600">
                        <template slot-scope="scope">
                            <el-popover trigger="hover" placement="bottom-start" width="400">
                                <p class="popword">{{scope.row.full_url}}</p>
                                <div slot="reference" class="name-wrapper">
                                    <a class="link" target="_blank"
                                       :href="scope.row.full_url">{{scope.row.short_url}}</a>
                                </div>
                            </el-popover>
                        </template>
                    </el-table-column>
                    <!--<el-table-column prop="status_code" label="响应状态码">-->
                    <!--</el-table-column>-->
                    <el-table-column prop="update_timestamp" label="爬取时间">
                    </el-table-column>
                </el-table>
                <div ></div>
                <el-pagination  @size-change="task_handleSizeChange"
                               @current-change="task_handleCurrentChange"
                               :current-page="task_currentPage" :page-sizes="[5, 9, 10]" :page-size="task_pagesize"
                               layout="total, sizes, prev, pager, next, jumper" :total="task_total">
                </el-pagination>
            </el-tab-pane>


            <el-tab-pane label="不符合规则的结果" name="error_word">
                <el-tag>检索结果仅代表不匹配结果（也有可能语义在上下文中是正确的，请继续人工筛选）</el-tag>
                <el-table id='error_word_table'
                          :data="computed_error_word"
                          stripe
                          style="width: 100%;">
                    <el-table-column label="网址" width="600">
                        <template slot-scope="scope">
                            <el-popover trigger="hover" placement="bottom-start" width="400">
                                <p class="popword">{{scope.row.full_url}}</p>
                                <div slot="reference" class="name-wrapper">
                                    <a class="link" target="_blank"
                                       :href="scope.row.full_url">{{scope.row.short_url}}</a>
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
                <el-pagination @size-change="error_word_handleSizeChange"
                               @current-change="error_word_handleCurrentChange"
                               :current-page="error_word_currentPage" :page-sizes="[5, 9, 10]"
                               :page-size="error_word_pagesize"
                               layout="total, sizes, prev, pager, next, jumper" :total="error_word_total">
                </el-pagination>
            </el-tab-pane>

            <el-tab-pane label="错误链接列表" name="error_link">
                <el-table id='resulttable'
                          :data="computed_error_link"
                          stripe
                          style="width: 100%;"
                >
                    <el-table-column
                            type="index"
                            width="50"
                            label="序号">
                    </el-table-column>

                    <el-table-column label="错误链接">
                        <template slot-scope="scope">
                            <el-popover trigger="hover" placement="bottom-start" width="400">
                                <p class="popword">{{scope.row.full_url}}</p>
                                <div slot="reference" class="name-wrapper">
                                    <a class="link" target="_blank"
                                       :href="scope.row.full_url">{{scope.row.short_url}}</a>
                                </div>
                            </el-popover>
                        </template>
                    </el-table-column>
                    <el-table-column width="200" prop="update_timestamp" label="解析时间"></el-table-column>
                    <el-table-column
                            fixed="right"
                            label="分析"
                            width="300">
                        <template slot-scope="scope">
                            <a target="_blank" :href="'/location/' + scope.row.result_id + '?type=real'">
                                <el-button type="primary" size="small">实时定位
                                </el-button>
                            </a>
                            <a target="_blank" :href="'/location/' + scope.row.result_id+ '?type=cache'">
                                <el-button type="primary" size="small">缓存定位
                                </el-button>
                            </a>
                            <el-button type="primary" size="small" @click="delete_result(scope.row.result_id)">已解决
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
                <div></div>
                <el-pagination @size-change="error_link_handleSizeChange"
                               @current-change="error_link_handleCurrentChange"
                               :current-page="error_link_currentPage" :page-sizes="[5, 9, 10]"
                               :page-size="error_link_pagesize"
                               layout="total, sizes, prev, pager, next, jumper" :total="error_link_total">
                </el-pagination>
            </el-tab-pane>
            <el-tab-pane label="政府关键词库" name="gov_lexicon">
                <el-table id='lexicontable'
                          :data="gov_lexicon_data.slice((lexicon_currentPage-1)*lexicon_pagesize,lexicon_currentPage*lexicon_pagesize)" stripe
                          style="width: 100%;"
                          :default-sort="{prop: 'update_timestamp', order: 'descending'}"
                >
                    <el-table-column prop="pattern" label="匹配词">
                    </el-table-column>
                    <el-table-column prop="correct_word" label="正确词">
                    </el-table-column>
                    <el-table-column prop="domain" label="域名">
                    </el-table-column>
                    <el-table-column prop="update_timestamp" label="更新时间">
                    </el-table-column>
                    <el-table-column
                            fixed="right"
                            label="操作"
                            width="300">
                        <template slot-scope="scope">
                            <el-button type="primary" size="small" @click="deleteRule(scope.row.rule_id)">删除</el-button>
                        </template>
                    </el-table-column>
                </el-table>
                <div id="letPaginationBottom"></div>
                <el-pagination id="ele_pagination" @size-change="handleSizeChange" @current-change="handleCurrentChange"
                               :current-page="lexicon_currentPage" :page-sizes="[5, 9, 10]" :page-size="lexicon_pagesize"
                               layout="total, sizes, prev, pager, next, jumper" :total="lexicon_total">
                </el-pagination>
            </el-tab-pane>
            <el-tab-pane>
                <span slot="label"><i class="el-icon-circle-plus-outline"></i>添加规则</span>
                <el-form :inline="true" :model="gov_rule_form" ref="gov_rule_form">

                    <el-tag type="success" style="margin:10px">示例： 匹配词：中*国 正确词：中华人民共和国
                    </el-tag>
                    <div v-for="(gov_rule, index) in gov_rule_form.gov_rules">
                        <el-form-item label="匹配词" :rules="{
                            required: true, message: '匹配词不能为空', trigger: 'blur'}"
                                      :prop="'gov_rules.' + index + '.0'">
                            <el-input v-model="gov_rule[0]"></el-input>
                        </el-form-item>
                        <el-form-item label="正确词" :rules="{
                            required: true, message: '正确词不能为空', trigger: 'blur'}"
                                      :prop="'gov_rules.' + index + '.1'">
                            <el-input v-model="gov_rule[1]"></el-input>
                        </el-form-item>
                        <el-form-item label="网站地址" :rules="[{
                            required: true, message: '网站地址不能为空', trigger: 'blur'},{ type: 'url', message: '请输入正确的网站地址', trigger: ['blur', 'change'] }]"
                                      :prop="'gov_rules.' + index + '.2'">
                            <el-input v-model="gov_rule[2]"></el-input>
                        </el-form-item>
                        <el-button @click.prevent="removeRule(gov_rule)">删除</el-button>
                    </div>
                    <el-button @click.prevent="addRule">新增规则</el-button>
                    <el-button type="primary" style="margin-top: 12px;" @click="lexicon_submitForm('gov_rule_form')">立即添加
                    </el-button>


                </el-form>
            </el-tab-pane>
        </el-tabs>

    </div>
</template>

<script>
    import axios from 'axios';
    import ElTabPane from "../../../node_modules/element-ui/packages/tabs/src/tab-pane.vue";

    export default {
        components: {ElTabPane},
        name: 'Project',
        created() {
            this.fetchData();
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
                error_word: {
                    total_count: "",
                    count: "",
                    result: [],
                },
                error_link: {
                    total_count: "",
                    count: "",
                    result: [],
                },
                error_word_currentPage: 1,
                error_word_pagesize: 9,

                error_link_currentPage: 1,
                error_link_pagesize: 9,
                gov_lexicon_data: [],

                gov_rule_form: {gov_rules: [['', '', '']]},

                lexicon_currentPage: 1,
                lexicon_pagesize: 9,

            }
        },
        computed: {
            computed_task: function () {
                let tmp_list = [];
                for (let value of this.task_data.result) {
                    let short_url = value.url;
                    if (value.url.length > 66) {
                        short_url = value.url.slice(0, 66) + '...'
                    }
                    let tmp_value = {
                        full_url: value.url,
                        short_url: short_url,
                        update_timestamp: value.update_timestamp,
                    };
                    tmp_list.push(tmp_value);
                }
                console.log(tmp_list);
                return tmp_list;
            },
            computed_error_word: function () {
                let tmp_list = [];
                for (let value of this.error_word.result) {
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
            computed_error_link: function () {
                let tmp_list = [];
                for (let value of this.error_link.result) {
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
                        result_id: value.result_id,
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
            error_word_total: function () {
                return Number(this.error_word.total_count)
            },
            error_link_total: function () {
                return Number(this.error_link.total_count)
            },
            lexicon_total: function () {
                return this.gov_lexicon_data.length
            },


        },
        methods: {
            fetchData() {
                this.fetchTaskData();
                this.fetch_error_word_data();
                this.fetch_error_link_data();
                this.fetch_lexicon_data()
            },
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
            fetch_error_word_data() {//获取错误列表
                axios.get('/results/' + this.$route.params.project_id + '?type=error_word').then((response) => {
                    console.log(response.data);
                    this.error_word = response.data;
                }).catch((response) => {
                    console.log(response);
                    this.$message.error({
                        message: "获取错误列表失败啦，检查下你的网络吧"
                    });
                });
            },
            fetch_error_link_data() {//获取错误链接列表
                axios.get('/results/' + this.$route.params.project_id + '?type=error_link').then((response) => {
                    console.log(response.data);
                    this.error_link = response.data;
                }).catch((response) => {
                    console.log(response);
                    this.$message.error({
                        message: "获取错误链接列表失败啦，检查下你的网络吧"
                    });
                });
            },
            fetch_lexicon_data() {//获取政府词库列表
                axios.get('/gov_lexicon').then((response) => {
                    this.gov_lexicon_data = response.data;
                }).catch((response) => {
                    console.log(response);
                    this.$message.error({
                        message: "获取政府词库列表失败啦，检查下你的网络吧"
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
            error_word_handleSizeChange(val) {
                this.error_word_pagesize = val;
                console.log(`每页 ${val} 条`);
            },
            error_link_handleSizeChange(val) {
                this.error_link_pagesize = val;
                console.log(`每页 ${val} 条`);
            },
            error_word_handleCurrentChange(val) {
                this.error_word_currentPage = val;
                console.log(`当前页: ${val}`);
            },
            error_link_handleCurrentChange(val) {
                this.error_link_currentPage = val;
                console.log(`当前页: ${val}`);
            },
            delete_result(result_id) {
                this.$confirm('此操作将删除记录, 是否删除?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    axios.delete(
                        '/result/' + result_id,
                    ).then(() => {
                        this.$message.success({
                            message: "成功删除"
                        });
                        this.fetch_error_link_data();
                    }).catch(() => {
                        this.$message.error({
                            message: "删除失败，请检查网络"
                        });
                    });

                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消删除'
                    });
                });
            },

            fetch_lexicon_data() {//获取政府词库列表
                axios.get('/gov_lexicon').then((response) => {
                    this.gov_lexicon_data = response.data;
                }).catch((response) => {
                    console.log(response);
                    this.$message.error({
                        message: "获取政府词库列表失败啦，检查下你的网络吧"
                    });
                });
            },
            lexicon_submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        axios.put(
                            '/gov_lexicon',
                            JSON.stringify(this.gov_rule_form),
                            {
                                headers: {
                                    'Content-Type': 'application/json'
                                }
                            }
                        ).then(() => {
                            this.$message.success({
                                message: "成功添加规则至词库"
                            });
                            this.resetForm(formName);
                            this.fetch_lexicon_data();
                        }).catch(() => {
                            this.$message.error({
                                message: "添加规则失败啦"
                            });
                        });
                    }
                    else {
                        this.$message.error({
                            message: "请先正确填写规则"
                        });

                        return false;
                    }
                });
            },
            resetForm(formName) {
                this.$refs[formName].resetFields();
            },


            handleSizeChange(val) {
                this.lexicon_pagesize = val;
                console.log(`每页 ${val} 条`);
            },
            handleCurrentChange(val) {
                this.lexicon_currentPage = val;
                console.log(`当前页: ${val}`);
            },
            removeRule(item) {
                let index = this.gov_rule_form.gov_rules.indexOf(item);
                if (index !== -1) {
                    this.gov_rule_form.gov_rules.splice(index, 1);
                }
            },
            addRule() {
                let arg = this.gov_rule_form.gov_rules;
                if (arg.length === 0) {
                    arg.push(['', '', '']);
                    return
                }
                arg.push(['', '', arg[arg.length - 1][2]]);

            },
            deleteRule(id) {
                axios.delete(
                    '/gov_lexicon/' + id,
                ).then(() => {
                    this.$message.success({
                        message: "成功删除规则"
                    });
                    this.fetch_lexicon_data();
                }).catch(() => {
                    this.$message.error({
                        message: "删除规则失败，请检查网络"
                    });
                });
            }

        }

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
