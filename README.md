# Django_API_Project

> **@Author:** HenrySHE
>
> **@Created Time:** 2019-06-10
>
> **@Description:** This project is a project log for learning Django API, including HTTP request (GET/POST/PUT/DELETE), and some 
>
> **@Reference Book:** *Django RESTful Web Services*
>
> **@Reference GitHub Repository**: [link](https://github.com/PacktPublishing/Django-RESTful-Web-Services)


> 创建日期: 2019-06-05
> @Author: HenrySHE
> @Books: **Django RESTful Web Services**
> @Project Code: [link](https://github.com/PacktPublishing/Django-RESTful-Web-Services)


## 前期准备

1. python 3.6 + (installed through anaconda)
2. virtualenv (同上)
3. PEP 405

## 创建Anaconda环境
>首先打开 **Anaconda Powershell Prompt !!!**  [Reference](https://blog.csdn.net/levon2018/article/details/84316088)
1. 列出环境 `conda info -e`
2. 激活环境 `conda activate DjangoEnv`

**整个流程:**
```shell
(base) PS>conda info -e
# conda environments:
#
base                  *  E:\Anaconda2
DjangoEnv                E:\Anaconda2\envs\DjangoEnv

(base) PS>conda activate DjangoEnv
(DjangoEnv) PS>python -V
Python 3.6.8 :: Anaconda, Inc.
(DjangoEnv) PS>
```

3. 创建虚拟环境(win): `python -m venv Django_API_Project` (win & Mac/Linux 不一样)
4. 进入win的虚拟环境: **先进入到那个对应虚拟环境目录(Django_API_Project)**`Scripts/activate.ps1` ,或者`Scripts/activate.bat`
5. 退出(win): `Script/deactive.bat`

```Shell
(DjangoEnv) PS>.\Scripts\activate
(Django_API_Project) (DjangoEnv) PS>
```

6. Install Django 1.11.5:  `pip install django==1.11.5`  (around 10 mins)
7. `pip install djangorestframework==3.6.4`(2 mins)
8. 创建restful01 的django项目`python .\Scripts\django-admin.py startproject restful01`
9. 进入文件夹 ` cd restful01`
10. 创建一个新的app叫做"toys" `python manage.py startapp toys`



## 理解Django文件夹,文件,配置

1. `toys/apps.py`: 定义了ToysConfig class作为 django.apps.AppConfig的子Class

2. 添加内容到`settings.py`文件夹

```python
INSTALLED_APPS = [
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',
#-------------下面是要添加的------
# Django REST framework
'rest_framework',
# Tyoys application
'toys.apps.ToysConfig',
]
```

## 安装 Tools
**安装清单:**
- Command-line tools:
    1. **CURL**
        - Win用户需要通过cygwin安装 (√)
    2. **HTTPie**
        - A command-line HTTP client (python)
        - 非常容易发送HTTP Request, easier than CURL
        - 安装: `pip install --upgrade httpie` (√)
        - 使用: `http`
- GUI tools
    1. **Postman**
        -  非常好的GUI 发送HTTP请求(√)
    2. **Stoplight**
        - 帮助model complex APIs (如果需要不同编程语言,那stoplight很有用)
    3. **iCurlHttp** (iOS App)
-  Python code
- Web browser
- JavaScript code

## Models/Migrations/Serialization序列化/Deserialization反序列化
> 目的: Perform **CRUD** (Create, Read, Update, Delete) operations on SQLite database

### 1. 确定我们第一个RESTful Web Service需求:

- An integer identifer
- A name
- An optional description 
- A toy category description (action figures, dolls or playsets)
- A release date
- A bool value indicating whether the toy has been on the online store's homepage at least once


假设:
- ` GET http://localhost:8000/toys/`是请求所有tyos (collection of toys)
- `GET http://localhost:8000/toys/42` 就是id=42的toy
- `POST http://localhost:8000/toys/` 附加一些信息就是添加toys到数据库(附加JSON数据)



### 2. 开始创建自己的Model

1. 修改 `models.py`

```python
    
from django.db import models
# Create your models here.
# Create the description of database attributes
class Toy(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=150, blank=False, default='')
    description = models.CharField(max_length=250, blank=True, default='')
    toy_category = models.CharField(max_length=200, blank=False, default='')
    release_date = models.DateTimeField()
    was_included_in_home = models.BooleanField(default= False)
    class Meta:
        ordering = ('name',)
```

注意, 在创建新的model的时候他会自动创建一个 id, 然后id 是auto increment的，所以不需要再重新定义一id 做自增。

然后跑这个命令:  `python manage.py makemigrations toys`
然后就会在`migrations`的文件夹下面发现`0001_initial.py`,里面会生成我们定义的model

### 3. Understanding Migrations
> Migration的作用就是call an function called `Migration`  
> `fields` 参数就是list of tuples 包括了 field name, field type, 和 additional attributes

执行 `python manage.py migrate`

执行过后会发现，root 文件夹下面会多了 `db.sqlite3`文件

```shell
(Django_API_Project) (DjangoEnv) PS>ls

    目录: E:\Code\Django_API_Project\restful01

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----         2019/6/5     15:46                restful01
d-----         2019/6/5     20:29                toys
-a----         2019/6/5     21:02         135168 db.sqlite3
-a----         2019/6/5     15:44            829 manage.py
```

### 4. Analyzing the database

分析数据表: 

```shell
(Django_API_Project) (DjangoEnv) PS>sqlite3 db.sqlite3 ".tables"
auth_group                  django_admin_log
auth_group_permissions      django_content_type
auth_permission             django_migrations
auth_user                   django_session
auth_user_groups            toys_toy
auth_user_user_permissions
```

Sqlite可视化数据软件: DBBrowser (http://sqlitebrowser.org), [免费下载地址](https://sqlitebrowser.org/dl/)
![7aeb84ab71911578c3b7dbc75723a07f.png](en-resource://database/5304:1)

### 5.理解Django生成的tables

查看table的schema: 
`sqlite3 db.sqlite3 ".schema toys_toy"`
结果:

```mysql
(DjangoEnv) PS>sqlite3 db.sqlite3 ".schema toys_toy"

CREATE TABLE IF NOT EXISTS "toys_toy" 
(
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "created" datetime NOT NULL,
    "name" varchar(150) NOT NULL, 
    "description" varchar(250) NOT NULL, 
    "toy_category" varchar(200) NOT NULL, 
    "release_date" datetime NOT NULL, 
    "was_included_in_home" bool NOT NULL
);
```

### 6. Controlling, serialization, deserializtion

> Our RESTful Web Service has to be able to serialize and deserialize the Toy instances into JSON representations. In Django REST framework, we just need to create a serializer class for the Toy instances to manage serialization to JSON and deserialization from JSON. Now, we will dive deep into the serialization and deserialization process in Django REST framework. It is very important to understand how it works because it is one of the most important components for all the RESTful Web Services we will build.
> 我们的RESTful Web服务必须能够将Toy**实例序列化和反序列化为JSON表示**。 在Django REST框架中，我们只需要为Toy实例创建一个序列化器类来管理JSON的序列化和JSON的反序列化。 现在，我们将深入研究Django REST框架中的序列化和反序列化过程。 理解它是如何工作非常重要，因为它是我们将构建的所有RESTful Web服务最重要的组件之一。
> 
> Django REST framework uses a two-phase process for serialization. The serializers are mediators between the model instances and Python primitives. Parser and renderers handle as mediators between Python primitives and HTTP requests and responses. We will configure our mediator between the Toy model instances and Python primitives by creating a subclass of the rest_framework.serializers.Serializer class to declare the fields and the necessary methods to manage serialization and deserialization
> Django REST框架使用两阶段进程进行序列化。 序列化器是模型实例和Python原语之间的中介。 解析器和渲染器处理Python原语和HTTP请求和响应之间的调解器。 我们将通过创建rest_framework.serializers.Serializer类的子类来配置玩家模型实例和Python基元之间的中介，以声明字段和管理序列化和反序列化的必要方法

进入shell模式: `python manage.py shell`

将数据进行序列化(转换成JSON格式,例如将toy1变成JSON对象,打印出来如下)

``` shell
>>> serializer_for_toy1 = ToySerializer(toy1)
>>> print(serializer_for_toy1.data)
{
    'pk': 1, 
    'name': 'Snoopy talking action figure', 
    'description': 'Snoopy speaks five languages', 
    'release_date': '2019-06-06T14:16:43.000742Z', 
    'toy_category': 'Action figures', 
    'was_included_in_home': False
}
```

将数据转换成JSON对象：
```python
json_renderer = JSONRenderer()
toy1_rendered_into_json = json_renderer.render(serializer_for_toy1.data)
toy2_rendered_into_json = json_renderer.render(serializer_for_toy2.data)
print(toy1_rendered_into_json)
#b'{"pk":1,"name":"Snoopy talking action figure","description":"Snoopy speaks five languages","release_date":"2019-06-06T14:16:43.000742Z","toy_category":"Action figures","was_included_in_home":false}'
print(toy2_rendered_into_json)
#b'{"pk":2,"name":"Hawaiian Barbie","description":"Barbie loves Hawaii","release_date":"2019-06-06T14:16:43.000742Z","toy_category":"Dolls","was_included_in_home":true}'
```

```python
# 添加新的toy对象(用JSON格式)
json_string_for_new_toy = '{"name":"Clash Royale play set","description":"6 figures from Clash Royale", "release_date":"2017-10-09T12:10:00.776594Z","toy_category":"Playset","was_included_in_home":false}'
json_bytes_for_new_toy = bytes(json_string_for_new_toy, encoding="UTF-8")

stream_for_new_toy = BytesIO(json_bytes_for_new_toy)

parser = JSONParser()
parsed_new_toy = parser.parse(stream_for_new_toy)
print(parsed_new_toy)
# {'name': 'Clash Royale play set', 'description': '6 figures from Clash Royale', 'release_date': '2017-10-09T12:10:00.776594Z', 'toy_category': 'Playset', 'was_included_in_home': False}

#插入新的数据
>>> new_toy_serializer = ToySerializer(data=parsed_new_toy)
>>> if new_toy_serializer.is_valid():
...     toy3 = new_toy_serializer.save()
...     print(toy3.name)
...
Clash Royale play set
```

## Create API Views

1. Change `view.py` 编辑Function, 处理请求,包括GET, POST, DELETE, 或者PUT. [项目代码](https://github.com/PacktPublishing/Django-RESTful-Web-Services/blob/master/Chapter03/hillar_django_restful_03_01/restful01/toys/views.py)

## Routing URLs to Django views and functions

> 1. 创建`toys/urls.py`, 然后定义了正则表达式
> 2. 修改上级文件夹`restful01/urls.py`

## Launching Django's development server
运行server: `python manage.py runserver` 运行 127.0.0.1:8000端口
或者`python manage.py runserver 0.0.0.0:8000`  (但是Office Wifi禁止访问)

运行结果:

```shell
(Django_API_Project) (DjangoEnv) PS>python manage.py runserver
Performing system checks...

System check identified no issues (0 silenced).
June 06, 2019 - 16:57:28
Django version 1.11.5, using settings 'restful01.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
Not Found: /
[06/Jun/2019 16:57:34] "GET / HTTP/1.1" 404 2137
[06/Jun/2019 16:58:02] "GET /toys/ HTTP/1.1" 200 548
```

## HTTP 请求篇

###  1. HTTP GET请求所有实例(instance)

访问 `http://127.0.0.1:8000/toys`会返回所有的toys代码(JSON Format):
```JSON
[{
	"pk": 3,
	"name": "Clash Royale play set",
	"description": "6 figures from Clash Royale",
	"release_date": "2017-10-09T12:10:00.776594Z",
	"toy_category": "Playset",
	"was_included_in_home": false
}, {
	"pk": 2,
	"name": "Hawaiian Barbie",
	"description": "Barbie loves Hawaii",
	"release_date": "2019-06-06T14:16:43.000742Z",
	"toy_category": "Dolls",
	"was_included_in_home": true
}, {
	"pk": 1,
	"name": "Snoopy talking action figure",
	"description": "Snoopy speaks five languages",
	"release_date": "2019-06-06T14:16:43.000742Z",
	"toy_category": "Action figures",
	"was_included_in_home": false
}]
```

**用curl/http去测试请求:(注意最后有反斜杠,不然会返回301)**

1. curl: `curl -iX GET 127.0.0.1:8000/toys/`

2. http: `http :8000/toys/` (or `http 127.0.0.1:8000/toys/`)


(`http -b :8000/toys/` 是去除header的命令)

### 2. HTTP GET请求单个instance

1. `http :8000/toys/3` (请求pk=3的数据)

2. 尝试请求不存在的pk值: `http :8000/toys/17500`


### 3. HTTP POST请求(创建新的实例)

1. http POST创建一个数据(植物大战僵尸)

```shell
http POST :8000/toys/ name="PvZ 2 puzzle" description="plants vs zombies 2 puzzle" toy_category="Puzzle" was_included_in_home=false release_date="2017-10-08T01:01:00.776594Z"
```


2. curl POST 数据 (可以放JSON格式数据），但是要加入content-type，并声明是JSON格式
```shell
curl -iX POST -H "Content-Type: application/json" -d '{"name":"PvZ 2 puzzle","description":"Plants vs Zombies 2 puzzle","toy_category":"Puzzle","was_included_in_home":"false","release_date":"2017-10-08T01:01:00.776594Z"}' localhost:8000/toys/
```

3. 查询插入的pk=4的value `http :8000/toys/4`


### 4. HTTP PUT 请求
> Sending update request (to update the previously added toy data)

1. http 请求去更新一个（记得所有的内容都要敲上去）
```shell
http PUT :8000/toys/4 name="PvZ 3 puzzle" description="plants vs zombies 3 puzzle" toy_category="Puzzle" was_included_in_home=false release_date="2017-10-08T01:01:00.776594Z"
```


2. 用curl 去PUT去： （失败了）

```shell
curl -iX PUT -H "Content-Type: application/json" -d '{"name":"PvZ 5 puzzle"}' localhost:8000/toys/4
```

### 5. HTTP DELETE 请求

1. http: `http DELETE :8000/toys/4`
删除后就回发现pk=4的数据被删除了；


2. curl `curl -iX DELETE localhost:8000/toys/4`


## Using Generalized Behavior form the APIView Class 
> **使用广义行为形成APIView类**: make it work with diverse content types <u>"without writing a huge amount of code"</u>
> 我们需要明白：

### 1. Taking advantage of model serializers

> Old code `seralizers.py` has many redundant code, 需要重复多次declear 参数，所以用新的方式去重新写这个code，这样少定义很多代码。


```python

from rest_framework import serializers
from toys.models import Toy

class ToySerializer(serializers.ModelSerializer):
        class Meta:
            model = Toy
            fields = ('id',
                'name',
                'description',
                'release_date',
                'toy_category',
                'was_included_in_home')
```
它定义了两个东西: `model` 就是引入Toy这个模块; 另外就是`fields`,declear a tuple of string values indicate the field names；对比旧的Code的不同是，它不需要implement `create` 和`update`两个函数`ModelSerializer`可以implement这两个funcion

### 2. Understanding accepted and returned content types

1. `http :8000/toys/ Accept:text/html` 获取JSon格式内容: `http :8000/toys/ Accept:application/json`
2. `curl -H "Accept: text/html" -iX GET localhost:8000/toys"`获取JSon格式内容: `curl -H "Accept:  application/json" -iX GET localhost:8000/toys"`



### 3. Making unsupported HTTP OPTIONS requests with command-line tools

> 查看options, 如果我们不知道哪个HTTP Method是可以被支持的

`http OPTIONS :8000/toys`  或者 `curl -iX OPTIONS localhost:8000/toys/`




### 4. Understanding decorators that work as wrappers

> **理解作为包装器的装饰器**: 更改 `toys/views.py`文件去支持OPTIONS verb在我们的RESTful Web Service
> **Decorator装饰器**是Django REST Framework自带的，我们要用`rest_framework.decorator`模块里面的`@api_view` decoratror，然后应用到`toys_list`和`toys_detail`里面
> **@api_view修饰器**: 它可以让我们去生命那些是HTTP verbs 可以处理的；然后请求了个不存在的请求，会返回`HTTP 405 Method Not Allowed`状态码


### 5. Using decorators to enable different parsers and renders
> **使用装饰器启用不同的解析器和渲染:** 只需要修改`views.py`文件去声明代码；


**变化:** 
- 去除了`JSONResponse`改用更加generic `rest_framework.response.Response`
- 去除了`rest_framework.parsers.JSONParser`


### 6. Taking advantage of content negotiation classes
> **利用内容协商类**:  `APIView` class 定义了default settings(for each views)
 

1. `DEFAULT_PARSER_CLASSES` 声明了class that we went to use for parsing backend，包括：
    - `JSONParser` : application/json
    - `FormParser` : application/x-www-form-urlencoded
    - `MultiPartParser` : multipart/form-data

    当access `request.data`的时候, 会检验the value of `Content-Type` Header，然后决定哪个parser去接纳这个数据

2. `DEFAULT_RENDERER_CLASSES` 决定了render backend, 包括:
    - `JSONRenderer`: application/json
    - `BrowsableAPIRenderer`: text/html
 

### 7. Making supported HTTP OPTIONS requests with command-line tools

1.  查看OPTIONS: `http OPTIONS :8000/toys` 会出现以下的内容:

```shell
(Django_API_Project) (DjangoEnv) E:\Code\Django_API_Project\restful01>http OPTIONS :8000/toys/
HTTP/1.0 200 OK
Allow: POST, OPTIONS, GET
Content-Length: 167
Content-Type: application/json
Date: Tue, 11 Jun 2019 02:21:41 GMT
Server: WSGIServer/0.2 CPython/3.6.8
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

{
    "description": "",
    "name": "Toy List",
    "parses": [
        "application/json",
        "application/x-www-form-urlencoded",
        "multipart/form-data"
    ],
    "renders": [
        "application/json",
        "text/html"
    ]
}
```


2. 或者`curl -iX OPTIONS localhost:8000/toys/` 查看options

3. 获取指定toys pk的OPTION: `http OPTIONS :8000/toys/2`


### 8. Working with different content types

> 在现实情况下,不止只能接收JSON格式的数据, 还需要有`application/x-www-form-urlencoded`和`multipart/form-data` (在POST和PUT两个请求里面specified的)

1. POST through HTTP
```shell
http -f POST :8000/toys/ name="ken in Rome" description="ken loves Rome" toy_category="Dolls" release_date="2017-10-09T12:11:37.090335Z" was_included_in_home=false
```


2. POST through curl **(还没测试)**
```shell
curl -iX POST -d '{"name":"ken inRome", "description": "ken loves Rome", "toy_category":"Dolls", "release_date": "2017-10-09T12:11:37.090335Z", "was_included_in_home": false}' localhost:8000/toys/
```

### 9. Sending HTTP requests with unsupported HTTP verbs

1. http: `http PATCH :8000/toys/` → Method Not Allowed

2. curl: `curl -iX PATCH lacalhost:8000/toys/`


## Understanding and Customizing the Browsable API Feature

> Key Word: **Browsable API**

1. Understanding the possibility of rendering text/HTML content
2. Using a web browser to work with our web service 
3. Making HTTP GET requests with the browsable API 
4. Making HTTP POST requests with the browsable API 
5. Making HTTP PUT requests with the browsable API 
6. Making HTTP DELETE requests with the browsable API 
7. Making HTTP OPTIONS requests with the browsable API

### 1. Understanding the possibility of rendering text/HTML content


> `rest_framework.response.BrowsableAPIRenderer` 类 负责rendering the `text/html`内容

1. Retrieve all toys with `Accept` request header key set to `text/html`
`http -v :8000/toys/ "Accept:text/html"` 或者 `curl -vH "Accept: text/html" -iX GET localhost:8000/toys/`

### 2. Using a web browser to work with our web service 

web 端访问，有UI界面；访问所有Toys数据：

访问个别数据（PK=5）

### 3. Making HTTP GET requests with the browsable API 

`GET`下拉菜单下面选择`json`
选择JSON格式数据: 浏览器输入`http://localhost:8000/toys/5?format=json`


### 4. Making HTTP POST requests with the browsable API 
在 `localhost:8000/toys/`页面下选择`application/x-www-form-urlencoded` 格式，然后输入以下JSON内容： 
```JSON
{
    "name": "Surfer girl",
    "description": "Surfer girl doll",
    "toy_category" : "Dolls",
    "was_included_in_home": "false",
    "release_date": "2017-10-29T12:11:25.090335Z"
}
```

**POST之后结果:**



### 5. Making HTTP PUT requests with the browsable API 

在 `localhost:8000/toys/6`下面,更新JSON **(注意不要加id,因为id是自增的,不能修改)**, 然后点击PUT即可

### 6. Making HTTP DELETE requests with the browsable API 

删除直接点击对应pk值的数据点击DELETE按钮



### 7. Making HTTP OPTIONS requests with the browsable API
1. 看详细toys的信息:

2. 点击OPTIONS之后:


## Working with Advanced Relationships and Serialization

> 这章会create complex RESTful Web Service, present data in PostgreSQL database

1. Defining the requirements for a complex RESTful Web Service 
2. Creating a new app with Django 
3. Configuring a new web service 
4. Defining many-to-one relationships with models.ForeignKey 
5. Installing PostgreSQL 
6. Running migrations that generate relationships 
7. Analyzing the database 
8. Configuring serialization and deserialization with relationships 
9. Defining hyperlinks with 
10. Working with class-based views 
11. Taking advantage of generic classes and generic views 
12. Generalizing and mixing behavior
13. Working with routing and endpoints 
14. Making requests that interact with resources that have relationships



### 1. Defining the requirements for a complex RESTful Web Service (P174/426)
> We want to deal with more complex database model (目前交互的是single database table)
> Add new database (关于Drone无人机的,有很多数据要存储、要获取、存储、删除)

**Drone Data:**
1. `DroneCategory`表: 只需要个name
2. `Drone` 表： 
    1. Foreign key to `DroneCategory`
    2. Name
    3. Manufacutring date
    4. A bool value indicating whether the drone participated in at least one competition or not
    5. A timestamp with date and time (when does this drone info be added into database)
3. `Pilot`表：
    1. Name
    2. Gender value
    3. Int value with num of races in which the pilot participated
    4. A timestamp with date and time (when does this drone info be added into database)
4. `Competitions`表：
    1. Foreign key to `Pilot`
    2. Foreign key to `Drone`
    3. Distance value(feet为单位)
    4. A date in which the drone controlled by the pilot reached the specified distance value
    
假设我们要用`GET http://localhost:8000/competitions` 去获取所有stored competitions in the collection.另外我们要用PostgreSQL

### 2. Creating a new app with Django 

1. 进入`restful01`文件夹, 然后`python manage.py startapp drones`

### 3. Configuring a new web service

1. 添加进`settings.py`

### 4. Defining many-to-one relationships with models.ForeignKey 

更改`drones/models.py` file: → [源代码](https://github.com/PacktPublishing/Django-RESTful-Web-Services/blob/master/Chapter07/hillar_django_restful_07_01/restful01/drones/models.py)

主要就是一下几个模块:(models)
1. DroneCategory
2. Drone
3. Pilot
4. Competition

**代码解读**
- `Meta` 定义了ordering attribute
- `__str__`方法返回每个model返回的名字
- `ForeignKey`提供了many-to one relationship to `DroneCategory` model.
- 因为希望在一个数据删除之后,对应的内容都删除,所以声明`models.CASCADE`在`on_delete` 参数定义时


### 5. Installing PostgreSQL 

> There are interactive installers built by **EnterpriseDB** and **BigSQL** for macOS and Windows. In case you are working with macOS, Postgres.app provides a really easy way to install and use PostgreSQL on this operating system. You can read more about Postgres.app and download It from its web page: <u>http://postgresapp.com</u>

-  根据菜鸟学院的教程安装的 [安装教程](https://www.runoob.com/postgresql/windows-install-postgresql.html)
- PostgreSQL [下载网址](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
 
安装路径： `C:\Program Files\PostgreSQL\9.6`
Data文件路径： `C:\Program Files\PostgreSQL\9.6\data`
Password: `DjangoAPI`
Port: `5432`

打开方式: 在`postgreSQL` 找到`pgAdmin 4`打开即可

Shell方式访问数据库:


```
Server [localhost]:
Database [postgres]:
Port [5432]:
Username [postgres]:
用户 postgres 的口令：
psql (9.6.13)
输入 "help" 来获取帮助信息.
```

### 6. Running migrations that generate relationships 

1. 创建数据库,名字为drones 命令: `createdb drones`
2. 修改`settings.py`文件
3. 修改`urls.py`文件, 去除toys相关的东西
4. 安装`psycopg2` : `pip install psycopg2`
5. 开始migrate: `python manage.py makemigrations drones`
6. 正式apply all migrations: `python manage.py migrate`


### 7. Analyzing the database 

1. 查看数据库表: (在shell里面查看)`psql --username=postgres --dbname=drones --command="\dt"`

    
### 8. Configuring serialization and deserialization with relationships 

1. 更新`restful01/drones`,创建`serializers.py`然后声明新的`DroneCategorySerializer`类

### 9. Defining many-to-one relationships with models.ForeignKey 

1. 添加代码到`serializers.py`然后声明新的`DroneSerializer`类




### 10. Working with class-based views 

Create two class views:
- `ListCreateAPIView`: 实现GET,所有listing of a queryset, POST creates a model instance
- `RetrieveUpdateDestroyAPIView`: GET, DELETE, PUT, PATCH 操作instance


### 11. Taking advantage of generic classes and generic views 

1. Update `drones/views.py`[代码连接](https://github.com/PacktPublishing/Django-RESTful-Web-Services/blob/master/Chapter07/hillar_django_restful_07_01/restful01/drones/serializers.py)

### 12. Generalizing and mixing behavior


### 13. Working with routing and endpoints 
> We want to create an endpoint for the root of our web service to make it easy to browse the resource collections and resources provided by our web service with the browsable API feature and understand how everything works. Add the following code to the `views.py` file In the `restful01/drones` folder to declare the ApiRoot class as a subclass of the generics.GenericAPIView class. The code file for the sample is included in the `hillar_django_restful_06_01` folder in the `restful01/drones/views.py` file:

1. Add function to `drones/views.py`
2. 在`drones`文件夹下New file called `urls.py` → 应该是
3. 更改`restful01`文件夹下的`urls.py`文件

### 14. Making requests that interact with resources that have relationships
1. HTTP添加Drone种类:`http POST :8000/drone-categories/ name="Quadcopter"`

```shell
(Django_API_Project) (DjangoEnv) PS>http POST :8000/drone-categories/ name="Quadcopter"
HTTP/1.0 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 89
Content-Type: application/json
Date: Wed, 12 Jun 2019 10:30:36 GMT
Location: http://localhost:8000/drone-categories/1
Server: WSGIServer/0.2 CPython/3.6.8
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

{
    "drones": [],
    "name": "Quadcopter",
    "pk": 1,
    "url": "http://localhost:8000/drone-categories/1"
}
```




2. HTTP POST Drones数据

`http POST :8000/drones/ name="WonderDrone" drone_category="Quadcopter" manufacturing_date="2017-07-20T02:02:00.716312Z" has_it_completed="false"`

输入结果:


3. HTTP POST Drones数据

`http POST :8000/drones/ name="Atom" drone_category="Quadcopter" manufacturing_date="2017-08-18T02:02:00.716312Z" has_it_completed="false"`

存储结果:


----
#### 14.1 PostgreSQL数据库操作: 

教程链接: [link](https://chartio.com/resources/tutorials/how-to-list-databases-and-tables-in-postgresql-using-psql/)

1. Listing列出数据库: `\l`

2. Switch数据库(Connect): `\c` 

3. List数据库里面的表: `\dt`


#### 14.2 查询数据表里面的内容:

1. 列出所有category
2. 查询所有drone
    


----

#### 14.3  HTTP 访问对应数据\
    - 我们可以看看到, `DroneCategorySerializer`类定义了`drone`attribute作为`HyperlinkedRelatedField`, 所以serializer呈递了所有相关的`Drone`实例的URL进这个`drones`的Array里面。
    
    
#### 14.4 POST Pilot信息: 
```shell
http POST :8000/pilots/ name="Penelope Pitstop" gender="F" races_count=0
http POST :8000/pilots/ name="Peter Perfect" gender="M" races_count=0
```


#### 14.5 POST Competition信息:

```shell
http POST :8000/competitions/ distance_in_feet=800 distance_achievement_date="2017-10-20T05:03:20.776594Z" drone="Atom" pilot="Penelope Pitstop"

http POST :8000/competitions/ distance_in_feet=2800 distance_achievement_date="2017-10-21T06:02:23.776594Z" drone="WonderDrone" pilot="Penelope Pitstop"

http POST :8000/competitions/ distance_in_feet=790 distance_achievement_date="2017-10-20T05:43:20.776594Z" drone="Atom" pilot="Peter Perfect"
```




#### 14.6 psql列出所有表
结果如下(具体的sql语句直接看图吧):



## Using Constraints, Filtering, Searching, Ordering, and Pagination

> **这一章节我们将学会:**
> 在本章中，我们将利用Django REST框架中包含的许多功能，为RESTful Web服务添加约**束，分页，过滤，搜索和排序功能。** 我们将使用几行代码添加大量功能我们将了解：
> 1. Browsing the API with resources and relationships 使用资源和关系浏览API
> 2. Defining unique constraints 定义唯一约束
> 3. Working with unique constraints 使用独特的约束
> 4. Understanding pagination 了解分页
> 5. Configuring pagination classes 配置分页类
> 6. Making requests that paginate results 发出分页结果的请求
> 7. Working with customized pagination classes 使用自定义分页类
> 8. Making requests that use customized paginated results 发出使用自定义分页结果的请求
> 9. Configuring filter backend classes 配置过滤后端类
> 10. Adding filtering, searching, and ordering 添加过滤，搜索和排序
> 11. Working with different Types of Django filters 使用不同类型的Django过滤器
> 12. Making requests that filter results 发出过滤结果的请求
> 13. Composing requests that filter and order results 撰写过滤和订购结果的请求
> 14. Making requests that perform starts with searches 执行请求以搜索开始
> 15. Using the browsable API to test pagination, filtering, searching, and ordering 使用可浏览的API测试分页，过滤，搜索和排序


### 1. Browsing the API with resources and relationships 使用资源和关系浏览API

- `http://localhost:8000/drone-categories/` 查看所有种类
- `http://localhost:8000/drones/`查看所有drones
- `http://localhost:8000/pilots/`查看所有pilots
- `http://localhost:8000/competitions/`查看所有比赛

在这些网站下面我们可以非常方便地访问、修改（在有特定`pk`值的地方对某行数据进行修改）、新增数据（在总的页面下POST新数据）

### 2. Defining unique constraints 定义唯一约束

> 如果不设定constraints, 有可能会出现很多重复的categories **with same name**. 为了避免了这种情况, 我们要添加contraints.

1. 修改`drones/models.py` 将数据添加前提条件设定为: `unique=True`
2. 运行migrate等操作

### 3. Working with unique constraints 使用独特的约束
1. 尝试存一个已经存在的category:

### 4. Understanding pagination 了解分页
> 目前数据量非常小, 所以可以直接显示; 但是如果数据量达到100+级别,可能就需要pagination来帮我们进行分页操作了, 在GET操作进行的时候需要声明哪一个pice需要被获取, 另外一个实现方法就是通过设定offset & limit,就是从第几个开始,获取多少数据

### 5. Configuring pagination classes 配置分页类

1. 配置`restful01/settings.py`文件, 末尾配置page_size等信息;
```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 4
    }
```
2. 先POST一个新的categories:

3. 插入多行数据:
```shell
http POST :8000/drones/ name="Need for Speed" drone_category="Quadcopter" manufacturing_date="2017-02-18T02:02:00.716312Z" has_it_completed="false"

http POST :8000/drones/ name="Eclipse" drone_category="Octocopter" manufacturing_date="2017-02-18T02:02:00.716312Z" has_it_completed="false"

http POST :8000/drones/ name="Gossamer Albatross" drone_category="Quadcopter" manufacturing_date="2017-02-18T02:02:00.716312Z" has_it_completed="false"

http POST :8000/drones/ name="Dassault Falcon 7X" drone_category="Octocopter" manufacturing_date="2017-04-18T02:02:00.716312Z" has_it_completed="false"

http POST :8000/drones/ name="Gulfstream I" drone_category="Quadcopter" manufacturing_date="2017-02-18T02:02:00.716312Z" has_it_completed="false"

http POST :8000/drones/ name="RV-3" drone_category="Octocopter" manufacturing_date="2017-02-18T02:02:00.716312Z" has_it_completed="false"

http POST :8000/drones/ name="Dusty" drone_category="Quadcopter" manufacturing_date="2017-07-20T02:02:00.716312Z" has_it_completed="false"

http POST :8000/drones/ name="Ripslinger" drone_category="Octocopter" manufacturing_date="2017-02-18T02:02:00.716312Z" has_it_completed="false"

http POST :8000/drones/ name="Skipper" drone_category="Quadcopter" manufacturing_date="2017-02-18T02:02:00.716312Z" has_it_completed="false"

```

插入结果:

查看网页的数据: (每个categories下面的所有数据)

网页查看所有drones数据 `/drones/`




### 6. Making requests that paginate results 发出分页结果的请求

`http GET ":8000/drones/?limit=5&offset=2"`

### 7. Working with customized pagination classes 使用自定义分页类

1. `restful01/drones`下创建新文件`custompagination.py`
2. 更改`restful01/settings.y`文件
3. run server


### 8. Making requests that use customized paginated results 发出使用自定义分页结果的请求

1. 查询:`http GET ":8000/drones/?limit=500"`
效果:

上面的图`limit=500`但是显示的只有8条数据,就是前面定义的8条限制

### 9. Configuring filter backend classes 配置过滤后端类

1. 安装django-filter `pip install django-filter`

2. 在`settings.py`文件里面加入相应的代码, (07_03上面有代码)

### 10. Adding filtering, searching, and ordering 添加过滤，搜索和排序

1. 更新`drones/views.py`

### 11. Working with different Types of Django filters 使用不同类型的Django过滤器

1. Add `CompetitionFilter` class

### 12. Making requests that filter results 发出过滤结果的请求
1. 请求,搜索 `http ":8000/drone-categories/?name=Quadcopter"`


### 13. Composing requests that filter and order results 撰写过滤和订购结果的请求
> 现在制作更加复杂的, 加上请求条件, 看能否获取到值(这样就不用获取所有数据然后再进行过滤整理)

1.  寻找`category = Quadcopter`, 而且 `has_it_competed=False`, 顺/逆序 排列

访问`http://localhost:8000/drones/?drone_category=1&has_it_competed=False&ordering=-name`
(根据名字逆序排列)

访问`http://localhost:8000/drones/?drone_category=1&has_it_competed=False&ordering=+name`


2. 进行更复杂的搜索: 
http ":8000/competitions/?pilot_name=Penelope+Pitstop&drone_name=WonderDrone" 
出问题了




### 14. Making requests that perform starts with searches 执行请求以搜索开始

1. `http :8000/drones/?search=G"`

### 15. Using the browsable API to test pagination, filtering, searching, and ordering 使用可浏览的API测试分页，过滤，搜索和排序

有问题


## Securing the API with Authentiation and Permissions

> 在本章中，我们将介绍Django REST框架中身份验证和权限之间的差异。 我们将通过添加身份验证方案的要求和指定权限策略来开始保护RESTful Web服务。 我们会理解：

1. Understanding authentication and permissions in Django, the Django REST framework, and RESTful Web Services 了解Django，Django REST框架和RESTful Web服务中的身份验证和权限
2. Authentication classes 认证课程
3. Security and permissions-related data to models 与模型相关的安全性和权限相关数据
4. Working with object-level permissions via customized permission classes 通过自定义权限类处理对象级权限
5. Saving information about users that make requests 保存有关发出请求的用户的信息
6. Setting permissions policies 设置权限策略
7. Creating the superuser for Django 为Django创建超级用户
8. Creating a user for Django 为Django创建用户
9. Making authenticated requests 进行身份验证请求
10. Browsing the secured API with the required authentication 使用所需的身份验证浏览安全的API
11. Working with token-based authentication 使用基于令牌的身份验证
12. Generating and using tokens 生成和使用令牌


### 1. Understanding authentication and permissions in Django, the Django REST framework, and RESTful Web Services 了解Django，Django REST框架和RESTful Web服务中的身份验证和权限

> 在前面的请求都是不需要验证身份的，这样做的话意味着所有人都可以请求数据，但是事实上这样是不安全的；所有用户都能请求，就可能会遭到攻击； 通过override方法改写setting,取实行Authentication.

### 2. Learning about the Authentication classes 认证课程

Django提供了集中classes在`rest_framework.authentication`模块:
1. `BasicAuthentication`:  HTTP basic authenticaiton against a username and a pwd
2. `SessionAuthentication`: Work with Django's session framework
3. `TokenAuthentication`: simple token-based authentication

步骤: 
1. 修改 `restful01/restful01/settings.py` 文件

### 3. Including security and permissions-related data to models 引入与模型相关的安全性和权限相关数据

1. 修改`restful01/drones/models.py` file
2. Edit `drones/serializers.py` file


### 4. Working with object-level permissions via customized permission classes 通过自定义权限类处理对象级权限

1. create new file `custompermission.py`


----

