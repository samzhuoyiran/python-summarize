## 1.Jinja2模板简介
### 模板
作用:模板是承担视图函数的一个作用,返回响应内容

+ 模板其实是一个包含响应文本的文件,其中占位符(变量)表示动态部分,告诉模板引擎其具体的值需要从使用的数据库中获取
+ 使用真实值替换变量,再返回最终得到字符串,这个过程叫做"渲染"
+ Flask是使用Jinja2这个模板引擎来渲染模板

使用模板的好处

+ 视图函数只需要负责业务逻辑和数据的处理(业务逻辑方面)
+ 模板则取到视图函数的数据结果进行展示(视图展示方面)
+ 代码结构清晰,耦合度低

### Jinja2

+ JInja2 是 Python 下的一个被广泛应用的模板引擎，是由Python实现的模板语言，他的设计思想来源于 Django 的模板引擎，并扩展了其语法和一系列强大的功能，其是Flask内置的模板语言
+ 模板语言：是一种被设计来自动生成文档的简单文本格式，在模板语言中，一般都会把一些变量传给模板，替换模板的特定位置上预先定义好的占位变量名

### 渲染模板函数
+ Flask提供的render_template函数封装了该引擎模板
+ render_template函数的第一个参数是模板的文件名,后面的参数都是键值对,表示模板中变量对应的真实值

### 使用
+ {{}}来表示变量名,这种{{}}叫做**变量代码块**

      	<h1>{{ post.title }}</h1>
