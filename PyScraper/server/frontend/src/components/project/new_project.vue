<template>
    <div>
        <el-steps :active="active" finishStatus="success">
            <el-step title="步骤 1"></el-step>
            <el-step title="步骤 2"></el-step>
            <el-step title="步骤 3"></el-step>
        </el-steps>
        <!--<el-form-item label="活动区域" prop="region">-->
        <!--<el-select v-model="projectForm.region" placeholder="请选择活动区域">-->
        <!--<el-option label="区域一" value="shanghai"></el-option>-->
        <!--<el-option label="区域二" value="beijing"></el-option>-->
        <!--</el-select>-->
        <!--</el-form-item>-->
        <!--<el-form-item label="活动性质" prop="type">-->
        <!--<el-checkbox-group v-model="projectForm.type">-->
        <!--<el-checkbox label="美食/餐厅线上活动" name="type"></el-checkbox>-->
        <!--<el-checkbox label="地推活动" name="type"></el-checkbox>-->
        <!--<el-checkbox label="线下主题活动" name="type"></el-checkbox>-->
        <!--<el-checkbox label="单纯品牌曝光" name="type"></el-checkbox>-->
        <!--</el-checkbox-group>-->
        <!--</el-form-item>-->
        <!--<el-form-item label="特殊资源" prop="resource">-->
        <!--<el-radio-group v-model="projectForm.resource">-->
        <!--<el-radio label="线上品牌商赞助"></el-radio>-->
        <!--<el-radio label="线下场地免费"></el-radio>-->
        <!--</el-radio-group>-->
        <!--</el-form-item>-->
        <!--<el-form-item label="活动形式" prop="desc">-->
        <!--<el-input type="textarea" v-model="projectForm.desc"></el-input>-->
        <!--</el-form-item>-->
        <!--<el-form-item>-->
        <!--<el-button type="primary" @click="submitForm('projectForm')">立即创建</el-button>-->
        <!--</el-form-item>-->
        <div v-if="active==0">
            <el-button type="success" @click="next_exist_script">选择已有脚本</el-button>
            <el-button type="primary" @click="next_non_exist_script">新建脚本</el-button>

        </div>
        <template v-if="active==1">
            <template v-if="new_spider">
                <el-form :model="projectForm" :rules="rules" ref="projectForm" labelWidth="100px"
                         class="demo-projectForm">
                    <el-form-item label="项目名称" prop="project_name">
                        <el-input v-model="projectForm.project_name"></el-input>
                    </el-form-item>
                    <el-form-item label="脚本名称" prop="spider_name">
                        <el-input v-model="projectForm.spider_name"></el-input>
                    </el-form-item>
                    <el-form-item label="起始URL" prop="start_url">
                        <el-input v-model="projectForm.start_url"></el-input>
                    </el-form-item>
                    <el-form-item label="遵守rbots.txt" prop="obey_robots">
                        <el-switch v-model="projectForm.obey_robots" activeText="on" inactiveText="off"></el-switch>
                    </el-form-item>
                    <el-form-item label="重复抓取" prop="repeat_enabled">
                        <el-switch v-model="projectForm.repeat_enabled" activeText="on" inactiveText="off"></el-switch>
                    </el-form-item>
                    <el-form-item label="使用代理" prop="proxy_enabled">
                        <el-switch v-model="projectForm.proxy_enabled" activeText="on" inactiveText="off"></el-switch>
                    </el-form-item>
                    <el-form-item label="选择数据库" prop="databases">
                        <el-select v-model="choosed_database" placeholder="请选择">
                            <el-option
                                    v-for="database in databases"
                                    :key="database.database_id"
                                    :value="database.database_id">
                                {{database.database_name}}
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="标签" prop="tag">
                        <el-input v-model="projectForm.tag"></el-input>
                    </el-form-item>
                    <el-button style="margin-top: 12px;" @click="next">下一步</el-button>
                </el-form>
            </template>
            <template v-else>
                <el-form :model="projectForm" :rules="rules" ref="projectForm" labelWidth="100px"
                         class="demo-projectForm">
                    <el-form-item label="项目名称" prop="project_name">
                        <el-input v-model="projectForm.project_name"></el-input>
                    </el-form-item>
                    <el-form-item label="选择脚本" prop="spider_name">
                        <el-select v-model="projectForm.spider_name" placeholder="请选择">
                            <el-option
                                    v-for="(key, value) in spiders"
                                    :key="key"
                                    :value="value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="选择数据库" prop="databases">
                        <el-select v-model="choosed_database" placeholder="请选择">
                            <el-option
                                    v-for="database in databases"
                                    :key="database.database_id"
                                    :value="database.database_id">
                                {{database.database_name}}
                            </el-option>
                        </el-select>
                    </el-form-item>

                    <el-button style="margin-top: 12px;" @click="next_step">下一步</el-button>
                </el-form>
            </template>
        </template>
        <template v-else-if="active==2">
            <el-form :model="projectForm" :rules="rules" ref="projectForm" labelWidth="100px" class="demo-projectForm">
                <el-card>
                    <div slot="header" class="clearfix">
                        <span>通知配置</span>
                    </div>
                    <el-form-item label="邮箱" prop="email">
                        <el-input v-model="projectForm.name"></el-input>
                    </el-form-item>
                    <el-form-item label="微信" prop="wechat">
                        <el-input v-model="projectForm.desc"></el-input>
                    </el-form-item>
                    <el-form-item label="Webhook" prop="webhook">
                        <el-input v-model="projectForm.desc"></el-input>
                    </el-form-item>

                    <el-button type="primary" @click="submitForm('projectForm')">立即创建</el-button>

                </el-card>
            </el-form>

        </template>

    </div>
