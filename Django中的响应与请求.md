## Django中的响应与请求
### 响应 Request
1. HttpResponse

		HttpResponse(content= 响应体, content_type=响应体数据类型, status= 状态码)
	+ content: 表示但会的内容
	+ status_code: 返回 HTTP 响应状态码
	+ content_type: 指定返回的数据的 mime 类型
2. JsonResponse

	+ 帮助我们将数据转换为 json 字符串
	+ 设置响应头**Content-Type**为**application/json**
3. redirect重定向

		from django.shortcuts import redirect
		
		def demo_ciew(request):
			return redirect('/index.html')
			
### Cookie
#### Cookie 的特点

+ Cookie 以键值对格式进行信息存储
+ 基于域名安全,不同域名不可互相访问
+ 当浏览器请求某网站时，会将浏览器存储的跟网站相关的所有Cookie信息提交给网站服务器

1. 设置 cookie

	可以通过 HttpResponse 对象中的 set_cookie 方法来设置
	
		HttpResponse.set_cookie(cookie名, value=cookie值, max_age=cookie有效期)
2. 删除 cookie

	可以通过HttpResponse对象中的delete_cookie方法来删除cookie
	
		response.delete_cookie(''cookie名)
3. 读取 cookie

	可以通过HttpRequest对象的COOKIES属性来读取本次请求携带的cookie值。request.COOKIES为字典类型
	
		def demo_view(request):
			cookie1 = request.COOKIES.get('cookie名')
			return HttpResponse('OK')
			
### Session
1. 启用 session

	django 项目默认启用 session, 如需禁用 session, 将 setting 中的 session 中间件注释掉即可
2. 存储方式
	
	2.1 数据库
	
	默认存储方式
	
		SESSION_ENGINE='django.contrib.sessions.backends.db'
	
	2.2 本地缓存
	
	存储在本机内存中，如果丢失则不能找回，比数据库的方式读写更快
	
		SESSION_ENGINE='django.contrib.sessions.backends.cache'
	
	2.3 混合存储
	
	优先从本机内存中存取，如果没有则从数据库中存取
	
		SESSION_ENGINE='django.contrib.sessions.backends.cached_db'
	
	2.4 redis
	
	需要在 settings.py 中进行设置:
	
		CACHES = {
		    "default": {
		        "BACKEND": "django_redis.cache.RedisCache",
		        "LOCATION": "redis://127.0.0.1:6379/1",
		        "OPTIONS": {
		            "CLIENT_CLASS": "django_redis.client.DefaultClient",
		        }
		    }
		}
		SESSION_ENGINE = "django.contrib.sessions.backends.cache"
		SESSION_CACHE_ALIAS = "default"
	
3. session 操作

	通过 HttpRequest 对象的 session 属性进行绘画的读写操作
	1) 意见支队的格式写 session
	
		request.session['键']=值
		
	2) 根据键读取值
	
		request.session.get('键', 默认值)
	
	3) 清除所有 session , 在存储中删除值部分
	
		request.session.clear()
		
	4)清除 session 数据, 在存储中删除整条数据
	
		request.session.flush()
		
	5) 删除指定键及值,在存储中只删除某个键及对应的值
	
		del request.session['键']

	6) 设置 session 有效期
	
		request.session.set_expiry(value)
