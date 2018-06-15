## Django中的类视图与中间件
### 类视图
**1 类视图的引入**

以函数的方式定义的视图成为**函数视图（FBV）**：

+ 便于理解
+ 但遇到一个视图对应的路径提供了多种不同HTTP请求方式的支持时，便需要在一个函数中编写不同的业务逻辑，代码可读性与复用性都不佳

在Django中也可以使用类来定义一个视图，称为**类视图（CBV）**：

使用类视图可以将视图对应的不同请求方式以类中的不同方法来区别定义

+ 代码的可读性更好
+ 类视图相对于函数视图有更高的复用性，例如：其他地方需要用到某个类视图的某个特定逻辑，直接继承该类视图即可

**2 类视图的使用**

定义类视图需要继承自Django提供的父类**View**

**配置路由时，使用类视图的`as_view（）`**方法来转化为一个视图函数

	urlpatterns = [
	    url(r'^register/$', views.Register.as_view(), name='register'),
	]
**3 类视图使用装饰器**

为类视图添加装饰器，可以使用三种方法

我们先准备一个为函数视图的装饰器

	def my_decorator(func):
		def wrapper(request, *args, **kwargs):
			print('in decorator')
			print(request.path)
			return func(request, *args, **kwargs)
		return wrapper
	
	class DemoView(View):
	    def get(self, request):
	        print('is get')
	        return HttpResponse('ok')
	
	    def post(self, request):
	        print('is post')
	        return HttpResponse('ok')

3.1 在类视图中装饰

	urlpatterns = [
	    url(r'^demo/$', my_decorate(DemoView.as_view()))
	]
	
此种方式会为类视图中的所有请求方法都加上装饰器行为（在视图入口处，分发请求之前），但是这种装饰行为被放到了URL配置中，这样单看视图是不好理解的，不利于代码的完整性，不建议使用

3.2 在类视图中装饰

在类视图中使用为函数视图准备的装饰器时，不能直接添加装饰器，需要使用method_decorator将其转换为适用于类视图方法的装饰器。

	from django.utils.decorators import method_decorator    
	# 为特定请求方法添加装饰器
	class DemoView(View):
	
	    @method_decorator(my_decorator)
	    def dispatch(self, *args, **kwargs):
	        return super().dispatch(*args, **kwargs)
	
	    def get(self, request):
	        print('is get')
	        return HttpResponse('ok')
	
	    def post(self, request):
	        print('is post')
        return HttpResponse('ok')
        
**method_decorator装饰器还支持使用name参数指明被装饰的方法**

	# 为特定请求方法添加装饰器
	@method_decorator(my_decorator, name='dispatch')
	class DemoView(View):
	
	    def dispatch(self, *args, **kwargs):
	        return super().dispatch(*args, **kwargs)
	
	    def get(self, request):
	        print('is get')
	        return HttpResponse('ok')
	
	    def post(self, request):
	        print('is post')
	        return HttpResponse('ok')
	        
**3.3 构造Mixin扩展类**

使用面向对象多继承的特性

	class MyDecoratorMixin(object):
	       def get(self, request):
	        print('is get')
	        return HttpResponse('ok')
	
	class DemoView(MyDecoratorMixin, View):
	
	    def post(self, request):
	        print('is post')
	        return HttpResponse('ok')
	        
	        
### 中间件

django的中间件是一个轻量级、底层的插件系统，，可以介入Django的请求和响应处理过程，修改Django的输入或输出。中间件的设计为开发者提供了一种无侵入式的开发方式，增强了Django框架的健壮性。

我们可以使用中间件，在Django处理视图的不同阶段对输入或输出进行干预。

**1 中间件的定义方法**

可以定义一个中间件工厂函数，然后返回一个可以被调用的中间件

中间价工厂函数需要接受一个可以调用的get_response对象

返回的中间件也是一个可以被调用的对象，并且像视图一样需要接受一个request对象参数，返回一个response对象

	def simple_middleware(get_response):
		# 此处编写的代码尽在Django第一次配置和初始化的时候执行一次
		
		def middleware(request):
			# 此处编写的代码会在每次请求处理视图前被调用
			response = get_response(request)
			# 此处编写的代码会在每个	请求处理视图之后调用
			return response
		return middleware
		
**我们自定义的中间件完成之后，需要在项目同名文件夹中的settings.py文件中添加注册中间件**

	MIDDLEWARE = [
	    'django.middleware.security.SecurityMiddleware',
	    'django.contrib.sessions.middleware.SessionMiddleware',
	    'django.middleware.common.CommonMiddleware',
	    'django.middleware.csrf.CsrfViewMiddleware',
	    'django.contrib.auth.middleware.AuthenticationMiddleware',
	    'django.contrib.messages.middleware.MessageMiddleware',
	    'django.middleware.clickjacking.XFrameOptionsMiddleware',
	    'users.middleware.my_middleware',  # 添加自定义中间件
	]

**2 多个中间件的执行顺序**

+ 在请求视图被处理前，中间件由上至下依次执行
+ 在请求视图被处理后，中间件右下至上依次执行

