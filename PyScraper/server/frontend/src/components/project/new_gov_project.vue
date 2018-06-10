<template>
    <div>
        <el-steps :active="active">
            <el-step title="步骤 1" icon="el-icon-edit"></el-step>
            <el-step title="规则配置" icon="el-icon-edit"></el-step>

        </el-steps>
        <template v-if="active==1">
            <p align="center"><b>新建政府项目</b></p>
            <el-form :model="gov_projectForm" :rules="rules" ref="gov_projectForm" labelWidth="100px">
                <el-form-item label="项目名称" prop="project_name">
                    <el-input v-model="gov_projectForm.project_name"></el-input>
                </el-form-item>
                <el-form-item label="脚本名称" prop="setting.spider_name">
                    <el-input v-model="gov_projectForm.setting.spider_name"></el-input>
                    <el-tag type="info">(建议是项目名称的拼音)</el-tag>
                </el-form-item>
                <el-form-item label="起始URL" prop="setting.start_url">
                    <el-input v-model="gov_projectForm.setting.start_url"></el-input>
                </el-form-item>
                <el-form-item label="标签" prop="tag">
                    <el-input v-model="gov_projectForm.tag"></el-input>
                </el-form-item>
                <el-form-item label="邮箱" prop="setting.information_config.email">
                    <el-input v-model="gov_projectForm.setting.information_config.email"></el-input>
                    <el-tag type="info">(有错误的网站会发到邮箱通知)</el-tag>
                </el-form-item>
                <el-form-item>
                    <el-button style="margin-top: 12px;" @click="next_step">下一步</el-button>
                    <el-button @click="resetForm('gov_projectForm')">重置</el-button>
                </el-form-item>
            </el-form>
        </template>
        <template v-if="active==2">
            <p align="center"><b>纠错规则配置(*号代表模糊匹配的字)</b></p>
            <el-tag type="info">例子：温*市和温州市</el-tag>
            <el-form :inline="true" :model="gov_projectForm" ref="gov_projectForm2" labelWidth="100px">
                <div v-for="(rule, index) in gov_projectForm.setting.rules">
                    <el-form-item label="匹配词" :rules="{
      required: true, message: '值不能为空', trigger: 'blur'
    }" :prop="'setting.rules.' + index + '.0'">
                        <el-input v-model="rule[0]"></el-input>
                    </el-form-item>
                    <el-form-item label="正确词" :rules="{
      required: true, message: '值不能为空', trigger: 'blur'
    }" :prop="'setting.rules.' + index + '.1'">
                        <el-input v-model="rule[1]"></el-input>
                    </el-form-item>
                    <el-button @click.prevent="removeRule(rule)">删除</el-button>
                </div>

            </el-form>
            <el-form>
                <el-form-item>
                    <el-button @click="addRule">新增规则</el-button>
                </el-form-item>
                <el-form-item>
                    <el-button style="margin-top: 12px;" @click="last">上一步</el-button>

                    <el-button type="primary" style="margin-top: 12px;" @click="submitForm('gov_projectForm2')">立即创建
                    </el-button>

                    <!--<el-button @click="resetForm('gov_projectForm')">重置</el-button>-->
                </el-form-item>
            </el-form>
        </template>
    </div>
</template>
<script>
    import axios from "axios";
    import ElFormItem from "../../../node_modules/element-ui/packages/form/src/form-item.vue";

    export default {
        components: {ElFormItem},
        name: 'New_gov_project',
        data() {
            return {

                active: 1,
                gov_projectForm: {
                    project_name: "",
                    setting: {
                        information_config: {},
                        start_url: "",
                        obey_robots: false,
                        repeat_enabled: false,
                        proxy_enabled: false,
                        spider_name: "",
                        spidercls: "",
                        rules: [],
                        database_config: {},
                        script_type: "gov",
                    },
                    tag: "",
                    cron_config: {},
                },
                rules: {
                    project_name: {required: true, message: '请输入项目名称', trigger: 'blur'},
                    setting: {
                        spider_name: {required: true, message: '请输入爬虫脚本名称', trigger: 'blur'},

                        start_url: [{required: true, message: '请输入起始网址', trigger: 'blur'},
                            { type: 'url', message: '网址需要以http开头'}
                        ],
                        information_config: {
                            email: {required: true, message: '请输入邮箱', trigger: 'blur'}
                        }
                    }
                }
            };
        },

        methods: {
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        axios.put(
                            '/projects',
                            JSON.stringify(this.gov_projectForm),
                            {
                                headers: {
                                    'Content-Type': 'application/json'
                                }
                            }
                        ).then(() => {
                            this.$router.push({path: '/projects'});
                            this.$message.success({
                                message: "新建政府项目成功"
                            });

                        }).catch(() => {
                            this.$message.error({
                                message: "新建政府项目失败请检查网络设置"
                            });

                        });
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            resetForm(formName) {
                this.$refs[formName].resetFields();
            },
            last() {
                this.active--;
            },
            next() {
                this.active++;
            },
            next_step() {
                this.$refs['gov_projectForm'].validate((valid) => {
                    if (valid) {
                        console.log('legal next setp');
                        this.next();

                    } else {
                        console.log('illegal next setp');
                        return false;
                    }
                });
            },
            removeRule(item) {
                let index = this.gov_projectForm.setting.rules.indexOf(item)
                if (index !== -1) {
                    this.gov_projectForm.setting.rules.splice(index, 1)
                }
            },
            addRule() {
                this.gov_projectForm.setting.rules.push([]);
            },

        }
    }
</script>
