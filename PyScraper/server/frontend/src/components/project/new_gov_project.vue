<template>
    <div>
        <el-form :model="gov_projectForm" :rules="rules" ref="gov_projectForm" labelWidth="100px"
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

            <el-form-item label="邮箱" prop="email">
                <el-input v-model="projectForm.name"></el-input>
            </el-form-item>
            <el-button type="primary" style="margin-top: 12px;" @click="submitForm('projectForm')">立即创建</el-button>
        </el-form>
    </div>
</template>
<script>
    import axios from "axios";

    export default {
        name: 'New_gov_project',
        data() {
            return {
                gov_projectForm: {
                    project_name: '',
                    type: 'gov',
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
                    start_url: {required: true, message: '请输入起始URL', trigger: 'blur'},

                }
            };
        },

        methods: {
            next() {
                if (this.active++ > 2) this.active = 0;
            },
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        alert('submit!');
                        router.push({path: '/projects'})
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            resetForm(formName) {
                this.$refs[formName].resetFields();
            }

        }
    }
</script>
