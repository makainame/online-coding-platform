def _cp(title, description, difficulty, tags, cases, starter_code):
    return {
        "title": title,
        "description": description,
        "difficulty": difficulty,
        "tags": tags,
        "test_cases": [
            {"input": inp, "expected_output": out}
            for inp, out in cases
        ],
        "starter_code": starter_code,
    }


CURRICULUM_PROBLEMS = [
    _cp(
        "打印欢迎语",
        "不读取输入，直接输出 欢迎学习 Python。",
        "easy",
        "Day01,print,入门",
        [("", "欢迎学习 Python")],
        """print("欢迎学习 Python")
""",
    ),
    _cp(
        "变量数据类型",
        "输入一个值，使用变量保存后输出原值，再输出它的数据类型名称。",
        "easy",
        "Day01,变量,type",
        [
            ("18", "18\nstr"),
            ("3.14", "3.14\nstr"),
            ("True", "True\nstr"),
        ],
        """value = input().strip()
print(value)
print(type(value).__name__)
""",
    ),
    _cp(
        "交换两个变量",
        "输入两个值，使用 Python 一行语法交换两个变量后输出。",
        "easy",
        "Day02,变量交换,元组",
        [
            ("3 5", "5 3"),
            ("-1 9", "9 -1"),
            ("x y", "y x"),
        ],
        """a, b = input().split()
a, b = b, a
print(a, b)
""",
    ),
    _cp(
        "f-string 输出成绩",
        "输入姓名和成绩，用空格分隔，使用 f-string 输出 姓名 的成绩是 成绩 分。",
        "easy",
        "Day02,f-string,格式化",
        [
            ("小明 92", "小明的成绩是92分"),
            ("小红 88", "小红的成绩是88分"),
            ("Tom 100", "Tom的成绩是100分"),
        ],
        """name, score = input().split()
print(f"{name}的成绩是{score}分")
""",
    ),
    _cp(
        "成绩等级判断",
        "输入一个整数成绩，85 分及以上输出 优秀，60 到 84 输出 及格，低于 60 输出 不及格。",
        "easy",
        "Day02,if,elif,else",
        [
            ("92", "优秀"),
            ("60", "及格"),
            ("45", "不及格"),
        ],
        """score = int(input())
if score >= 85:
    print("优秀")
elif score >= 60:
    print("及格")
else:
    print("不及格")
""",
    ),
    _cp(
        "判断闰年",
        "输入一个年份，判断是否为闰年：能被 400 整除，或能被 4 整除但不能被 100 整除。",
        "easy",
        "Day02,if,逻辑运算",
        [
            ("2024", "闰年"),
            ("1900", "平年"),
            ("2000", "闰年"),
        ],
        """year = int(input())
if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
    print("闰年")
else:
    print("平年")
""",
    ),
    _cp(
        "三元判断正负",
        "输入一个整数，使用三元运算符输出 正数、负数 或 零。",
        "easy",
        "Day03,三元运算符,if",
        [
            ("-3", "负数"),
            ("5", "正数"),
            ("0", "零"),
        ],
        """n = int(input())
print("正数" if n > 0 else ("零" if n == 0 else "负数"))
""",
    ),
    _cp(
        "while 打印 1 到 n",
        "输入一个正整数 n，使用 while 循环输出 1 到 n，数字之间用空格分隔。",
        "easy",
        "Day03,while,循环",
        [
            ("3", "1 2 3"),
            ("1", "1"),
            ("5", "1 2 3 4 5"),
        ],
        """n = int(input())
i = 1
while i <= n:
    print(i, end=" ")
    i += 1
""",
    ),
    _cp(
        "for 循环求和",
        "输入一个正整数 n，使用 for 循环计算 1 到 n 的和并输出。",
        "easy",
        "Day03,for,循环,求和",
        [
            ("10", "55"),
            ("100", "5050"),
            ("1", "1"),
        ],
        """n = int(input())
total = 0
for i in range(1, n + 1):
    total += i
print(total)
""",
    ),
    _cp(
        "continue 跳过偶数",
        "输入一个正整数 n，使用 for 循环输出 1 到 n 中的所有奇数，数字之间用空格分隔。",
        "easy",
        "Day03,continue,循环",
        [
            ("5", "1 3 5"),
            ("3", "1 3"),
            ("1", "1"),
        ],
        """n = int(input())
for i in range(1, n + 1):
    if i % 2 == 0:
        continue
    print(i, end=" ")
""",
    ),
    _cp(
        "字符串切片反转",
        "输入一个字符串，使用字符串切片反转后输出。",
        "easy",
        "Day04,字符串,切片",
        [
            ("hello", "olleh"),
            ("Python", "nohtyP"),
            ("abc", "cba"),
        ],
        """s = input().strip()
print(s[::-1])
""",
    ),
    _cp(
        "字符串常用方法",
        "输入一个字符串，输出它转大写后的结果，再输出其中字母 a 出现的次数。",
        "easy",
        "Day04,字符串,upper,count",
        [
            ("banana", "BANANA\n3"),
            ("Hello", "HELLO\n0"),
            ("python", "PYTHON\n0"),
        ],
        """s = input().strip()
print(s.upper())
print(s.count("a"))
""",
    ),
    _cp(
        "列表增删改",
        "输入一个整数列表，依次执行：末尾添加 4、删除第一次出现的 2、把第一个元素改成 9，最后输出列表。",
        "medium",
        "Day04,列表,增删改",
        [
            ("1 2 3", "9 3 4"),
            ("2 5", "9 5 4"),
            ("3 2 1", "9 3 1 4"),
        ],
        """nums = list(map(int, input().split()))
nums.append(4)
if 2 in nums:
    nums.remove(2)
nums[0] = 9
print(" ".join(map(str, nums)))
""",
    ),
    _cp(
        "元组打包解包",
        "输入两个值，把它们打包成元组，再解包给两个变量并输出。",
        "easy",
        "Day04,元组,打包,解包",
        [
            ("3 5", "3 5"),
            ("Tom Jerry", "Tom Jerry"),
            ("10 20", "10 20"),
        ],
        """a, b = input().split()
t = (a, b)
x, y = t
print(x, y)
""",
    ),
    _cp(
        "字典新增查询",
        "创建字典保存姓名，再添加年龄键，最后输出姓名和年龄。",
        "easy",
        "Day04,字典,新增,查询",
        [("", "张三 18")],
        """d = {"name": "张三"}
d["age"] = 18
print(d["name"], d["age"])
""",
    ),
    _cp(
        "字典遍历",
        "遍历字典 {'a': 1, 'b': 2}，使用 items 每行输出 键:值。",
        "easy",
        "Day04,字典,items,遍历",
        [("", "a:1\nb:2")],
        """d = {"a": 1, "b": 2}
for key, value in d.items():
    print(f"{key}:{value}")
""",
    ),
    _cp(
        "集合去重",
        "输入一行整数，使用集合去重后按升序输出。",
        "easy",
        "Day05,集合,去重",
        [
            ("1 2 2 3 1", "1 2 3"),
            ("5 5 5", "5"),
            ("3 1 2", "1 2 3"),
        ],
        """nums = list(map(int, input().split()))
print(" ".join(map(str, sorted(set(nums)))))
""",
    ),
    _cp(
        "列表推导式生成奇数",
        "输入一个正整数 n，使用列表推导式生成 1 到 n 中的所有奇数，输出时用空格分隔。",
        "medium",
        "Day05,列表推导式,高级语法",
        [
            ("5", "1 3 5"),
            ("10", "1 3 5 7 9"),
            ("1", "1"),
        ],
        """n = int(input())
nums = [i for i in range(1, n + 1) if i % 2 == 1]
print(" ".join(map(str, nums)))
""",
    ),
    _cp(
        "字典推导式生成平方",
        "输入一个正整数 n，使用字典推导式生成 1 到 n 的平方映射，每行输出 数字:平方。",
        "medium",
        "Day05,字典推导式,高级语法",
        [
            ("3", "1:1\n2:4\n3:9"),
            ("1", "1:1"),
        ],
        """n = int(input())
d = {i: i * i for i in range(1, n + 1)}
for key, value in d.items():
    print(f"{key}:{value}")
""",
    ),
    _cp(
        "自定义函数判断偶数",
        "定义函数 is_even(n)，输入一个整数，输出 偶数 或 奇数。",
        "easy",
        "Day05,函数,def,return",
        [
            ("4", "偶数"),
            ("7", "奇数"),
            ("0", "偶数"),
        ],
        """def is_even(n):
    return n % 2 == 0

n = int(input())
print("偶数" if is_even(n) else "奇数")
""",
    ),
    _cp(
        "lambda 乘法",
        "输入两个整数，使用 lambda 匿名函数计算乘积并输出。",
        "medium",
        "Day06,lambda,匿名函数",
        [
            ("3 4", "12"),
            ("5 6", "30"),
            ("-2 7", "-14"),
        ],
        """mul = lambda x, y: x * y
a, b = map(int, input().split())
print(mul(a, b))
""",
    ),
    _cp(
        "递归阶乘",
        "输入一个非负整数 n，使用递归计算 n! 并输出。",
        "medium",
        "Day06,递归,阶乘",
        [
            ("5", "120"),
            ("10", "3628800"),
            ("0", "1"),
        ],
        """def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

n = int(input())
print(factorial(n))
""",
    ),
    _cp(
        "异常处理除零",
        "输入两个整数，输出整除结果；除数为 0 时输出 error。",
        "easy",
        "Day07,异常,try,except",
        [
            ("8 2", "4"),
            ("5 0", "error"),
            ("9 3", "3"),
        ],
        """try:
    a, b = map(int, input().split())
    print(a // b)
except ZeroDivisionError:
    print("error")
""",
    ),
    _cp(
        "定义类和对象",
        "输入姓名和年龄，定义 Student 类并创建对象，输出对象的姓名和年龄。",
        "easy",
        "进阶Day01,类,对象,__init__",
        [
            ("Tom 18", "Tom 18"),
            ("Lily 20", "Lily 20"),
        ],
        """class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

name, age = input().split()
s = Student(name, age)
print(s.name, s.age)
""",
    ),
    _cp(
        "学生 __str__",
        "定义 Student 类并实现 __str__，输入姓名和年龄，输出 学生：姓名，年龄岁。",
        "medium",
        "进阶Day01,魔术方法,__str__",
        [
            ("Tom 18", "学生：Tom，18岁"),
            ("Lily 20", "学生：Lily，20岁"),
        ],
        """class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"学生：{self.name}，{self.age}岁"

name, age = input().split()
print(Student(name, age))
""",
    ),
    _cp(
        "继承和方法重写",
        "定义 Animal 父类和 Dog 子类，子类重写 speak 方法，输出 汪汪。",
        "medium",
        "进阶Day02,继承,方法重写",
        [("", "汪汪")],
        """class Animal:
    def speak(self):
        return "动物叫"

class Dog(Animal):
    def speak(self):
        return "汪汪"

print(Dog().speak())
""",
    ),
    _cp(
        "类变量和类方法",
        "定义 Book 类，使用类变量记录创建数量，创建两本书后通过类方法输出总数。",
        "medium",
        "进阶Day03,类变量,classmethod",
        [("", "2")],
        """class Book:
    count = 0

    def __init__(self, title):
        self.title = title
        Book.count += 1

    @classmethod
    def total(cls):
        return cls.count

b1 = Book("Python")
b2 = Book("AI")
print(Book.total())
""",
    ),
    _cp(
        "闭包",
        "输入一个名字，使用闭包返回内部函数，内部函数输出 你好，名字。",
        "medium",
        "进阶Day04,闭包,嵌套函数",
        [
            ("张三", "你好，张三"),
            ("李四", "你好，李四"),
        ],
        """def outer(name):
    def inner():
        return f"你好，{name}"
    return inner

name = input().strip()
print(outer(name)())
""",
    ),
    _cp(
        "装饰器",
        "定义装饰器 check，让函数输出 欢迎，名字。输入一个名字并输出结果。",
        "medium",
        "进阶Day04,装饰器,高级语法",
        [
            ("Tom", "欢迎，Tom"),
            ("小红", "欢迎，小红"),
        ],
        """def check(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@check
def say(name):
    return f"欢迎，{name}"

name = input().strip()
print(say(name))
""",
    ),
    _cp(
        "生成器生成平方",
        "输入一个正整数 n，使用生成器生成 1 到 n 的平方，输出时用空格分隔。",
        "medium",
        "进阶Day07,生成器,yield",
        [
            ("3", "1 4 9"),
            ("5", "1 4 9 16 25"),
        ],
        """def squares(n):
    for i in range(1, n + 1):
        yield i * i

n = int(input())
print(" ".join(map(str, squares(n))))
""",
    ),
    _cp(
        "property 学生姓名",
        "输入一个姓名，使用 @property 把私有姓名属性封装成只读属性并输出。",
        "medium",
        "进阶Day07,property,封装",
        [
            ("Tom", "Tom"),
            ("小红", "小红"),
        ],
        """class Student:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

name = input().strip()
print(Student(name).name)
""",
    ),
    _cp(
        "正则校验手机号",
        "输入一个手机号，使用正则判断是否为 1 开头、第二位 3-9、后面 9 位数字，输出 有效 或 无效。",
        "medium",
        "进阶Day07,正则,re",
        [
            ("13812345678", "有效"),
            ("12812345678", "无效"),
            ("12345678901", "无效"),
        ],
        """import re

phone = input().strip()
if re.match(r"^1[3-9]\\d{9}$", phone):
    print("有效")
else:
    print("无效")
""",
    ),
]


CURRICULUM_STARTER_CODES = {
    item["title"]: item["starter_code"]
    for item in CURRICULUM_PROBLEMS
}
