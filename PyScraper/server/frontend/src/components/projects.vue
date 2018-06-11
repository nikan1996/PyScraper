<template>
    <div id="projects">
        <router-link to="/create_project">
            <el-button type="primary">新建项目</el-button>
        </router-link>
        <router-link to="/create_gov_project">
            <el-button type="primary">新建政府项目</el-button>
        </router-link>
        <router-link to="/gov_lexicon">
            <el-button type="primary">政府关键词库</el-button>
        </router-link>
        <div v-cloak>
            <el-table :data="show_projects.slice((currentPage-1)*pagesize,currentPage*pagesize)" stripe
                      style="width: 100%"
                      :default-sort="{prop: 'project_id', order: 'descending'}">
                <el-table-column prop="'tag" label="标签" width="180">
                </el-table-column>
                <el-table-column prop="project_name" label="项目名称" width="180">
                </el-table-column>
                <el-table-column prop="status" label="状态">
                </el-table-column>
                <el-table-column
                        fixed="right"
                        label="操作"
                        width="400">
                    <template slot-scope="scope">
                        <el-button type="primary" size="small" @click="see(scope.row)">查看</el-button>
                        <el-button type="primary" size="small" @click="edit(scope.row)">编辑</el-button>
                        <el-button type="primary" size="small" @click="start(scope.row)"
                                   :disabled="scope.row.status == '运行'"
                        >开始
                        </el-button>
                        <el-button type="primary" size="small" @click="pause(scope.row)"
                                   :disabled="scope.row.status == '暂停'||scope.row.status == '停止'">暂停
                        </el-button>
                        <el-button type="primary" size="small" @click="stop(scope.row)"
                                   :disabled="scope.row.status == '停止'">停止
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange"
                       :current-page="currentPage" :page-sizes="[5, 9, 10]" :page-size="pagesize"
                       layout="total, sizes, prev, pager, next, jumper" :total="total">
        </el-pagination>
    </div>
</template>

<script>
    import axios from 'axios';

    function sortByKey(array, key) {
    return array.sort(function(a, b) {
        let x = a[key]; let y = b[key];
        return ((x < y) ? -1 : ((x > y) ? 1 : 0));
    });
}
    export default {
        name: "Projects",
        created() {
            this.fetchData();
        },
        data() {
            return {
                projects: [],
                /**{
                    project_id: '1',
                    tag: '',
                    project_name: '温州市科技局',
                    status: 'start',
                    update_timestamp: "2018-06-03 02:34:20",
                    setting: {},
                }*/
                projects_status: {
                    'stop': '停止',
                    'pause': '暂停',
                    'start': '运行',
                },
                currentPage: 1,
                pagesize: 9,
            }
        },
        computed: {
            show_projects: function () {
                let tmp_list = [];
                for (let value of this.projects) {
                    let tmp_value = {
                        project_id: value.project_id,
                        tag: value.tag,
                        project_name: value.project_name,
                        status: this.projects_status[value.status],
                        update_timestamp: value.update_timestamp,
                    }
                    tmp_list.push(tmp_value);
                }
                return tmp_list;
            },

            total: function () {
                return this.projects.length;
            }
        },
        methods: {
            fetchData() {//获取项目列表
                axios.get('/projects').then((response) => {
                    this.projects = sortByKey(response.data, 'update_timestamp').reverse();
                }).catch((response) => {
                    console.log(response);
                    this.$message.error({
                        message: "获取项目失败啦，检查下你的网络吧"
                    });
                });
            },
            see(row) {
                this.$router.push({path: '/project/' + row.project_id});
                console.log(row);
            },
            start(row) {
                console.log(row);
                axios.put(
                    '/project_action/' + row.project_id,
                    JSON.stringify({'action': 'start'}),
                    {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    }
                ).then(() => {
                    let self = this;
                    setTimeout(
                        function () {
                            self.fetchData()
                            self.$message.success({
                                message: "启动项目成功"
                            });
                        },
                        1000
                    )
                }).catch(() => {
                    this.$message.error({
                        message: "启动项目失败请检查网络设置"
                    });

                });

            },
            stop(row) {
                console.log(row);
                axios.put(
                    '/project_action/' + row.project_id,
                    JSON.stringify({'action': 'stop'}),
                    {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    }
                ).then(() => {
                    let self = this;
                    setTimeout(
                        function () {
                            self.fetchData()
                            self.$message.success({
                                message: "停止项目成功"
                            });
                        },
                        1000
                    )

                }).catch(() => {
                    this.$message.error({
                        message: "停止项目失败请检查网络设置"
                    });

                });
//                 setTimeout(this.fetchData(), 1000);
            },
            pause(row) {
                console.log(row);
                axios.put(
                    '/project_action/' + row.project_id,
                    JSON.stringify({'action': 'pause'}),
                    {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    }
                ).then(() => {
                    let self = this;
                    setTimeout(
                        function () {
                            self.fetchData()
                            self.$message.success({
                                message: "暂停项目成功"
                            });
                        },
                        1000
                    )


                }).catch(() => {
                    this.$message.error({
                        message: "暂停项目失败请检查网络设置"
                    });

                });
//                 setTimeout(this.fetchData(), 1000);
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
    #projects {

    }
</style>
