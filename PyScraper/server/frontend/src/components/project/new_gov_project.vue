<template>
    <div>
        <el-steps :active="active" finishStatus="success">
            <el-step title="步骤 1"></el-step>
            <el-step title="步骤 2"></el-step>
            <el-step title="步骤 3"></el-step>
        </el-steps>
        <!--<el-form-item label="活动区域" prop="region">-->
        <!--<el-select v-model="ruleForm.region" placeholder="请选择活动区域">-->
        <!--<el-option label="区域一" value="shanghai"></el-option>-->
        <!--<el-option label="区域二" value="beijing"></el-option>-->
        <!--</el-select>-->
        <!--</el-form-item>-->
        <!--<el-form-item label="活动性质" prop="type">-->
        <!--<el-checkbox-group v-model="ruleForm.type">-->
        <!--<el-checkbox label="美食/餐厅线上活动" name="type"></el-checkbox>-->
        <!--<el-checkbox label="地推活动" name="type"></el-checkbox>-->
        <!--<el-checkbox label="线下主题活动" name="type"></el-checkbox>-->
        <!--<el-checkbox label="单纯品牌曝光" name="type"></el-checkbox>-->
        <!--</el-checkbox-group>-->
        <!--</el-form-item>-->
        <!--<el-form-item label="特殊资源" prop="resource">-->
        <!--<el-radio-group v-model="ruleForm.resource">-->
        <!--<el-radio label="线上品牌商赞助"></el-radio>-->
        <!--<el-radio label="线下场地免费"></el-radio>-->
        <!--</el-radio-group>-->
        <!--</el-form-item>-->
        <!--<el-form-item label="活动形式" prop="desc">-->
        <!--<el-input type="textarea" v-model="ruleForm.desc"></el-input>-->
        <!--</el-form-item>-->
        <!--<el-form-item>-->
        <!--<el-button type="primary" @click="submitForm('ruleForm')">立即创建</el-button>-->
        <!--</el-form-item>-->
        <div v-if="active==0">
            <el-form :model="ruleForm" :rules="rules" ref="ruleForm" labelWidth="100px" class="demo-ruleForm">
                <el-form-item label="项目名称" prop="project_name">
                    <el-input v-model="ruleForm.name"></el-input>
                </el-form-item>
                <el-form-item label="起始URL" prop="start_url">
                    <el-input v-model="ruleForm.desc"></el-input>
                </el-form-item>
                <el-form-item label="遵守rbots.txt" prop="obey_robots">
                    <el-switch v-model="ruleForm.delivery" activeText="on" inactiveText="off"></el-switch>
                </el-form-item>
                <el-form-item label="重复抓取" prop="repeat_enabled">
                    <el-switch v-model="ruleForm.delivery" activeText="on" inactiveText="off"></el-switch>
                </el-form-item>
                <el-form-item label="使用代理" prop="proxy_enabled">
                    <el-switch v-model="ruleForm.delivery" activeText="on" inactiveText="off"></el-switch>
                </el-form-item>
                <el-button style="margin-top: 12px;" @click="next">下一步</el-button>
            </el-form>
        </div>
        <div v-if="active==1">
            <el-button style="margin-top: 12px;" @click="next">下一步</el-button>
        </div>
        <div v-else-if="active==2">
            <el-button type="primary" @click="submitForm('NewProjectForm')">立即创建</el-button>
        </div>
    </div>
</template>
<script>
    import router from "vue-router";

    export default {
        name: 'New_project',
        data() {
            return {
                active: 1,
                NewProjectForm: {
                    project_name: '',
                    start_url: '',
                    obey_robots: true,
                    repeat_enabled: false,
                    proxy_enabled: false,

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
