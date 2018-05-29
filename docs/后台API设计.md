# 后台API设计

### 项目Project

获取Project列表

`GET /projects`

创建project

`put /projects`

删除某个Project

`DELETE /projects/<int:project_id>`

修改某个Project

`PUT /projects/<int:project_id>`

查看某个Project

`GET /databases/<int:project_id>`

### Project Action

Action: Start, Stop, Pause

`PUT /project_action/<string:action>`

### 数据库Database

获取Database列表

`GET /databases`

新建Database

`PUT /database`

删除某个Database

`DELETE /databases/<int:database_id>`

修改某个Database

`PUT /databases/<int:database_id>`

查看某个Database

`GET /databases/<int:database_id>`



### 爬虫Spider

获取Spider列表

`GET /spiders`

删除某个Spider

`DELETE /spiders/<int:spider_id>`

修改某个Spider

`PUT /spiders/<int:spider_id>`

查看某个Spider

`GET /spiders/<int:spider_id>`



Debug模式

GET /spider/debug/



### 