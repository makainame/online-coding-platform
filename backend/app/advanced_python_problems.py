def _p(title, description, difficulty, tags, cases):
    return {
        "title": title,
        "description": description,
        "difficulty": difficulty,
        "tags": tags,
        "test_cases": [
            {"input": inp, "expected_output": out}
            for inp, out in cases
        ],
    }


ADVANCED_PYTHON_PROBLEMS = [
    _p(
        "字符串首字母大写",
        "输入一个字符串，使用 capitalize 让首字母大写，其余字母小写后输出。",
        "easy",
        "字符串,capitalize",
        [
            ("hello world", "Hello world"),
            ("python", "Python"),
            ("a b", "A b"),
        ],
    ),
    _p(
        "字符串去除首尾空格",
        "输入一个字符串，使用 strip 去除首尾空格后输出。",
        "easy",
        "字符串,strip",
        [
            ("  hello  ", "hello"),
            ("  a b  ", "a b"),
            ("python", "python"),
        ],
    ),
    _p(
        "前缀判断",
        "第一行输入字符串，第二行输入前缀，使用 startswith 判断是否以该前缀开头，输出 yes 或 no。",
        "easy",
        "字符串,startswith",
        [
            ("hello\nhe", "yes"),
            ("hello\nlo", "no"),
            ("python\npy", "yes"),
        ],
    ),
    _p(
        "后缀判断",
        "第一行输入字符串，第二行输入后缀，使用 endswith 判断是否以该后缀结尾，输出 yes 或 no。",
        "easy",
        "字符串,endswith",
        [
            ("hello\nlo", "yes"),
            ("hello\nhe", "no"),
            ("python\non", "yes"),
        ],
    ),
    _p(
        "查找子串位置",
        "第一行输入字符串，第二行输入子串，使用 find 输出子串第一次出现的位置；不存在输出 -1。",
        "easy",
        "字符串,find",
        [
            ("hello world\nworld", "6"),
            ("abcabc\nbc", "1"),
            ("hello\nz", "-1"),
        ],
    ),
    _p(
        "字符串分割数量",
        "输入一行由空格分隔的字符串，使用 split 输出单词数量。",
        "easy",
        "字符串,split",
        [
            ("a b c", "3"),
            ("hello", "1"),
            ("python is fun", "3"),
        ],
    ),
    _p(
        "字符串连接",
        "输入一行英文单词，用 join 以 - 连接后输出。",
        "easy",
        "字符串,join",
        [
            ("a b c", "a-b-c"),
            ("python is fun", "python-is-fun"),
            ("x y", "x-y"),
        ],
    ),
    _p(
        "数字补零",
        "输入一个整数，使用 zfill 输出 3 位数字，不足补 0。",
        "easy",
        "字符串,zfill",
        [
            ("5", "005"),
            ("123", "123"),
            ("42", "042"),
        ],
    ),
    _p(
        "列表插入",
        "第一行输入列表，第二行输入下标，第三行输入值，使用 insert 插入后输出。",
        "easy",
        "列表,insert",
        [
            ("1 3 4\n1\n2", "1 2 3 4"),
            ("1 2\n0\n9", "9 1 2"),
            ("1 2\n2\n8", "1 2 8"),
        ],
    ),
    _p(
        "列表删除指定值",
        "第一行输入列表，第二行输入要删除的值，使用 remove 删除第一次出现后输出。",
        "easy",
        "列表,remove",
        [
            ("1 2 3 2\n2", "1 3 2"),
            ("a b c\nb", "a c"),
            ("1 1 1\n1", "1 1"),
        ],
    ),
    _p(
        "列表弹出",
        "第一行输入列表，第二行输入下标，使用 pop 删除该位置元素后输出剩余列表。",
        "easy",
        "列表,pop",
        [
            ("1 2 3\n1", "1 3"),
            ("1 2 3\n0", "2 3"),
            ("1 2\n1", "1"),
        ],
    ),
    _p(
        "列表扩展",
        "两行输入两个列表，使用 extend 把第二个列表追加到第一个列表后输出。",
        "easy",
        "列表,extend",
        [
            ("1 2\n3 4", "1 2 3 4"),
            ("a\nb c", "a b c"),
            ("1\n2", "1 2"),
        ],
    ),
    _p(
        "列表查找下标",
        "第一行输入列表，第二行输入目标值，使用 index 输出第一次出现下标；不存在输出 -1。",
        "easy",
        "列表,index",
        [
            ("a b c\nb", "1"),
            ("1 2 3\n9", "-1"),
            ("x y x\nx", "0"),
        ],
    ),
    _p(
        "列表复制反转",
        "输入一个列表，使用 copy 复制后反转副本并输出。",
        "easy",
        "列表,copy,reverse",
        [
            ("1 2 3", "3 2 1"),
            ("a b", "b a"),
            ("1", "1"),
        ],
    ),
    _p(
        "列表清空长度",
        "输入一个列表，使用 clear 清空后输出列表长度。",
        "easy",
        "列表,clear",
        [
            ("1 2 3", "0"),
            ("a b c d", "0"),
            ("x", "0"),
        ],
    ),
    _p(
        "字典 get 默认值",
        "程序内置字典 {'apple': 3, 'banana': 5}，输入一个键，用 get 输出对应值；不存在输出 not found。",
        "medium",
        "字典,get",
        [
            ("apple", "3"),
            ("banana", "5"),
            ("cherry", "not found"),
        ],
    ),
    _p(
        "字典成员判断",
        "程序内置字典 {'apple': 3, 'banana': 5}，输入一个键，使用 in 判断键是否存在，输出 yes 或 no。",
        "medium",
        "字典,in",
        [
            ("apple", "yes"),
            ("grape", "no"),
            ("banana", "yes"),
        ],
    ),
    _p(
        "集合差集",
        "两行输入两组整数，输出第一组减去第二组的差集，按升序排列。",
        "medium",
        "集合,差集",
        [
            ("1 2 3\n2 3 4", "1"),
            ("1 2\n1 2", ""),
            ("1 2 3\n4", "1 2 3"),
        ],
    ),
    _p(
        "集合对称差",
        "两行输入两组整数，输出两组中不同时存在的元素，按升序排列。",
        "medium",
        "集合,对称差",
        [
            ("1 2 3\n2 3 4", "1 4"),
            ("1 2\n3 4", "1 2 3 4"),
            ("1\n1", ""),
        ],
    ),
    _p(
        "集合添加",
        "第一行输入集合，第二行输入要添加的值，使用 add 添加后按升序输出。",
        "easy",
        "集合,add",
        [
            ("1 2\n3", "1 2 3"),
            ("1\n2", "1 2"),
            ("1 2\n1", "1 2"),
        ],
    ),
    _p(
        "集合安全删除",
        "第一行输入集合，第二行输入要删除的值，使用 discard 删除后按升序输出；不存在不报错。",
        "medium",
        "集合,discard",
        [
            ("1 2 3\n2", "1 3"),
            ("1 2\n9", "1 2"),
            ("1 2 3\n1", "2 3"),
        ],
    ),
    _p(
        "子集判断",
        "两行输入两组整数，判断第一组是否为第二组的子集，输出 yes 或 no。",
        "medium",
        "集合,issubset",
        [
            ("1 2\n1 2 3", "yes"),
            ("1 2 3\n1 2", "no"),
            ("1\n1", "yes"),
        ],
    ),
    _p(
        "for-else 查找",
        "输入一行整数，如果存在偶数，使用 for 和 break 输出 found；否则通过 else 输出 not found。",
        "medium",
        "for,else,break",
        [
            ("1 3 5 6", "found"),
            ("1 3 5", "not found"),
            ("2", "found"),
        ],
    ),
    _p(
        "while-else 结束判断",
        "输入一个非负整数 n，使用 while 把 n 递减到 0 后通过 else 输出 done；负数输出 invalid。",
        "medium",
        "while,else",
        [
            ("3", "done"),
            ("-1", "invalid"),
            ("0", "done"),
        ],
    ),
    _p(
        "match-case 数字转英文",
        "输入整数 1、2 或其他数字，使用 match-case 输出 one、two 或 other。",
        "medium",
        "match,case,条件分支",
        [
            ("1", "one"),
            ("2", "two"),
            ("9", "other"),
        ],
    ),
    _p(
        "关键字参数幂运算",
        "输入底数和指数，使用关键字参数调用 pow(base=底数, exp=指数) 并输出结果。",
        "medium",
        "函数,关键字参数",
        [
            ("5 3", "125"),
            ("2 10", "1024"),
            ("3 2", "9"),
        ],
    ),
    _p(
        "**kwargs 拼接",
        "输入成对的键和值，用函数接收 **kwargs，输出 键=值 并用逗号连接。",
        "medium",
        "函数,**kwargs,高级语法",
        [
            ("a 1 b 2", "a=1,b=2"),
            ("x 9", "x=9"),
            ("a 1 b 2 c 3", "a=1,b=2,c=3"),
        ],
    ),
    _p(
        "返回多个值",
        "输入两个整数，编写函数返回它们的和与乘积，输出时用空格分隔。",
        "easy",
        "函数,多返回值,元组",
        [
            ("3 4", "7 12"),
            ("5 6", "11 30"),
            ("-1 2", "1 -2"),
        ],
    ),
    _p(
        "lambda 多参数",
        "输入两个整数，使用 lambda 定义乘法函数并输出乘积。",
        "medium",
        "lambda,高级语法",
        [
            ("3 4", "12"),
            ("5 6", "30"),
            ("-2 7", "-14"),
        ],
    ),
    _p(
        "字典推导式",
        "输入一行英文单词，用字典推导式生成 单词:长度 映射，每行输出 单词:长度。",
        "medium",
        "字典推导式,高级语法",
        [
            ("a bb ccc", "a:1\nbb:2\nccc:3"),
            ("python java", "python:6\njava:4"),
            ("x", "x:1"),
        ],
    ),
    _p(
        "集合推导式",
        "输入一行整数，用集合推导式生成每个数的平方，按升序输出。",
        "medium",
        "集合推导式,高级语法",
        [
            ("1 2 2 3", "1 4 9"),
            ("2 3", "4 9"),
            ("0", "0"),
        ],
    ),
    _p(
        "条件列表推导式",
        "输入一行整数，用带条件的列表推导式生成偶数的平方，按原顺序输出。",
        "medium",
        "列表推导式,条件,高级语法",
        [
            ("1 2 3 4", "4 16"),
            ("1 3 5", ""),
            ("2 4", "4 16"),
        ],
    ),
    _p(
        "递归反转字符串",
        "输入一个字符串，使用递归反转后输出。",
        "medium",
        "递归,字符串",
        [
            ("abc", "cba"),
            ("hello", "olleh"),
            ("a", "a"),
        ],
    ),
    _p(
        "递归幂运算",
        "输入底数和指数，使用递归实现幂运算并输出。",
        "medium",
        "递归,幂运算",
        [
            ("2 10", "1024"),
            ("3 3", "27"),
            ("5 0", "1"),
        ],
    ),
    _p(
        "iter next 取首元素",
        "输入一行元素，使用 iter 和 next 输出第一个元素。",
        "medium",
        "迭代器,iter,next",
        [
            ("a b c", "a"),
            ("1 2 3", "1"),
            ("x", "x"),
        ],
    ),
    _p(
        "yield from 合并",
        "两行输入两个列表，使用生成器和 yield from 依次产出两个列表的全部元素，输出时用空格分隔。",
        "hard",
        "生成器,yield,from",
        [
            ("1 2\n3 4", "1 2 3 4"),
            ("a\nb c", "a b c"),
            ("1\n2 3", "1 2 3"),
        ],
    ),
    _p(
        "classmethod 工厂方法",
        "输入姓名和年龄，使用 classmethod 工厂方法创建 Person 对象并输出 姓名 is 年龄 years old。",
        "medium",
        "类,classmethod,面向对象",
        [
            ("Tom 18", "Tom is 18 years old"),
            ("Lily 20", "Lily is 20 years old"),
            ("Bob 7", "Bob is 7 years old"),
        ],
    ),
    _p(
        "staticmethod 工具方法",
        "输入两个整数，使用 staticmethod 定义 add 方法并输出结果。",
        "medium",
        "类,staticmethod,面向对象",
        [
            ("3 4", "7"),
            ("10 20", "30"),
            ("-1 1", "0"),
        ],
    ),
    _p(
        "property 面积",
        "输入圆的半径，定义 Circle 类并使用 property 返回面积，圆周率取 3.14。",
        "medium",
        "类,property,面向对象",
        [
            ("5", "78.5"),
            ("10", "314.0"),
            ("1", "3.14"),
        ],
    ),
    _p(
        "__str__ 魔术方法",
        "输入两个整数，定义 Point 类并实现 __str__，输出格式为 Point(x,y)。",
        "medium",
        "类,魔术方法,__str__",
        [
            ("1 2", "Point(1,2)"),
            ("3 4", "Point(3,4)"),
            ("-1 5", "Point(-1,5)"),
        ],
    ),
    _p(
        "__eq__ 魔术方法",
        "两行各输入一个点的坐标，定义 Point 类并实现 __eq__，输出两个点是否相等。",
        "medium",
        "类,魔术方法,__eq__",
        [
            ("1 2\n1 2", "True"),
            ("1 2\n3 4", "False"),
            ("0 0\n0 0", "True"),
        ],
    ),
    _p(
        "try except else",
        "输入两个整数，输出整除结果；除数为 0 时输出 error。如果成功，额外输出 success。",
        "medium",
        "异常,try,except,else",
        [
            ("8 2", "4\nsuccess"),
            ("5 0", "error"),
            ("9 3", "3\nsuccess"),
        ],
    ),
    _p(
        "finally 清理",
        "输入一个整数，输出该数；如果转换失败输出 error。无论是否出错，最后都输出 finally。",
        "medium",
        "异常,finally",
        [
            ("5", "5\nfinally"),
            ("abc", "error\nfinally"),
            ("-3", "-3\nfinally"),
        ],
    ),
    _p(
        "自定义上下文管理器",
        "实现一个上下文管理器，进入时输出 enter，执行时输出 body，退出时输出 exit。",
        "medium",
        "上下文管理器,__enter__,__exit__",
        [
            ("", "enter\nbody\nexit"),
        ],
    ),
    _p(
        "functools partial",
        "输入一个整数 n，使用 functools.partial 固定平方函数的指数为 2，输出 n 的平方。",
        "medium",
        "functools,partial,高级语法",
        [
            ("3", "9"),
            ("4", "16"),
            ("5", "25"),
        ],
    ),
    _p(
        "any 判断",
        "输入一行整数，使用 any 判断是否存在偶数，存在输出 yes，否则输出 no。",
        "medium",
        "any,高级语法",
        [
            ("1 3 5 6", "yes"),
            ("1 3 5", "no"),
            ("2 4", "yes"),
        ],
    ),
    _p(
        "all 判断",
        "输入一行整数，使用 all 判断是否全部大于 0，是则输出 yes，否则输出 no。",
        "medium",
        "all,高级语法",
        [
            ("1 2 3", "yes"),
            ("1 -2 3", "no"),
            ("0 1", "no"),
        ],
    ),
    _p(
        "abs 绝对值",
        "输入一个数字，使用 abs 输出绝对值。",
        "easy",
        "内置函数,abs",
        [
            ("-7", "7"),
            ("5", "5"),
            ("-0.5", "0.5"),
        ],
    ),
    _p(
        "round 保留小数",
        "第一行输入小数，第二行输入保留位数，使用 round 输出结果。",
        "easy",
        "内置函数,round",
        [
            ("3.14159\n2", "3.14"),
            ("1.5\n0", "2"),
            ("123.456\n1", "123.5"),
        ],
    ),
    _p(
        "itertools 排列数",
        "输入一个字符串，使用 itertools.permutations 输出它的全排列数量。",
        "medium",
        "itertools,permutations,高级语法",
        [
            ("ab", "2"),
            ("abc", "6"),
            ("abcd", "24"),
        ],
    ),
]