+ 变量代码块可以使Python中**任意类型、对象**,只要它能够被str()转换为字符串就可以
+ 用 {%%} 定义的控制代码块，可以实现一些语言层次的功能，比如循环或者if语句
	
	      {% if user %}
	          {{ user }}  
	      {% else %}
	          hello!
	      <ul>
	          {% for index in indexs %}
	          <li> {{ index }} </li>
	          {% endfor %}
	      </ul>
	      {# {{ 注释格式:不会再html中被渲染出来 }} #}
	      
### 模板的使用
+ 在项目下创建 templates 文件夹，用于存放所有的模板文件，并在目录下创建一个模板html文件 temp_demo1.html
+ 创建视图函数将该模板内容进行渲染返回

        @app.route('/')
        def index():
            return render_template('temp_demo1.html')
+ 代码中传入字符串，列表，字典到模板中

	      @app.route('/')
	      def index():
	        # 往模板中传入的数据
	        my_str = 'Hello world'
	        my_int = 10
	        my_array = [3, 4, 2, 1, 7, 9]
	        my_dict = {
	        'name': 'xiaoming',
	        'age': 18
	        }
	        return render_template('temp_demo1.html',
	                           my_str=my_str,
	                           my_int=my_int,
	                           my_array=my_array,
	                           my_dict=my_dict
	                           )
+ 模板中的代码

	      <!DOCTYPE html>
	      <html lang="en">
	      <head>
	          <meta charset="UTF-8">
	          <title>Title</title>
	      </head>
	      <body>
	      我的模板html内容
	      <br/>{{ my_str }}
	      <br/>{{ my_int }}
	      <br/>{{ my_array }}
	      <br/>{{ my_dict }}
	
	      </body>
	      </html>
+ 运行效果

	      我的模板html内容
	      Hello 黑马程序员
	      10
	      [3, 4, 2, 1, 7, 9]
	      {'name': 'xiaoming', 'age': 18}
+ 相关运算,取值

	      <br/> my_int + 10 的和为：{{ my_int + 10 }}
	      <br/> my_int + my_array第0个值的和为：{{ my_int + my_array[0] }}
	      <br/> my_array 第0个值为：{{ my_array[0] }}
	      <br/> my_array 第1个值为：{{ my_array.1 }}
	      <br/> my_dict 中 name 的值为：{{ my_dict['name'] }}
	      <br/> my_dict 中 age 的值为：{{ my_dict.age }}
+ 结果

	      my_int + 10 的和为：20
	      my_int + my_array第0个值的和为：13
	      my_array 第0个值为：3
	      my_array 第1个值为：4
	      my_dict 中 name 的值为：xiaoming
	      my_dict 中 age 的值为：18
	      
### 过滤器
过滤器的本质就是函数<br>
使用方式:
+ 变量名 | 过滤器

     	 {{variable | filter_name}}
### 链式调用

      	{{"hello world" | reverse | upper}}
      	
### 常见的内置过滤器
#### 字符串操作
+ safe:禁用转义

    	<p>{{ '<em>hello world'</em> | safe }}</p>
+ capitalize:首字母大写

      	<p>{{ 'hello' | capitalize }}</p>
+ lower:全部小写

      	<p>{{ 'hello' | lower }}</p>
+ upper:全部大写

      	<p>{{ 'hello' | upper }}</p>
+ reverse:字符串反转

      	<p>{{ 'hello' | reverse }}</p>
+ title:把值中的每个单词的首字母都转成大写

      	<p>{{ 'hello' | title }}</p>
+ format:格式化输出

      	<p>{{ '%s is %d' | format('name',17) }}</p>
      	
#### 列表操作
+ first:取第一个元素
+ last:取最后一个元素
+ length:获取列表长度
+ sum:列表求和
+ sort:列表排序

### 自定义过滤器
过滤器的本质是函数.当模板内置的过滤器不能满足需求,可以自定义过滤器.自定义过滤器有两种实现方式:

+ 一种是通过Flask应用对象的**add_template_filter**方法
+ 通过装饰器来实现自定义过滤器

**注意:自定义的过滤器,如果和内置过滤器同名,那么自定义的会覆盖掉内置的**
#### 方式一:
通过调用应用程序实例的 add_template_filter 方法实现自定义过滤器。该方法第一个参数是函数名，第二个参数是自定义的过滤器名称:

    def do_listreverse(li):
        # 通过原列表创建一个新列表
        new_li = list(li)
        # 对列表进行翻转
        new_li.reverse()
        return new_li
    # 添加自定义过滤器
    app.add_template_filter(do_listreverse,'listreverse')
#### 方式二:
用装饰器来自定义过滤器,装饰器传入的参数是过滤器的名称

    @app.template_filter('listreverse')
    def do_listreverse(li):
        # 通过原列表创建一个新列表
        new_li = list(li)
        # 对列表进行翻转
        new_li.reverse()
        return new_li    
### 控制代码块
控制代码块主要使用两个语句:

+ if / else if / else / endif
+ for / endfor

#### if语句
Jinja2 语法中的if语句跟 Python 中的 if 语句相似,后面的布尔值或返回布尔值的表达式将决定代码中的哪个流程会被执行:

    {%if user.is_logged_in() %}
        <a href='/logout'>Logout</a>
    {% else %}
        <a href='/login'>Login</a>
    {% endif %}
过滤器可以用在if语句中

    {% if comments | length > 0 %}
        There are {{ comments | length }} comments
    {% else %}
        There are no comments
    {% endif %}
#### 循环语句
+ 我们可以在Jinja2中使用循环来迭代任何列表或者生成器函数

	      {% for post in posts %}
	          <div>
	              <h1>{{ post.title }}</h1>
	              <p>{{ post.text | safe }}</p>
	          </div>
	      {% endfor %}
+ 循环和if语句可以组合使用,以模拟 Python 循环中的 continue 功能，下面这个循环将只会渲染post.text不为None的那些post:

	      {% for post in posts if post.text %}
	          <div>
	              <h1>{{ post.title }}</h1>
	              <p>{{ post.text | safe }}</p>
	          </div>
	      {% endfor %}
+ 在循环内部,你可以使用一个叫做loop的特殊变量来获得关于for循环的一些信息
  + 比如:要是我们想知道当前被迭代的元素序号,并模拟Python中的enumerate函数做的事情,则可以使用loop变量的index属性,例如:

        {% for post in posts%}
        {{loop.index}}, {{post.title}}
        {% endfor %}
        
### Web表单
Web 表单是 Web 应用程序的基本功能。

它是HTML页面中负责数据采集的部件。表单有三个部分组成：表单标签、表单域、表单按钮。表单允许用户输入数据，负责HTML页面数据采集，通过表单将用户输入的数据提交给服务器。

在Flask中，为了处理web表单，我们可以使用 Flask-WTF 扩展，它封装了 WTForms，并且它有验证表单数据的功能
#### WTForms支持的HTML标准字段
+ Stringfield:文本字段
+ TextAreaField:多行文本字段
+ PasswordField:密码文本字段
+ HiddenField:隐藏文件字段
+ DateField:文本字段，值为 datetime.date 文本格式
+ DateTimeField:文本字段，值为 datetime.datetime 文本格式
+ IntegerField:文本字段，值为整数
+ DecimalField:	文本字段，值为decimal.Decimal
+ FloatField:文本字段，值为浮点数
+ BooleanField:复选框，值为True 和 False
+ RadioField:一组单选框
+ SelectField:下拉列表
+ SelectMutipleField:下拉列表，可选择多个值
+ FileField:文件上传字段
+ SubmitField:表单提交按钮
+ FormField:把表单作为字段嵌入另一个表单
+ FieldList:一组指定类型的字段
#### WTForms常用验证函数
+ DataRequired	:确保字段中有数据
+ EqualTo:比较两个字段的值，常用于比较两次密码输入
+ Length:	验证输入的字符串长度
+ NumberRange:	验证输入的值在数字范围内
+ URL:	验证URL
+ AnyOf:	验证输入值在可选列表中
+ NoneOf:	验证输入值不在可选列表中

**使用 Flask-WTF 需要配置参数 SECRET_KEY**

CSRF_ENABLED是为了CSRF（跨站请求伪造）保护。 SECRET_KEY用来生成加密令牌，当CSRF激活的时候，该设置会根据设置的密匙生成加密令牌。
#### 使用 Flask-WTF 实现表单

    from flask import Flask,render_template, flash
    #导入wtf扩展的表单类
    from flask_wtf import FlaskForm
    #导入自定义表单需要的字段
    from wtforms import SubmitField,StringField,PasswordField
    #导入wtf扩展提供的表单验证器
    from wtforms.validators import DataRequired,EqualTo
    app = Flask(__name__)
    app.config['SECRET_KEY']='SECRET_KEY'

    #自定义表单类，文本字段、密码字段、提交按钮
    class RegisterForm(FlaskForm):
        username = StringField("用户名：", validators=[DataRequired("请输入用户名")], render_kw={"placeholder": "请输入用户名"})
        password = PasswordField("密码：", validators=[DataRequired("请输入密码")])
        password2 = PasswordField("确认密码：", validators=[DataRequired("请输入确认密码"), EqualTo("password", "两次密码不一致")])
        submit = SubmitField("注册")

    #定义根路由视图函数，生成表单对象，获取表单数据，进行表单数据验证
    @app.route('/demo2', methods=["get", "post"])
    def demo2():
        register_form = RegisterForm()
        # 验证表单
        if register_form.validate_on_submit():
            # 如果代码能走到这个地方，那么就代码表单中所有的数据都能验证成功
            username = request.form.get("username")
            password = request.form.get("password")
            password2 = request.form.get("password2")
            # 假装做注册操作
            print(username, password, password2)
            return "success"
        else:
            if request.method == "POST":
                flash("参数有误或者不完整")

        return render_template('temp_register.html', form=register_form)
    if __name__ == '__main__':
        app.run(debug=True)

### CSRF(Cross Site Request Forgery)
+ 跨站请求伪造
+ CSRF指攻击者盗用了你的身份，以你的名义发送恶意请求
  + 包括：以你名义发送邮件，发消息，盗取你的账号，甚至于购买商品，虚拟货币转账......
+ 造成的问题：个人隐私泄露以及财产安全

...


### 模板代码复用
#### 模板的继承

1. 基类中定义的多个页面的重复部分;
2. 把多个页面中重复的部分提取定义成block,区域块
3. 子类中首先使用extends继承父类,然后根据子类页面中自己需要实现的部分,进行重写
4. 子类和基类中的相同的话,直接继承
5. 继承自基类的区域块,如果为空,子类中也为空,相当于重写









