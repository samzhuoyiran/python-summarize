## Flask框架视图及路由

### 相关配置参数
一个简单的flask应用程序需要有下面的参数及运行配置
+ Flask程序初始化参数
+ Flask程序相关配置加载方式
+ app.run()参数
#### 程序初始化参数
`app = Flask(__name__)`
+ import_name--用来定位程序所在的位置,以此来确定静态文件查找的路径,一般填入`__name__`.
+ static_path--静态文件访问路径(不推荐使用,使用static_url_path代替);
+ static_url_path--静态文件访问路径，可以不传，默认为：/ + static_folder
+ static_folder--静态文件存储的文件夹，可以不传，默认为 static
+ template_folder--模板文件存储的文件夹，可以不传，默认为 templates
#### 程序加载配置
在Flask程序运行时可以给falsk设置相关配置:配置debug模式,配置数据库连接地址等.<br>
设置Flask配置有三种方式:
+ 从配置对象中加载(最常用):`app.config.from_object()`
+ 从配置文件中加载:`app.config.form_pyfile()`
+ 从环境变量中加载(了解):`app.config.from_envvar()`
#### 读取配置
Flask 应用程序将一些常用的配置设置成了应用程序对象的属性，也可以通过属性直接设置/获取某些配置：app.debug = True
+ app.config.get()
+ 在视图函数中使用 current_app.config.get()

### 路由基本定义
+ 明确路由定义的参数，请求方式指定
#### 指定路由地址
      # 指定访问路径为 demo1
      @app.route('/demo1')
        def demo1():
          return 'demo1'
#### 给路由传参
有时我们需要将同一类 URL 映射到同一个视图函数处理，比如：使用同一个视图函数来显示不同用户的个人信息.
      # 路由传递参数
      @app.route('/user/<user_id>')
      def user_info(user_id):
          return 'hello %s' % user_id
+ 路由传递的参数默认当做 string 处理，也可以指定参数的类型
      # 路由传递参数
      @app.route('/user/<int:user_id>')
      def user_info(user_id):
          return 'hello %d' % user_id
>这里指定int，尖括号中的内容是动态的，在此暂时可以理解为接受 int 类型的值，实际上 int 代表使用 IntegerConverter 去处理 url 传入的参数
#### 指定请求方式
在Flask中定义一个路由,默认的请求方式是:GET、OPTIONS(自带)、HEAD(自带)<br>
如果想添加请求方式,那可以如下指定:
      @app.route('/demo2', methods=['GET', 'POST'])
      def demo2():
          # 直接从请求中取到请求方式并返回
          return request.method

### 视图常用逻辑
+ 返回JSON
+ 重定向
  + url_for
+ 自定义状态码
#### 返回JSON
在使用 Flask 写一个接口时候需要给客户端返回 JSON 数据，在 Flask 中可以直接使用 jsonify 生成一个 JSON 的响应
      # 返回JSON  导入jsonify方法
      from flask import jsonify
      @app.route('/demo4')
      def demo4():
          json_dict = {
            "user_name":"Sam",
            "user_age":18
          }
          return josnify(json_dict)
>不推荐使用 json.dumps 转成 JSON 字符串直接返回，因为返回的数据要符合 HTTP 协议规范，如果是 JSON 需要指定 content-type:application/json

### 重定向
+ 重定向到百度
      # 重定向 导入redirect方法
      form flask import redirect
      @app.route('/demo5')
      def demo5():
          return redirect('http://www.baidu.com')
+ 重定向到自己写的视图函数
  + 也可以直接填写自己的url路径
  + 也可以使用url_for生成指定视图函数所对应的url
        form flask import Flask,redirect,url_for
        app = Flask(__name__)
        # 路由传递参数
        @app.route('/user/<int:user_id>')
        def user_info(user_id):
            return 'hello %s' % user_id
        # 重定向
        @app.route('/demo5')
        def demo5():
            return redirect(url_for('user_info',user_id=100))

### 自定义状态码
+ 在flask中可以很方便的定义状态码,以实现不符合http协议的状态码,可以用于前后端的数据交互
      # 自定义状态码
      @app.route('/demo6')
      def demo6():
          return '状态码为:666',666

