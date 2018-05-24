<template>
    <div id="database">
        <el-tabs type="border-card" v-model="activeName">
            <el-tab-pane>
                <span slot="label"><i class="el-icon-circle-plus-outline"></i>添加数据库</span>
                <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
                    <el-form-item label="连接名" prop="name">
                        <el-input v-model="ruleForm.name" suffixIcon="el-icon-edit"></el-input>
                    </el-form-item>
                    <el-form-item label="地址" prop="db_address">
                        <el-input v-model="ruleForm.name" placeholder="localhost"></el-input>
                    </el-form-item>
                    <el-form-item label="端口" prop="db_port">
                        <el-input v-model="ruleForm.name" placeholder="3306"></el-input>
                    </el-form-item>
                    <el-form-item label="数据库名称" prop="db_name">
                        <el-input v-model="ruleForm.name" suffixIcon="el-icon-edit"></el-input>
                    </el-form-item>
                    <el-form-item label="用户名" prop="db_user">
                        <el-input v-model="ruleForm.name" placeholder="user"></el-input>
                    </el-form-item>
                    <el-form-item label="密码" prop="db_password">
                        <el-input v-model="ruleForm.name" placeholder="password" type="password"></el-input>
                    </el-form-item>

                    <el-form-item label="类型" prop="db_type">
                        <el-select v-model="db_type_default_value" defaultFirstOption placeholder="请选择">
                            <el-option
                                    v-for="item in db_type_options"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="submitForm('ruleForm')">立即创建</el-button>
                        <el-button @click="resetForm('ruleForm')">测试</el-button>
                        <el-button @click="resetForm('ruleForm')">重置</el-button>
                    </el-form-item>
                </el-form>
            </el-tab-pane>
            <el-tab-pane label="数据库管理" name="db_management">
                <el-table :data="db_data" stripe style="width: 100%">
                    <el-table-column prop="db_name" label="连接名" width="180">
                    </el-table-column>
                    <el-table-column label="操作" width="180">
                    </el-table-column>
                </el-table>
                <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange"
                               :current-page="currentPage" :page-sizes="[10, 20, 50]" :page-size="10"
                               layout="total, sizes, prev, pager, next, jumper" :total="total">
                </el-pagination>
            </el-tab-pane>

        </el-tabs>

    </div>
</template>
<script>
    import ElSelectDropdown from "../../node_modules/element-ui/packages/select/src/select-dropdown.vue";

    export default {
        components: {ElSelectDropdown},
        name: "Databases",
        data() {
            return {
                activeName: "db_management",
                ruleForm: {
                    name: '',
                    region: '',
                    date1: '',
                    date2: '',
                    delivery: false,
                    type: [],
                    resource: '',
                    desc: ''
                },
                rules: {
                    db_name: [{
                        required: true,
                        message: '请输入数据库名称',
                        trigger: 'blur'
                    }],
                    db_address: [{
                        required: true,
                        message: '请输入数据库地址',
                        trigger: 'blur'
                    }],

                },
                db_type_options: [{
                    value: 'mysql',
                    label: 'Mysql',
                },
                    {
                        value: 'mongodb',
                        label: 'MongoDB',
                    }],
                currentPage: 1,
                total: 0,
                db_type_default_value: "mysql",
                db_data: [],
            };
        },
        methods: {
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        alert('submit!');
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            resetForm(formName) {
                this.$refs[formName].resetFields();
            },

            handleSizeChange(val) {
                console.log(`每页 ${val} 条`);
            },
            handleCurrentChange(val) {
                console.log(`当前页: ${val}`);
            }

        }
    }
</script>

<style scoped>

</style>
