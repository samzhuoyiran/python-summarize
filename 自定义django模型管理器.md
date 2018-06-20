### 自定义django模型管理器

管理器是django的模型进行数据库操作的接口，django应用的每个模型类都拥有至少一个管理器

当没有为模型类定义管理器时，django回味每一个模型类生成一个objects的管理器，来自**models.Manager**类的对象

**注意：一旦为模型类指明自定义管理器后，django不再生成默认管理对象objects**

自定义管理器类主要用于有两种情况：

1. 修改原始查询集，重写all()方法

```
# 定义一个管理器类重写all()方法
class MyManager(models.Manager):
	def all(self):
		# 返回未删除的数据
		return super().filter(is_delete=False)
# 在模型类中指定管理器
class MyInfo(models.Model):
	...
	mymanager = MyManager()
	
# 使用
MyInfo.mymanager.all()
```

1. 在管理器类中补充定义新的方法

```
# 定义一个create方法
class MyManager(models.Manager):
	def create_new(self, *args, **kwargs):
		info = self.model()  # 获得模型类
		# 保存传入的属性
		...
		# 保存到数据表
		info.save()
		return info
		
class MyInfo(models.Model):
	...
	mymanager = MyManager()
	
# 调用
info = MyInfo.mymanager.create_new(*args,**kwargs)
```

