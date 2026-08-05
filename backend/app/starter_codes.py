from .advanced_python_problems import ADVANCED_STARTER_CODES, ADVANCED_STARTER_HINTS
from .code_comments import add_line_comments
from .curriculum_problems import CURRICULUM_STARTER_CODES
from .curriculum_problems_extra import CURRICULUM_EXTRA_STARTER_CODES


DEFAULT_STARTER = """def solve():
    data = input().strip()
    # 请根据题目要求处理 data 并输出结果
    print(data)

solve()
"""


STARTER_CODES = {
    "两数之和": """def solve():
    a, b = map(int, input().split())
    print(a + b)

solve()
""",
    "斐波那契数列": """def fib(n):
    if n <= 2:
        return 1
    return fib(n - 1) + fib(n - 2)

n = int(input())
print(fib(n))
""",
    "三个数之和": """a, b, c = map(int, input().split())
print(a + b + c)
""",
    "判断奇偶": """n = int(input())
# 使用 % 判断奇偶并输出 odd 或 even
print()
""",
    "三个数最大值": """a, b, c = map(int, input().split())
print(max(a, b, c))
""",
    "字符串反转": """s = input().strip()
print(s[::-1])
""",
    "列表求和": """nums = list(map(int, input().split()))
print(sum(nums))
""",
    "判断回文": """s = input().strip()
# 比较 s 和 s[::-1]，输出 yes 或 no
print()
""",
    "统计元音": """s = input().strip()
vowels = "aeiou"
# 统计 s 中元音数量并输出
print()
""",
    "列表去重": """nums = list(map(int, input().split()))
seen = []
# 按出现顺序去重
print(" ".join(map(str, seen)))
""",
    "计算阶乘": """def factorial(n):
    # 使用递归或循环实现阶乘
    return 1

n = int(input())
print(factorial(n))
""",
    "判断素数": """def is_prime(n):
    # 判断 n 是否为素数
    return False

n = int(input())
print("prime" if is_prime(n) else "not prime")
""",
    "大小写转换": """s = input().strip()
print(s.swapcase())
""",
    "单词词频统计": """words = input().split()
counter = {}
# 统计每个单词出现次数
for word, count in counter.items():
    print(f"{word}:{count}")
""",
    "冒泡排序": """nums = list(map(int, input().split()))
# 使用冒泡排序升序排列
print(" ".join(map(str, nums)))
""",
    "二分查找": """def binary_search(nums, target):
    # 实现二分查找
    return -1

nums = list(map(int, input().split()))
target = int(input())
print(binary_search(nums, target))
""",
    "递归求和": """def recursive_sum(n):
    # 使用递归计算 1+2+...+n
    return n

n = int(input())
print(recursive_sum(n))
""",
    "平方生成器": """def squares(n):
    for i in range(1, n + 1):
        yield i * i

n = int(input())
print(" ".join(map(str, squares(n))))
""",
    "筛选偶数": """nums = list(map(int, input().split()))
even = list(filter(lambda x: x % 2 == 0, nums))
print(" ".join(map(str, even)))
""",
    "乘方装饰器": """def doubler(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs) * 2
    return wrapper

@doubler
def fn(n):
    return n

n = int(input())
print(fn(n))
""",
    "矩形面积类": """class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

w, h = map(int, input().split())
print(Rectangle(w, h).area())
""",
    "安全除法": """try:
    a, b = map(int, input().split())
    print(a // b)
except ZeroDivisionError:
    print("error")
""",
    "字符串排序": """words = input().split()
for word in sorted(words):
    print(word)
""",
    "立方列表推导式": """n = int(input())
cubes = [i ** 3 for i in range(1, n + 1)]
print(" ".join(map(str, cubes)))
""",
    "输出 Hello World": """print("Hello World")
""",
    "整数除法与余数": """a, b = map(int, input().split())
print(a // b, a % b)
""",
    "字符串长度": """s = input().strip()
print(len(s))
""",
    "字符串拼接": """a = input().strip()
b = input().strip()
print(a + b)
""",
    "字符串替换": """s = input().strip()
print(s.replace("hello", "hi"))
""",
    "字符串转整数": """s = input().strip()
print(int(s) + 1)
""",
    "f-string 格式化": """name, age = input().split()
print(f"{name} is {age} years old")
""",
    "列表索引": """nums = list(map(int, input().split()))
index = int(input())
print(nums[index])
""",
    "列表尾部添加": """nums = list(map(int, input().split()))
value = int(input())
nums.append(value)
print(" ".join(map(str, nums)))
""",
    "列表反转": """nums = list(map(int, input().split()))
print(" ".join(map(str, nums[::-1])))
""",
    "元素出现次数": """items = input().split()
target = input().strip()
print(items.count(target))
""",
    "元组解包": """a, b = input().split()
print(f"a={a} b={b}")
""",
    "集合交集": """a = set(map(int, input().split()))
b = set(map(int, input().split()))
print(" ".join(map(str, sorted(a & b))))
""",
    "集合并集": """a = set(map(int, input().split()))
b = set(map(int, input().split()))
print(" ".join(map(str, sorted(a | b))))
""",
    "while 循环求和": """n = int(input())
total = 0
i = 0
# 使用 while 累加 0 到 n
print(total)
""",
    "第一个偶数": """nums = list(map(int, input().split()))
# 使用 break 找到第一个偶数
print(-1)
""",
    "enumerate 下标": """items = input().split()
for index, item in enumerate(items):
    print(f"{index}:{item}")
""",
    "zip 合并": """a = input().split()
b = input().split()
for x, y in zip(a, b):
    print(f"{x}-{y}")
""",
    "条件表达式": """n = int(input())
result = "positive" if n > 0 else "non-positive"
print(result)
""",
    "函数默认参数": """def multiply(a, b=2):
    return a * b

args = list(map(int, input().split()))
print(multiply(*args))
""",
    "*args 求和": """def total(*args):
    return sum(args)

print(total(*map(int, input().split())))
""",
    "lambda 长度排序": """words = input().split()
print(" ".join(sorted(words, key=lambda word: len(word))))
""",
    "map 平方": """nums = list(map(int, input().split()))
print(" ".join(map(str, map(lambda x: x * x, nums))))
""",
    "filter 长度筛选": """words = input().split()
long_words = list(filter(lambda word: len(word) > 2, words))
print(" ".join(long_words))
""",
    "二进制转换": """n = int(input())
print(bin(n)[2:])
""",
    "十六进制转换": """n = int(input())
print(hex(n)[2:])
""",
    "最大公约数": """import math

a, b = map(int, input().split())
print(math.gcd(a, b))
""",
    "最小公倍数": """import math

a, b = map(int, input().split())
print(a * b // math.gcd(a, b))
""",
    "水仙花数": """n = int(input())
# 判断 n 是否为水仙花数
print("no")
""",
    "完数": """n = int(input())
# 计算除自身外所有正因数之和
print("no")
""",
    "反转数字": """n = int(input())
# 处理正负号并反转数字
print()
""",
    "首字母大写": """s = input().strip()
print(s.title())
""",
    "最长单词": """words = input().split()
print(max(words, key=len))
""",
    "装饰器转大写": """def uppercase(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper

@uppercase
def echo(s):
    return s

s = input().strip()
print(echo(s))
""",
    "类继承": """class Animal:
    def sound(self):
        return "unknown"

class Dog(Animal):
    def sound(self):
        return "bark"

class Cat(Animal):
    def sound(self):
        return "meow"

animal = input().strip()
print(Dog().sound() if animal == "dog" else Cat().sound())
""",
    "自定义异常": """class NegativeNumberError(Exception):
    pass

try:
    n = int(input())
    if n < 0:
        raise NegativeNumberError("negative")
    print(n)
except NegativeNumberError:
    print("error")
""",
}


ALL_STARTER_CODES = {
    **STARTER_CODES,
    **ADVANCED_STARTER_CODES,
    **CURRICULUM_STARTER_CODES,
    **CURRICULUM_EXTRA_STARTER_CODES,
}


def get_starter_code(problem) -> str:
    custom_code = getattr(problem, "starter_code", None)
    code = custom_code or ALL_STARTER_CODES.get(problem.title, DEFAULT_STARTER)
    hint = ADVANCED_STARTER_HINTS.get(problem.title)
    header = (
        f"# 题目：{problem.title}\n"
        f"# 知识点：{problem.tags or 'Python'}\n"
    )
    if hint:
        header += f"# 提示：{hint}\n"
    header += "# 先读取输入，再按题目要求处理，最后用 print 输出结果\n\n"
    return add_line_comments(header + code)
