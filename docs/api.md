# API 

| 接口功能说明 | 接口详细信息 |
|:------------ |:----------- |
| 获取学生列表 | [api/get_person_list](#get_person_list) |
| 添加学生 | [api/add_person](#add_person) |
| 删除学生 | [api/delete_person](#delete_person) |
| 获取活动列表 | [api/get_activity_list](#get_activity_list) |
| 添加活动 | [api/add_activity](#add_activity) |
| 删除活动 | [api/delete_activity](#delete_activity) |
| 获取客户端更新 | [api/check_update](#check_update) |

| 类型名 | 类型详细信息 |
|:------ |:------------ |
| 学生 | [Person](#person) |
| 活动 | [Activity](#activity) |  

***以下所有API返回参数表均省略StatusCode部分，仅写出返回主体信息（<code>data</code>内）***

***

### <span id="get_person_list">获取学生列表</span>

*   请求URL
>   api/get_person_list

*   请求方式
>   GET

*   请求参数
>   | 请求参数 | 参数类型 | 可否为空 | 参数说明 |
>   | -------- |:------- |:-------:|:------- |
>   | filter | string | 可 | 一个或多个关于所需学生的属性限定表达式<br/>多个表达式之间用<code>$</code>分隔<br/>为空则无限定 |
>   | count | int | 可 | 至多请求的学生数量<br/>为空则无限定 |

*   请求实例
>请求至多5个活动参与分不小于3的男生
><pre><code>api/get_person_list?filter=gender==M$participation>=3&count=2</code></pre>

*   返回
>   | 返回参数 | 参数类型 | 参数说明 |
>   | -------- | :------- | :------- |
>   | [] | jsonArray | 学生信息列表 |

*   返回示例
><pre><code>[
>    {
>        "model": "app.person",
>        "pk": 1,
>        "fields": {
>            "student_number": "6666666666",
>            "name": "delbertbeta",
>            "gender": "M",
>            "participation": 4
>            ......
>        }
>    },
>    {
>        "model": "app.person",
>        "pk": 2,
>        "fields": {
>            "student_number": "6666666667",
>            "name": "oidiotlin",
>            "gender": "M",
>            "participation": 3
>            ......
>        }
>    }
>]</code></pre>

***

### <span id="add_person">添加学生</span>

*   请求URL
>   api/add_person

*   请求方式
>   POST

*   请求参数
>   | 请求参数 | 参数类型 | 可否为空 | 参数说明 |
>   | -------- | :------- |:-------:| :------- |
>   | student_number | string | 不可 | 新添加学生的学号 |
>   | name | string | 不可 | 新添加学生的姓名 |
>   | pinyin | string | 不可 | 新添加学生的姓名拼音 |
>   | gender | string | 不可 | 新添加学生的性别（男：<code>M</code>，女：<code>F</code>）|
>   | native_province | string | 可 | 新添加学生的姓名拼音 |
>   | dormitory | string | 可 | 新添加学生的寝室 |
>   | birthday | string | 可 | 新添加学生的手机号 | 

*   请求实例
><pre><code>{
    "student_number": "6666666666",
    "name": "delbertbeta",
    "gender": "M",
    "participation": 4
}</code></pre>

*   返回
>   | 返回参数 | 参数类型 | 参数说明 |
>   | -------- | :------- | :------- |
>   | status | string | 添加成功：<code>success</code> <br/>添加失败：<code>fail</code>|
>   | errCode | int | 错误代码<br/>资源已存在：<code>1</code><br/>其他异常：<code>0</code> |

*   返回示例
><pre><code>{
>    "code": 200,
>    "message": "OK",
>    "data": {
>        "status": "success"
>    }
>}</code></pre>

***

### <span id="delete_person">删除学生</span>

*   请求URL
>   api/delete_person

*   请求方式
>   POST

*   请求参数
>   | 请求参数 | 参数类型 | 可否为空 | 参数说明 |
>   | -------- | :------- |:--------:|:-------- |
>   | student_number | string | 否 | 删除学生的学号 | 

*   请求实例
><pre><code>{"student_number": "6666666666"}</code></pre>

*   返回
>   | 返回参数 | 参数类型 | 参数说明 |
>   | -------- | :------- | :------- |
>   | status | string | 删除成功：<code>success</code> <br/> 删除失败：<code>fail</code> |
>   | errCode | int | 错误代码<br/>资源不存在：<code>1</code><br/>其他异常：<code>0</code> |

*   返回示例
><pre><code>{
>    "code": 200,
>    "message": "OK",
>    "data": {
>        "status": "fail"
>        "errCode": 1
>    }
>}</code></pre>

***

### <span id="get_activity_list">获取活动列表</span>

*   请求URL
>   api/get_activity_list

*   请求方式
>   GET

*   请求参数
>   | 请求参数 | 参数类型 | 可否为空 | 参数说明 |
>   | -------- |:------- |:-------:|:------- |
>   | filter | string | 可 | 一个或多个关于所需活动的属性限定表达式<br/>多个表达式之间用<code>$</code>分隔<br/>为空则无限定 |
>   | count | int | 可 | 至多请求的活动数量<br/>为空则无限定 |

*   请求示例
>请求至多2个参与分为2的活动
><pre><code>api/get_activity_list?filter=participation==2&count=2</code></pre>

***

### <span id="person">学生类（Person）</span>

*   属性
>   | 属性名 | 属性说明 | 是否唯一 | 可否为空 |
>   |:------ |:-------- |:--------:|:--------:|
>   | student_number | 学号 | 是 | 不可 |
>   | name | 姓名 | 否 | 不可 |
>   | pinyin | 姓名拼音 | 否 | 不可 |
>   | gender | 性别 | 否 | 不可 |
>   | native_province | 籍贯 | 否 | 可 |
>   | dormitory | 寝室 | 否 | 可 |
>   | birthday | 生日 | 否 | 可 |
>   | phone_number | 手机号 | 是 | 可 |
>   | position | 职务 | 否 | 可 |
>   | participation | 活动参与分 | 否 | 不可 |

***

### <span id="activity">活动类（Activity）</span>

*   属性
>   | 属性名 | 属性说明 | 是否唯一 | 可否为空 |
>   |:------ |:-------- |:--------:|:--------:|
>   | id | 表内索引号 | 是 | 不可 |
>   | name | 活动名称 | 否 | 不可 |
>   | date | 日期 | 否 | 可 |
>   | time | 开始时间 | 否 | 可 |
>   | place | 地点 | 否 | 可 |
>   | content | 内容 | 否 | 可 |
>   | participation | 参与得分 | 否 | 不可（缺省为0） |
>   | participator | 参与者id（用半角逗号分隔） | 否 | 可 |
>   | images | 相关图片url（用半角逗号分隔） | 否 | 可 |