<template>
    <div id="database">
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
                               layout="lexicon_total, sizes, prev, pager, next, jumper" :lexicon_total="lexicon_total">
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
    </div>
</template>
<script>
    import axios from 'axios';

    export default {
        name: "Gov_lexicon",
        created() {
            this.fetch_lexicon_data();
        },
        data() {
            return {
                activeName: "gov_lexicon",
                gov_lexicon_data: [],

                gov_rule_form: {gov_rules: [['', '', '']]},

                lexicon_currentPage: 1,
                lexicon_pagesize: 9,
            };
        },
        computed: {
            lexicon_total: function () {
                return this.gov_lexicon_data.length
            },


        },
        methods: {
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
</style>
