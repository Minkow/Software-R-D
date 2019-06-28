### Demo功能演示

***

#####1. 注册与登录

![1561714032750](C:\Users\Minkow\AppData\Roaming\Typora\typora-user-images\1561714032750.png)

比较简单的注册与登陆界面，使用MySql数据库存储用户信息，用户密码加盐后存入数据库。



##### 2. 主页面

![1561714110348](C:\Users\Minkow\AppData\Roaming\Typora\typora-user-images\1561714110348.png)

仿照百度搜索的页面 : )



##### 3. 查询界面

![1561714181637](C:\Users\Minkow\AppData\Roaming\Typora\typora-user-images\1561714181637.png)

数据存放于Neo4j数据库中，类RDF数据，蓝色的词条是超链接，主要保存词条的关系信息。



#####4. 可视化(演示的时候没有渲染出来Orz)

![1561714264425](C:\Users\Minkow\AppData\Roaming\Typora\typora-user-images\1561714264425.png)

把上述结果传入json使用cytoscape.js进行了可视化，可拖拽



##### 5. 知识编辑

![1561714331142](C:\Users\Minkow\AppData\Roaming\Typora\typora-user-images\1561714331142.png)

web界面上的知识编辑系统，限制管理员权限用户访问。填好三元组信息提交即可，支持增删改查所有功能。



##### 6. What else

以上是web接口，除此之外还有restful接口提供。