### 正则匹配路由
在web开发中可能会出现限制用户访问规则的场景,那么这个时候就需要正则去匹配,根据自己的规则去限定请求参数在进行访问<br>
具体实现步骤:
+ 导入转换器基类:在Flask中所有的路由的匹配规则都是使用转换器对象进行记录
+ 自定义转换器:自定义类继承自转换器基类
+ 添加转换器到默认转换器字典中
+ 使用自定义转换器实现自定义匹配规则
#### 代码实现
+ 导入转换器基类:
      from werkzeug.routing import BaseConverter
+ 自定义转换器类:
      class RegexConverter(BaseConverter):
          def __init__(self,map,args):
              super(RegexConverter,self).__init__(map)
              # 将接受的第一个参数当做匹配规则进行保存
              self.regex = args[0]
+ 添加自定义的转换器到默认的转换器字典中,并指定转换器使用时名字为:re
      app.url_map.converter['re'] = RegexConverter
+ 使用自定义转换器实现自定义匹配规则
      @app.route('/<re("[a-z]{3}":args)>')
      def re_args(args):
          return 'hello %s' % args
### 系统自带转换器
      DEFAULT_CONVERTERS = {
      'default':          UnicodeConverter,
      'string':           UnicodeConverter,
      'any':              AnyConverter,
      'path':             PathConverter,
      'int':              IntegerConverter,
      'float':            FloatConverter,
      'uuid':             UUIDConverter,
      }
>系统自带的转换器具体使用方式在每种转换器的注释代码中有写，请留意每种转换器初始化的参数。

### 请求勾子
为了让每个视图函数避免编写重复功能的代码，Flask提供了通用设施的功能，即请求钩子
请求钩子是通过装饰器的形式实现,Flask支持如下四种请求钩子:
+ before_first_request:在处理第一个请求前执行
+ before_request:
  + 在每个请求前执行
  + 如果在某修饰的函数中返回了一个响应，视图函数将不再被调用
after_request
+ after_request:
  + 如果没有抛出错误,在每次请求后执行
  + 接受一个参数:视图函数的响应(response)
  + 在此函数中可以对响应的值作最后一次修改处理
  + 需要将参数中的响应在此参数中返回
+ teardown_request:
  + 在每次请求后执行
  + 接受一个参数:错误信息,如果有错误抛出的话

### 获取请求参数
#### request
request是flask中代表当前请求的request对象,其中一个请求上下文变量(可以理解为全局变量,在视图函数中直接使用可以取到当前本次请求)
<br>
常用请求如下:
<table>
<thead>
<tr>
<th style="text-align:left">属性</th>
<th style="text-align:left">说明</th>
<th style="text-align:left">类型</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:left">data</td>
<td style="text-align:left">记录请求的数据，并转换为字符串</td>
<td style="text-align:left">`*`</td>
</tr>
<tr>
<td style="text-align:left">form</td>
<td style="text-align:left">记录请求中的表单数据</td>
<td style="text-align:left">MultiDict</td>
</tr>
<tr>
<td style="text-align:left">args</td>
<td style="text-align:left">记录请求中的查询参数</td>
<td style="text-align:left">MultiDict</td>
</tr>
<tr>
<td style="text-align:left">cookies</td>
<td style="text-align:left">记录请求中的cookie信息</td>
<td style="text-align:left">Dict</td>
</tr>
<tr>
<td style="text-align:left">headers</td>
<td style="text-align:left">记录请求中的报文头</td>
<td style="text-align:left">EnvironHeaders</td>
</tr>
<tr>
<td style="text-align:left">method</td>
<td style="text-align:left">记录请求使用的HTTP方法</td>
<td style="text-align:left">GET/POST</td>
</tr>
<tr>
<td style="text-align:left">url</td>
<td style="text-align:left">记录请求的URL地址</td>
<td style="text-align:left">string</td>
</tr>
<tr>
<td style="text-align:left">files</td>
<td style="text-align:left">记录请求上传的文件</td>
<td style="text-align:left">`*`</td>
</tr>
</tbody>
</table>

#### 示例
+ 获取上传图片并保存到本地
      # 导入request方法
      from flask import Flask
      app = Flask(__name__)
      @app.route('/savefile',methods=['POST'])
      def save_file():
          img = req

