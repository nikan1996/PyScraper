<template>
    <div id="database">
        <el-tabs id='eltabs' type="card" v-model="activeName">
            <el-tab-pane label="数据库管理" name="db_management">
                <el-table id='dbtable' :data="db_data.slice((currentPage-1)*pagesize,currentPage*pagesize)" stripe
                          style="width: 100%;"
                          :default-sort="{prop: 'update_timestamp', order: 'descending'}"
                >
                    <el-table-column prop="database_name" label="连接名">
                    </el-table-column>
                    <el-table-column prop="update_timestamp" label="更新时间">
                    </el-table-column>
                    <el-table-column
                            fixed="right"
                            label="操作"
                            width="180">
                        <template slot-scope="scope">
                            <el-button @click="handleClick(scope.row)" type="text" size="small">查看</el-button>
                            <el-button type="text" size="small">编辑</el-button>
                            <el-button type="text" size="small">删除</el-button>
                        </template>
                    </el-table-column>
                </el-table>
                <div id="letPaginationBottom"></div>
                <el-pagination id="ele_pagination" @size-change="handleSizeChange" @current-change="handleCurrentChange"
                               :current-page="currentPage" :page-sizes="[5, 10]" :page-size="pagesize"
                               layout="total, sizes, prev, pager, next, jumper" :total="total">
                </el-pagination>
            </el-tab-pane>
            <el-tab-pane>
                <span slot="label"><i class="el-icon-circle-plus-outline"></i>添加数据库</span>
                <el-form :model="new_db" ref="new_db" :rules="form_check_rules" label-width="100px">
                    <el-form-item label="连接名" prop="database_name">
                        <el-input v-model="new_db.database_name" suffixIcon="el-icon-edit"></el-input>
                    </el-form-item>
                    <el-form-item label="地址" prop="config.host">
                        <el-input v-model="new_db.config.host" placeholder="localhost"></el-input>
                    </el-form-item>
                    <el-form-item label="端口" prop="config.port">
                        <el-input v-model.number="new_db.config.port" placeholder="3306"></el-input>
                    </el-form-item>
                    <el-form-item label="数据库名称" prop="config.database">
                        <el-input v-model="new_db.config.database" suffixIcon="el-icon-edit"></el-input>
                    </el-form-item>
                    <el-form-item label="用户名" prop="config.user">
                        <el-input v-model="new_db.config.user" placeholder="user"></el-input>
                    </el-form-item>
                    <el-form-item label="密码" prop="config.password">
                        <el-input v-model="new_db.config.password" placeholder="password" type="password"></el-input>
                    </el-form-item>

                    <el-form-item label="类型" prop="db_type">
                        <el-select v-model="new_db.db_type" defaultFirstOption placeholder="请选择">
                            <el-option
                                    v-for="item in db_types"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="submitForm('new_db')">立即创建</el-button>
                        <el-button @click="resetForm('new_db')">重置</el-button>
                    </el-form-item>
                </el-form>
            </el-tab-pane>

        </el-tabs>

    </div>
</template>
<script>
    import axios from 'axios'

    export default {
        name: "Databases",
        created() {
            this.fetchData();
        },
        data() {
            return {
                activeName: "db_management",
                new_db: {
                    database_name: '',
                    config: {
                        host: '',
                        port: '',
                        user: '',
                        password: '',
                        database: ''
                    },
                    db_type: ''
                },
                form_check_rules: {
                    database_name: [{
                        required: true,
                        message: '请输入连接名',
                        trigger: 'blur'
                    }],
                    config: {
                        database: [{
                            required: true,
                            message: '请输入数据库名称',
                            trigger: 'blur'
                        }],
                        host: [{
                            required: true,
                            message: '请输入数据库地址',
                            trigger: 'blur'
                        }],
                        port: [{
                            required: true,
                            message: '请输入数据库端口',
                            trigger: 'blur'
                        }],
                        user: [{
                            required: true,
                            message: '请输入数据库用户名',
                            trigger: 'blur'
                        }],
                        password: [{
                            required: true,
                            message: '请输入数据库密码',
                            trigger: 'blur'
                        }],
                    },
                    db_type: [{
                        required: true,
                        message: '请输入数据库类型',
                        trigger: 'blur'
                    }],
                },
                db_types: [
                    {
                        value: 'mysql',
                        label: 'Mysql',
                    },
                    {
                        value: 'mongodb',
                        label: 'MongoDB',
                    }
                ],
                currentPage: 1,
                pagesize: 5,
                db_type_default_value: "mysql",
                db_data: [],
            };
        },
        computed: {
            total: function () {
                return this.db_data.length
            },
            show_data: function () {
                return this.db_data
            },

        },
        methods: {
            fetchData() {//获取数据库列表
                axios.get('/databases').then((response) => {
                    this.db_data = response.data;
                }).catch((response) => {
                    console.log(response);
                    this.$message.error({
                        message: "获取数据库失败啦，检查下你的网络吧"
                    });
                });
            },
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        axios.put(
                            '/databases',
                            JSON.stringify(this.new_db),
                            {
                                headers: {
                                    'Content-Type': 'application/json'
                                }
                            }
                        ).then(() => {
                            this.$message.success({
                                message: "成功添加数据库"
                            });
                            this.resetForm(formName);
                            this.fetchData();
                        }).catch(() => {
                            console.log(response);
                            this.$message.error({
                                message: "添加数据库失败啦请检查你的数据库配置是否能正确连接"
                            });
                        });
                    }
                    else {
                        this.$message.error({
                            message: "请先正确填写数据库配置"
                        });

                        return false;
                    }
                });
            },
            resetForm(formName) {
                this.$refs[formName].resetFields();
            },


            handleSizeChange(val) {
                this.pagesize = val;
                console.log(`每页 ${val} 条`);
            },
            handleCurrentChange(val) {
                this.currentPage = val;
                console.log(`当前页: ${val}`);
            }

        }
    }
</script>

<style scoped>
    #eltabs {
        /*min-height: 600px;*/

    }

    #database {
        /*overflow:auto;*/
    }
    #dbtable{
        /*position: relative;*/
        /*min-height: 600px;*/
        /*top: 0;*/
        /*left: 0;*/
        /*right: 0;*/
        /*bottom: 0;*/
    }
    /*#letPaginationBottom{*/
    /*min-height: 200px;*/
    /*overflow:auto;*/
    /*}*/
</style>
