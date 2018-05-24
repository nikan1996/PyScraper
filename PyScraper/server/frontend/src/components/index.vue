<template>
    <div>
        <el-collapse v-model="activeNames" @change="handleChange">
            <el-collapse-item title="项目数量" name="1">
                <div>目前总共拥有4个项目。</div>
            </el-collapse-item>
            <el-collapse-item title="爬取数据总量" name="2">
                <div>目前总共爬取了4000222条数据。</div>
            </el-collapse-item>
            <el-collapse-item title="显示正在运行的项目数量" name="3">
                <div>目前正在运行的项目数量为3。</div>
            </el-collapse-item>

        </el-collapse>
    </div>
</template>
<script>
    export default {
        name: "Index",
        data() {
            return {
                activeNames: ['1']
            };
        },
        methods: {
            handleChange(val) {
                console.log(val);
            }
        }
    }
</script>