### 状态保持
实现状态保持主要有两种:
+ 在客户端储存信息使用`cookie`
+ 在服务器端存储信息使用`session`
>无状态协议：
> 1. 协议对于事务处理没有记忆能力
> 2. 对同一个 url 请求没有上下文关系
> 3. 每次的请求都是独立的，它的执行情况和结果与前面的请求和之后的请求是无直接
关系的，它不会受前面的请求应答情况直接影响，也不会直接影响后面的请求应答情况
> 4. 服务器中没有保存客户端的状态，客户端必须每次带上自己的状态去请求服务器
> 5.人生若只如初见
#### cookie
+ cookie:指的是一些网站为了辨别用户身份,进行会话跟踪而储存在用户本地(浏览器)的数据
+ ** cookie是由服务器端生成,发送给客户端浏览器,浏览器会将cookie以key/value形式保存,下次请求同一网站时就发送该cookie给服务器 **
+ cookie的key/value值可以由服务器自己定义
+ 当浏览器请求某网站时，会将本网站下所有Cookie信息提交给服务器，所以在request中可以读取Cookie信息
#### 设置cookie
      # 导入make_response方法设置cookie
      # 导入request方法可以获取cookie
      from flask from Flask,request,make_response
      app = Flask(__name__)

      @app.route('/')
      def set_cookie():
          response = makeresponse('set cookie success')
          response.set_cookie('user_id',"sam",max_age=3600)  # 这里可以设置cookie过期时间单位秒
          return response

      @app.route('/getcookie')
      def get_cookie():
          cookie = request.get('user_id')  # 这里使用request.get通过设置的key获取value
          return cookie
#### session
+ 对于敏感、重要的信息,建议存储在服务器端,不能存储在浏览器中,如用户名、密码、余额、等级、验证码等
+ 在服务器端进行状态保持就是session
+ ** session依赖于cookie **
#### session设置cookie
      # 导入session方法
      from falsk import Flask,session
      app = Flask(__name__)
      @app.route('/session')
      def set_session_cookie():
          session['user_id'] = 'sam'
          return redirect(url_for('index'))

      @app.route('/index')
      def index():

          return session.get('user_id')
** 使用session需要设置secret_key **

### 上下文
上下文相当于一个容器,保存Flask程序运行过程中的一些信息</br>
上下文分为两种:
+ 请求上下文
+ 应用上下文

#### 1.请求上下文(request context)
  + request对象:封装了http请求的内容,针对的是http请求
  + session对象:用来记录请求会话中的信息,针对的是用户信息

#### 2.应用上下文(application context)
  + current_app:保存了程序运行的最基本环境配置信息,包括示例程序名、使用的全局变量、数据库的操作等,生命周期最长,程序执行它就存在,用来记录项目日志
  + g变量:临时储存信息,项目中用来临时储存用户信息
#### 两种上下文的区别
+ 应用上下文针对的是程序本身,请求上下文针对的是客户端和服务器端请求信息
+ 应用上下文比请求上下文的生命周期更长
+ request、session、g在请求结束后都会销毁

### 装饰器路由具体实现
Flask有两大核心:werkzeug和jinja2

    - werkzeug实现了路由、调试和web服务器网关接口
    - jinja2实现了模板
Werkzeug是一个遵循WSIG协议的python函数库

    - 其内部显现了很多web框架底层的东西,比如request和response对象
    - 与WSIG规范兼容;支持Unicode
    - 支持基本的会话管理和签名Cookie
    - 集成URL请求路由等
Werkzeug库的 routing 模块负责实现 URL 解析。不同的 URL 对应不同的视图函数，routing模块会对请求信息的URL进行解析，匹配到URL对应的视图函数，执行该函数以此生成一个响应信息。
routing模块内部有:
+ Rule类:存储了具体的URL和视图函数的映射
+ Map类:存储了所有的URL类规则
+ MapAdapter类(映射适配器):负责把URL和视图进行匹配或者说进行适配;

### Flask_Script扩展包
使用Falsk_script需要:

    # 导入扩展包、管理器
    from flask import Flask
    from flask_script import Manager

    app=Flask(__name__)
    # 实例化管理器对象将其与应用程序进行关联
    manager=Manager(app)

    @app.route('/')
    def index():
        return 'index'
    if __name__=='__main__':
        # 管理器代替app运行run方法
        manager.run()
作用:在终端可以通过命令的形式运行项目
>Flask-Script 还可以为当前应用程序添加脚本命令，后续项目中会使用到