ADVANCED_STARTER_CODES = {
    "字符串首字母大写": """s = input().strip()
print(s.capitalize())
""",
    "字符串去除首尾空格": """s = input().strip()
print(s.strip())
""",
    "前缀判断": """s = input().strip()
prefix = input().strip()
print("yes" if s.startswith(prefix) else "no")
""",
    "后缀判断": """s = input().strip()
suffix = input().strip()
print("yes" if s.endswith(suffix) else "no")
""",
    "查找子串位置": """s = input().strip()
target = input().strip()
print(s.find(target))
""",
    "字符串分割数量": """words = input().split()
print(len(words))
""",
    "字符串连接": """words = input().split()
print("-".join(words))
""",
    "数字补零": """s = input().strip()
print(s.zfill(3))
""",
    "列表插入": """nums = list(map(int, input().split()))
index = int(input())
value = int(input())
nums.insert(index, value)
print(" ".join(map(str, nums)))
""",
    "列表删除指定值": """items = input().split()
target = input().strip()
items.remove(target)
print(" ".join(items))
""",
    "列表弹出": """nums = list(map(int, input().split()))
index = int(input())
nums.pop(index)
print(" ".join(map(str, nums)))
""",
    "列表扩展": """a = input().split()
b = input().split()
a.extend(b)
print(" ".join(a))
""",
    "列表查找下标": """items = input().split()
target = input().strip()
try:
    print(items.index(target))
except ValueError:
    print(-1)
""",
    "列表复制反转": """nums = list(map(int, input().split()))
copy = nums.copy()
copy.reverse()
print(" ".join(map(str, copy)))
""",
    "列表清空长度": """nums = list(map(int, input().split()))
nums.clear()
print(len(nums))
""",
    "字典 get 默认值": """data = {"apple": 3, "banana": 5}
key = input().strip()
print(data.get(key, "not found"))
""",
    "字典成员判断": """data = {"apple": 3, "banana": 5}
key = input().strip()
print("yes" if key in data else "no")
""",
    "集合差集": """a = set(map(int, input().split()))
b = set(map(int, input().split()))
print(" ".join(map(str, sorted(a - b))))
""",
    "集合对称差": """a = set(map(int, input().split()))
b = set(map(int, input().split()))
print(" ".join(map(str, sorted(a ^ b))))
""",
    "集合添加": """s = set(map(int, input().split()))
value = int(input())
s.add(value)
print(" ".join(map(str, sorted(s))))
""",
    "集合安全删除": """s = set(map(int, input().split()))
value = int(input())
s.discard(value)
print(" ".join(map(str, sorted(s))))
""",
    "子集判断": """a = set(map(int, input().split()))
b = set(map(int, input().split()))
print("yes" if a.issubset(b) else "no")
""",
    "for-else 查找": """nums = list(map(int, input().split()))
for n in nums:
    if n % 2 == 0:
        print("found")
        break
else:
    print("not found")
""",
    "while-else 结束判断": """n = int(input())
if n < 0:
    print("invalid")
else:
    while n > 0:
        n -= 1
    else:
        print("done")
""",
    "match-case 数字转英文": """n = int(input())
match n:
    case 1:
        print("one")
    case 2:
        print("two")
    case _:
        print("other")
""",
    "关键字参数幂运算": """base, exp = map(int, input().split())
print(pow(base=base, exp=exp))
""",
    "**kwargs 拼接": """def format_kwargs(**kwargs):
    return ",".join(f"{key}={value}" for key, value in kwargs.items())

pairs = input().split()
data = {pairs[i]: pairs[i + 1] for i in range(0, len(pairs), 2)}
print(format_kwargs(**data))
""",
    "返回多个值": """def calc(a, b):
    return a + b, a * b

a, b = map(int, input().split())
total, product = calc(a, b)
print(total, product)
""",
    "lambda 多参数": """multiply = lambda x, y: x * y
a, b = map(int, input().split())
print(multiply(a, b))
""",
    "字典推导式": """words = input().split()
counter = {word: len(word) for word in words}
for word, length in counter.items():
    print(f"{word}:{length}")
""",
    "集合推导式": """nums = map(int, input().split())
squares = {x * x for x in nums}
print(" ".join(map(str, sorted(squares))))
""",
    "条件列表推导式": """nums = map(int, input().split())
squares = [x * x for x in nums if x % 2 == 0]
print(" ".join(map(str, squares)))
""",
    "递归反转字符串": """def reverse_string(s):
    if len(s) <= 1:
        return s
    return reverse_string(s[1:]) + s[0]

s = input().strip()
print(reverse_string(s))
""",
    "递归幂运算": """def power(base, exp):
    if exp == 0:
        return 1
    return base * power(base, exp - 1)

base, exp = map(int, input().split())
print(power(base, exp))
""",
    "iter next 取首元素": """items = iter(input().split())
print(next(items))
""",
    "yield from 合并": """def chain(a, b):
    yield from a
    yield from b

a = input().split()
b = input().split()
print(" ".join(chain(a, b)))
""",
    "classmethod 工厂方法": """class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def from_line(cls, line):
        name, age = line.split()
        return cls(name, age)

    def __str__(self):
        return f"{self.name} is {self.age} years old"

line = input().strip()
print(Person.from_line(line))
""",
    "staticmethod 工具方法": """class Math:
    @staticmethod
    def add(a, b):
        return a + b

a, b = map(int, input().split())
print(Math.add(a, b))
""",
    "property 面积": """class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        return 3.14 * self.radius * self.radius

radius = float(input())
print(Circle(radius).area)
""",
    "__str__ 魔术方法": """class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point({self.x},{self.y})"

x, y = map(int, input().split())
print(Point(x, y))
""",
    "__eq__ 魔术方法": """class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

x1, y1 = map(int, input().split())
x2, y2 = map(int, input().split())
print(Point(x1, y1) == Point(x2, y2))
""",
    "try except else": """try:
    a, b = map(int, input().split())
    result = a // b
except ZeroDivisionError:
    print("error")
else:
    print(result)
    print("success")
""",
    "finally 清理": """try:
    n = int(input())
    print(n)
except ValueError:
    print("error")
finally:
    print("finally")
""",
    "自定义上下文管理器": """class Manager:
    def __enter__(self):
        print("enter")
        return self

    def __exit__(self, exc_type, exc, tb):
        print("exit")

with Manager():
    print("body")
""",
    "functools partial": """from functools import partial

square = partial(pow, exp=2)
n = int(input())
print(square(n))
""",
    "any 判断": """nums = map(int, input().split())
print("yes" if any(n % 2 == 0 for n in nums) else "no")
""",
    "all 判断": """nums = map(int, input().split())
print("yes" if all(n > 0 for n in nums) else "no")
""",
    "abs 绝对值": """n = float(input())
print(abs(n))
""",
    "round 保留小数": """value = float(input())
digits = int(input())
print(round(value, digits))
""",
    "itertools 排列数": """from itertools import permutations

s = input().strip()
print(len(list(permutations(s))))
""",
}


