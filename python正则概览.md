### 一、python正则概览

1. 正则基本使用

		import re
		re.match(r"正则", 数据) 
			从头开始匹配
			返回值 成功匹配返回结果对象  从结果对象中获取匹配 .group()
				  匹配失败 返回None
		
		re.search(r"正则", 数据)
			从数据中进行搜索 并且尝试匹配 
			返回值 成功匹配返回结果对象  从结果对象中获取匹配 .group()
		          匹配失败 返回None
2. 匹配单个字符 - 元字符

		. 匹配1个任意字符 除 \n
			re.match(r"hello.","hello1").group()
			re.match(r"hello.","hello9").group()
			re.match(r"hello.","helloa").group()
			re.match(r"hello.","hello\n").group()
	
		[] 匹配集合中任意一个字符 -白名单
			re.match(r"hello[a]","helloa").group()
			re.match(r"hello[a]","hellob").group()
			re.match(r"hello[ab]","hellob").group()
			re.match(r"hello[ab]","helloc").group()
			re.match(r"hello[0123456789]","helloc").group()
		[^] 禁止匹配集合中的任意一个字符 -黑名单
			re.match(r"hello[^0123456789]","hello9").group()
			re.match(r"hello[^0123456789]","helloa").group()
	
		[-] 匹配范围 ASCII码表 
			re.match(r"hello[^0-9]","helloY").group()
			re.match(r"hello[^0-9]","hello0").group()
			re.match(r"hello[0123456789]","helloc").group()
				re.match(r"hello[0-9]","helloc").group()
		\d 匹配一个数字字符 \D匹配一个非数字字符
		\s space空白字符 匹配一个空白字符[\r\n\v\t\f ]  \S匹配一个非空白字符
		\w word单词     匹配一个单词字符[\da-zA-Z_]   \W匹配一个非单词字符[^\da-zA-Z_]
		拓展
			py2 ASCII[\da-zA-Z_]
			py3 UNICODE[\da-zA-Z_] 加上中文
				e.match(r"嫦娥\w号","嫦娥一号")
				re.match(r"嫦娥\w号","嫦娥一号",re.A).group()
		
		re.match(r"嫦娥[\da-zA-Z_]号","嫦娥A号").group()
		re.match(r"嫦娥\w号","嫦娥A号").group()

3. 匹配多个字符 - 次数

		{n} 匹配n次
			\d{100} 匹配\d100次
		
			re.match(r"嫦娥\d号","嫦娥10号").group()
			re.match(r"嫦娥\d\d号","嫦娥10号").group()
			re.match(r"嫦娥\d\d\d号","嫦娥100号").group()
			re.match(r"嫦娥\d\d\d\d\d\d号","嫦娥100000号").group()
			re.match(r"嫦娥\d{6}号","嫦娥100000号").group()
		
		{n,m} 匹配 n到m次
		
			re.match(r"嫦娥\d{3,6}号","嫦娥100000号").group()
		
		{n,}  匹配 至少n次 
			re.match(r"嫦娥\d{1,}号","嫦娥100000号").group()
			re.match(r"嫦娥\d{1,}号","嫦娥100000000000000000000号").group()
		
		+   匹配至少1次 {1,}
			re.match(r"嫦娥\d+号","嫦娥100000000000000000000号").group()
			re.match(r"嫦娥\d+号","嫦娥1号").group()
			re.match(r"嫦娥\d+号","嫦娥号").group()
			
		*   匹配至少0次 {0,}
			re.match(r"嫦娥\d{0,}号","嫦娥号").group()
			re.match(r"嫦娥\d*号","嫦娥号").group()
		
		?   匹配0次或者1次 {0,1}
			re.match(r"嫦娥\d{0,1}号","嫦娥号").group()
			re.match(r"嫦娥\d{0,1}号","嫦娥1号").group()
			re.match(r"嫦娥\d?号","嫦娥1号").group()
			re.match(r"嫦娥\d?号","嫦娥号").group()
		
		021-8888888
		0755-1234678
		\d{3,4}-\d{6,8}

4. ^ 匹配开始位置 	$  匹配结束位置

		re.match(r"\w{4,20}@163.com","123456@163.com").group()
		re.match(r"\w{4,20}@163.com","123456@163.com.hahahha").group()
		re.match(r"\w{4,20}@163.com$","123456@163.com.hahahha").group()

		re.search(r"\w{4,20}@163.com$","123456@163.com").group()
		re.search(r"\w{4,20}@163.com$","cc.123456@163.com").group()
		re.search(r"^\w{4,20}@163.com$","cc.123456@163.com").group()

		re.match(r"^\w{4,20}@163.com$","123456@163.com").group()

5. 分组

		目的 提取出整体数据中 符合某种规律的数据
		创建分组 
			(正则)
		
		取出分组数据
			.group() === .group(0) 表示第0个分组 表示整体匹配结果
			.group(分组编号)  
			
			re.match(r"嫦娥(\d?)号","嫦娥1号").group(1)
			re.match(r"^\w{4,20}@(\w+).com$","123456@qq.com").group(1)
			re.match(r"^\w{4,20}@qq\.com$","123456@qq.com").group()
		
		分组引用
			目的 - 将前面分组的匹配结果 用在后续的某个位置的匹配
			使用方式  \分组的编号
		
			re.match(r"(\d{3,4})-(\d{6,8})","021-1234567").group(1)
			re.match(r"(\d{3,4})-(\d{6,8})","021-1234567").group(2)
			re.match(r"^(\d{3,4})-(\d{6,8}) \1-\2$","021-1234567 021-1234567").group(2)
			re.match(r"^(\d{3,4})-(\d{6,8}) \1-\2$","021-1234567 021-1234567").group(1)
			re.match(r"^(\d{3,4})-(\d{6,8}) \1-\2$","021-1234567 021-1234568").group()
		
		| 匹配左边或者右边的表达式
			re.match(r"\w{4,20}@qq\.com|\w{4,20}@163.com","123456@163.com").group()
		
		(|)  匹配左边或者右边的表达式放到 分组中
			re.match(r"^\w{4,20}@(qq|163)\.com$","123456@163.com").group()
			re.match(r"^\w{4,20}@(qq|163)\.com$","123456@qq.com").group()
			re.match(r"^\w{4,20}@(qq|163)\.com$","123456@qq.com").group(1)
		
		re.match(r"^(?P<quhao>\d{3,4})-(?P<zuoji>\d{6,8}) (?P=quhao)-(?P=zuoji)$","021-1234567 021-1234567")
6. 高级方法
	
		findall(正则, 数据) 查找数据中符合正则规律的所有的数据
			结果是列表 
		sub(正则, "替换的数据", 数据，count=-1)  返回值替换之后的数据
			参数2可以是函数名 
			def func(参数是匹配对象):
				return  "替换的数据"
		split(正则,数据)  返回值为 列表

7. 贪婪模式 默认情况下

		懒惰模式 量词后面加?
	
		贪婪和非贪婪必须有一个前提就是满足整体匹配结果

8. r字符

		一般在正则内容前都加上一个r就可以,也无伤大雅
		自动对正则中的\ ---转义-> \\
		正则中需要使用\\ 匹配数据的\
		
		