</template>
<script>
    import axios from "axios";
    import ElButton from "../../../node_modules/element-ui/packages/button/src/button.vue";

    export default {
        components: {ElButton},
        name: 'New_project',
        created() {
            this.get_spiders();
            this.get_databases();
        },
        model: {
            prop: 'database_id',
            event: 'change'
        },
        props: {
            database_id: String,
        },
        data() {
            return {

                spiders: {},
                databases: {},
                new_spider: true,
                active: 0,
                projectForm: {
                    project_name: '',
                    spider_name: '',
                    spidercls: '',
                    database_id: null,
                    infomation_config: {},
                    start_url: '',
                    obey_robots: true,
                    repeat_enabled: false,
                    proxy_enabled: false,
                    database_config: {},
                    tag: "",
                    cron_config: {},
                },
                rules: {
                    project_name: {required: true, message: '请输入项目名称', trigger: 'blur'},

                    spider_name: {required: true, message: '请输入脚本名', trigger: 'blur'},
                    start_url: {required: true, message: '请输入起始URL', trigger: 'blur'},

                },
            };
        },
        computed: {
            choosed_database: {
                // getter
                get: function () {
                    if (this.projectForm.database_id === null) {
                        return null
                    }
                    return this.databases[this.projectForm.database_id].database_name
                },
                // setter
                set: function (newValue) {
                    console.log(newValue);
                    this.projectForm.database_id = newValue;
                }
            },
            post_projectForm: function () {
                let form = {
                    project_name: this.projectForm.project_name,
                    setting: {
                        infomation_config: this.projectForm.infomation_config,
                        start_url: this.projectForm.start_url,
                        obey_robots: this.projectForm.obey_robots,
                        repeat_enabled: this.projectForm.repeat_enabled,
                        proxy_enabled: this.projectForm.proxy_enabled,
                        spidercls: this.spiders[this.projectForm.spider_name],
                        database_config: this.databases[this.projectForm.database_id].config,
                    },
                    tag: "",
                    cron_config: this.projectForm.cron_config,
                };
                console.log(form)
                return form;
            }

        },
        methods: {
            get_spiders() {
                axios.get('/spiders').then((response) => {
                    this.spiders = response.data;
                }).catch((response) => {
                    console.log(response);
                    this.$message.error({
                        message: "获取脚本失败啦，检查下你的网络吧"
                    });
                });
            },
            get_databases() {
                axios.get('/databases').then((response) => {
                    for (let item of response.data) {
                        this.databases[item.database_id] = item;
                    }
                    console.log(this.databases)
                }).catch((response) => {
                    console.log(response);
                    this.$message.error({
                        message: "获取数据库失败啦，检查下你的网络吧"
                    });
                });
            },
            next() {
                this.active++;
            },
            next_step() {
                this.$refs['projectForm'].validate((valid) => {
                    if (valid) {
                        console.log('legal next setp');
                        this.next();

                    } else {
                        console.log('illegal next setp');
                        return false;
                    }
                });
            },
            next_exist_script() {
                this.next();
                this.new_spider = false
            },
            next_non_exist_script() {
                this.next();
                this.new_spider = true
            },

            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                        if (valid) {
                            console.log(valid);
                            axios.put(
                                '/projects',
                                JSON.stringify(this.post_projectForm),
                                {
                                    headers: {
                                        'Content-Type': 'application/json'
                                    }
                                }
                            ).then(() => {
                                this.$router.push({path: '/projects'});
                                this.$message.success({
                                    message: "新建项目成功"
                                });

                            }).catch(() => {
                                this.$message.error({
                                    message: "新建项目失败请检查网络设置"
                                });

                            });
                        }
                        else {
                            console.log('error submit!!');
                            return false;
                        }
                    }
                );
            },

        }
    }
</script>
