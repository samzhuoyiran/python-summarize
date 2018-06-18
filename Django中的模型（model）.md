## Django中的模型（model）

首先需要对需要的数据库进行配置，教程很多，这里就不说了

### 定义模型类

+ 模型类被定义在应用下的models.py文件中
+ 模型类必须继承自Model类，位于django.db.models中

#### 1 定义

```
from django.db import models

#定义图书模型类BookInfo
class BookInfo(models.Model):
    btitle = models.CharField(max_length=20, verbose_name='名称')
    bpub_date = models.DateField(verbose_name='发布日期')
    bread = models.IntegerField(default=0, verbose_name='阅读量')
    bcomment = models.IntegerField(default=0, verbose_name='评论量')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_books'  # 指明数据库表名
        verbose_name = '图书'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

    def __str__(self):
        """定义每个数据对象的显示信息"""
        return self.btitle

```

1）数据库表名

模型类如果未指明表名，django默认以`小写app名_小写模型类名`为数据库表名

可以通过**db_table**指明数据库表名

2）关于主键

django会为表创建自动增长的主键列

默认创建的主键列属性为id，可以使用pk（primary key）代替

3）属性命名限制

+ 不能是python的保留关键字

+ 不允许使用连续的下划线，这是由django的查询方式决定的

+ 定义属性时需要指定字段类型，通过字段类型的参数指定选项

+ ```
  属性=models.字段类型(选项)
  ```

4）字段类型

| 类型             | 说明                                                         |
| :--------------- | ------------------------------------------------------------ |
| AutoField        | 自动增长的IntegerField，通常不用指定，不指定时Django会自动创建属性名为id的自动增长属性 |
| Booleanfield     | 布尔字段，值为True或False                                    |
| NullBooleanField | 支持Null、True、False三种值                                  |
| CharField        | 字符串，参数max_length表示最大字符个数                       |
| TextField        | 大文本字段，一般超过4000个字符时使用                         |
| IntegerField     | 整数                                                         |
| Decimalfield     | 十进制浮点数 ， 参数max_digits表示总位数， 参数decimal_places表示小数位数 |
| FloatField       | 浮点数                                                       |
| DateField        | 日期， 参数auto_now表示每次保存对象时，自动设置该字段为当前时间，用于"最后一次修改"的时间戳，它总是使用当前日期，默认为False； 参数auto_now_add表示当对象第一次被创建时自动设置当前时间，用于创建的时间戳，它总是使用当前日期，默认为False; 参数auto_now_add和auto_now是相互排斥的，组合将会发生错误 |
| TimeField        | 时间，参数同date                                             |
| DateTimeField    | 日期时间，参数同date                                         |
| FileField        | 上传文件字段                                                 |
| imageField       | 继承于FileField，对上传的 内容进⾏行行校验，确保是有效的图⽚片(必须要安装Pillow才可以使用（pip install Pillow） |

5）选项

| 选项        | 说明                                                         |
| ----------- | ------------------------------------------------------------ |
| null        | 如果为True，表示允许为空，默认值是False                      |
| blank       | 如果为True，则该字段允许为空白，默认值是False                |
| db_column   | 字段的名称，如果未指定，则使用属性的名称                     |
| db_index    | 若值为True, 则在表中会为此字段创建索引，默认值是False        |
| default     | 默认                                                         |
| primary_key | 若为True，则该字段会成为模型的主键字段，默认值是False，一般作为AutoField的选项使用 |
| unique      | 如果为True, 这个字段在表中必须有唯一值，默认值是False        |

6）外键

在设置外键时，需要通过**in_delete**选项指明主表删除数据时，对于外键引用好数据如何处理，在django.db.models中包含了可选常量：

+ **CASCADE** 级联，删除主表数据时连通一起删除外键表中数据
+ **PROTECT** 保护，通过抛出**ProtectedError**异常，来阻止删除主表中被外键应用的数据
+ **SET_NULL** 设置为NULL，仅在该字段null=True允许为null时可用
+ **SET_DEFAULT** 设置为默认值，仅在该字段设置了默认值时可用
+ **SET()** 设置为特定值或者调用特定方法

7）元选项

在模型类中定义元选项`class Mate`

+ db_table = '表名'
+ verbose_name = '指定admin后台显示的名字'

#### 2 迁移

将模型类同步到数据库中

1）生成迁移文件

```python
python manage.py makemigrations
```

2）同步到数据库

```
python manage.py migrate
```

### 模型类的属性

+ object管理器，是Manager类型的对象

### 模型类对象方法

+ save()将模型类对象保存到数据库中
+ delete()将模型类对象从数据表中删除

### 查询集

#### 特性

+ 惰性执行：创建查询集不会访问数据库，直到调用数据时，才会访问数据库，调用数据的情况包括迭代、序列化、与if合用
+ 缓存：查询集的结果被存下来之后，再次查询时会使用之前缓存的数据

#### 过滤器

+ 返回列表的过滤器

```
all():返回所有数据
filter()：返回满足条件的数据
exclude()：返回满足条件之外的数据，相当于sql语句中的where部分的not关键字
order_by():排序
```

+ 返回单个值得过滤器

```
count()：返回当前查询的总条数
get()：返回单个满足条件的对象，如果未找到会引发"模型类.DoesNotExist"的异常，如果多条被返回，会引发"模型类.MultipleObjectsReturned"异常
aggregate()：聚合
```

+ 查询过滤条件（属性名称_比较运算符=值）

```
exact:判断是否相等
contains:是否包含
startswith，endswith：以什么开始，以什么结尾
isnull：是否为空
in：包含在什么范围内
year:年，month：月，day：日，week：星期，hour：时，minute：分，second：秒
gt：大于，gte：大于等于，lt：小于，lte：小于等于
F对象：F('字段')
Q对象：Q(属性名__运算符=值)
聚合函数：{
    求和：Sum('字段')
    最大值：Max(字段)
    最小值：Min(字段)
    平均数：Avg(字段)
}
条件关联：{
    一对多：关联模型类类名小写__属性名__运算符=值
    多对一：关联属性__属性名__运算符=值
}
```

+ 关联查询
  + 一对多：被关联对象.关联模型类名_set.过滤器
  + 多对一：关联对象.关联对象