ADVANCED_STARTER_HINTS = {
    "字符串首字母大写": "capitalize 会把首字母转大写、其余字母转小写。",
    "字符串去除首尾空格": "strip 可以同时去掉字符串首尾的空白。",
    "前缀判断": "startswith 会返回布尔值，用来判断是否以指定前缀开头。",
    "后缀判断": "endswith 会返回布尔值，用来判断是否以指定后缀结尾。",
    "查找子串位置": "find 找不到子串时会返回 -1。",
    "字符串分割数量": "split 默认按空白拆分字符串，返回单词列表。",
    "字符串连接": "join 是字符串方法，可以把列表元素拼接成一个字符串。",
    "数字补零": "zfill(n) 会把字符串补到 n 位，不足部分补 0。",
    "列表插入": "insert(index, value) 会在指定下标之前插入一个值。",
    "列表删除指定值": "remove 只删除列表中第一次出现的指定值。",
    "列表弹出": "pop(index) 会删除指定下标元素，并返回被删除的值。",
    "列表扩展": "extend 会把另一个列表的元素逐个追加到当前列表。",
    "列表查找下标": "index 找不到目标时会抛 ValueError，需要捕获。",
    "列表复制反转": "copy 创建独立副本，reverse 会原地反转列表。",
    "列表清空长度": "clear 清空列表，len 返回列表长度。",
    "字典 get 默认值": "get(key, default) 在键不存在时返回默认值，避免 KeyError。",
    "字典成员判断": "key in dict 可以判断字典中是否存在该键。",
    "集合差集": "a - b 返回只在集合 a 中出现的元素。",
    "集合对称差": "a ^ b 返回只属于其中一个集合的元素。",
    "集合添加": "add 向集合添加元素，集合会自动去重。",
    "集合安全删除": "discard 删除元素，即使元素不存在也不会报错。",
    "子集判断": "issubset 判断一个集合是否被另一个集合包含。",
    "for-else 查找": "for 循环没有被 break 中断时，会执行 else 分支。",
    "while-else 结束判断": "while 循环正常结束时会执行 else 分支。",
    "match-case 数字转英文": "match/case 是 Python 3.10+ 提供的分支匹配语法。",
    "关键字参数幂运算": "pow(base=..., exp=...) 演示了函数的关键字传参方式。",
    "**kwargs 拼接": "**kwargs 会把多余的键值对收集成一个字典。",
    "返回多个值": "函数返回多个值时，实际返回的是一个元组。",
    "lambda 多参数": "lambda 可以定义匿名函数，并且支持多个参数。",
    "字典推导式": "字典推导式可以快速生成 键:值 映射。",
    "集合推导式": "集合推导式会先计算再自动去重。",
    "条件列表推导式": "列表推导式可以在后面加 if 条件进行过滤。",
    "递归反转字符串": "递归需要设置出口，空串或单字符直接返回。",
    "递归幂运算": "递归幂运算需要设置 exp == 0 作为出口。",
    "iter next 取首元素": "iter 把可迭代对象变成迭代器，next 取出下一个值。",
    "yield from 合并": "yield from 会把另一个可迭代对象的元素逐个产出。",
    "classmethod 工厂方法": "classmethod 的第一个参数是类，适合编写工厂方法。",
    "staticmethod 工具方法": "staticmethod 不依赖实例，适合放置工具函数。",
    "property 面积": "property 可以把方法变成属性一样访问。",
    "__str__ 魔术方法": "__str__ 控制使用 print 输出对象时的显示内容。",
    "__eq__ 魔术方法": "__eq__ 定义两个对象是否相等的比较规则。",
    "try except else": "try 没有捕获到异常时，会执行 else 分支。",
    "finally 清理": "finally 无论是否出错都会执行，适合做清理操作。",
    "自定义上下文管理器": "__enter__ 和 __exit__ 实现 with 语句的进入和退出协议。",
    "functools partial": "partial 可以提前固定函数的部分参数。",
    "any 判断": "any 只要有一个元素为真就返回 True。",
    "all 判断": "all 要求所有元素都为真才返回 True。",
    "abs 绝对值": "abs 返回数字的绝对值。",
    "round 保留小数": "round 的第二个参数控制保留的小数位数。",
    "itertools 排列数": "permutations 返回全排列，排列数量等于字符串长度的阶乘。",
}
