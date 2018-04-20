# 浅谈python的装饰器
-
       最近在一直在搞python中的装饰器,今天就这个来做些装饰器的总结.


# 装饰器的本质
-
*  首先在Python中的函数是可以看做一个特殊变量的.而装饰器是建立在闭包的前提上的.
*  闭包就是将函数当做参数传入另一个函数,两个函数的嵌套,外部函数返回北部函数的引用.
*	装饰器本质上是一个Python函数，它可以让其他函数在不需要做任何代码变动的前提下增加额外功能，装饰器的返回值也是一个函数对象。它经常用于有切面需求的场景，比如：插入日志、性能测试、事务处理、缓存、权限校验等场景。装饰器是解决这类问题的绝佳设计，有了装饰器，我们就可以抽离出大量与函数功能本身无关的雷同代码并继续重用.

		总而言之 装饰器就是在不改变原先函数代码的情况下,给原先的函数添加功能.
		
# 装饰器的写法
-
	1. 创建一个闭包
	2. @xx装饰你要装饰的函数
	# 这里就直接写万能装饰器了
	def set_fun(func):
		def call_fun(*args,**kwargs):
			return func(*args,**kwargs)
		return call_fun
		
	@set_fun
	def test():
		pass
### 一个装饰器装饰函数
	如上,使用语法糖@装饰函数的引用,这里可能是很多人对装饰器不理解的原因吧;
	我们可以这样来看 @set_fun ==> test = set_fun(test) = call_fun,这个时候test就已经指向了闭包中
	的call_fun;
	这样当我们创建函数对象时执行的顺序就执行我们装饰过的函数了.

	
### 两个装饰器装饰一个函数
	
	def set_fun1(func):
		def call_fun1(*args,**kwargs):
			return func(*args,**kwargs)
		return call_fun1
		
	def set_fun2(func):
		def call_fun2(*args,**kwargs):
			return func(*args,**kwargs)
		return call_fun2
		
	@set_fun1
	@set_fun2
	def test():
		pass
	
	test()
+ 代码的执行顺序是从上往下的,首先遇见`@set_fun1`,但是它的下面并不是一个函数,无法进行装饰;
+ 接着`@set_fun2`,会对`test函数`进行装饰,返回的是`test = set_fun2(test) = call_fun2`;
+ 恩,第一个装饰就结束了,这时`@set_fun1`发现下面是一个函数了,心有不甘,它也要"化妆";
+ 这时下面函数已经是`call_fun2`的引用了,同理`test = set_fun1(call_fun2) = call_fun1`;
+ 这时,两个装饰器都是已经装饰完成的了,`test()`进行调用时的顺序是调用`@set_fun1`中的`call_fun1`,运行其中的`func()`,在`func()`中调用`call_fun2`,运行其中的`func()`指向原先的`test()`.

多个装饰器装饰一个函数的道理和上面说的相同
### 装饰器传参
	def set_args(args):
		print(args)		
		def set_fun(func):	
			def call_fun(*args,**kwargs):
				return func(*args,**kwargs)
			return call_fun
		
	@set_args(args)
	def test():
		pass
+ 装饰器传参就相当于三层函数嵌套,在闭包的外面包裹一层函数用来处理传入的参数.

### 类装饰器
	class Funcc(object):
		def __init__(self,func):
			self.func = func

		def __call__(self, *args, **kwargs):
			self.func()

	@Funcc    #test = Funcc(test)
	def test():
		pass

	test()
+ 类装饰器类似函数装饰器,创建类对象时使用一个`__init__`方法接收需要装饰的函数,并定义`__call__`方法运行需要添加的功能并执行原先的函数代码


# `装饰器的理念是就是对原函数、对象的加强，相当于重新封装`
+ 以上就是我对python中的解释器的浅显了解,欢迎修改补充.
		


