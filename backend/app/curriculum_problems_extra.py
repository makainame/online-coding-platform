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


_EXTRA = [
    (
        "输出两行文字",
        "不读取输入，使用 print 输出两行文字：第一行 和 第二行。",
        "easy",
        "Day01,print,转义符",
        [("", "第一行\n第二行")],
        """print("第一行")
print("第二行")
""",
    ),
    (
        "注释不影响输出",
        "代码中包含注释，程序输出 hello。",
        "easy",
        "Day01,注释",
        [("", "hello")],
        """# 这是一行注释
print("hello")  # 输出 hello
""",
    ),
    (
        "变量多次赋值",
        "给变量 x 依次赋值 1、2、3，最后输出 x。",
        "easy",
        "Day01,变量",
        [("", "3")],
        """x = 1
x = 2
x = 3
print(x)
""",
    ),
    (
        "查看变量类型",
        "输入一个值，使用 type 输出它的类型名称。",
        "easy",
        "Day01,type,数据类型",
        [
            ("123", "int"),
            ("3.14", "float"),
            ("hello", "str"),
        ],
        """value = input().strip()
print(type(value).__name__)
""",
    ),
    (
        "整数转浮点数",
        "输入一个整数，使用 float 转成浮点数并输出。",
        "easy",
        "Day01,float,类型转换",
        [
            ("5", "5.0"),
            ("10", "10.0"),
            ("-3", "-3.0"),
        ],
        """n = int(input())
print(float(n))
""",
    ),
    (
        "字符串转整数加十",
        "输入一个整数字符串，使用 int 转成整数后加 10 输出。",
        "easy",
        "Day01,int,类型转换",
        [
            ("5", "15"),
            ("20", "30"),
            ("-8", "2"),
        ],
        """s = input().strip()
print(int(s) + 10)
""",
    ),
    (
        "临时变量交换",
        "输入两个值，使用临时变量完成交换后输出。",
        "easy",
        "Day02,变量交换",
        [
            ("3 5", "5 3"),
            ("a b", "b a"),
            ("10 20", "20 10"),
        ],
        """a, b = input().split()
temp = a
a = b
b = temp
print(a, b)
""",
    ),
    (
        "算术交换两个数",
        "输入两个整数，使用加减法完成交换后输出。",
        "easy",
        "Day02,算术运算,变量交换",
        [
            ("3 5", "5 3"),
            ("10 20", "20 10"),
            ("-1 4", "4 -1"),
        ],
        """a, b = map(int, input().split())
a = a + b
b = a - b
a = a - b
print(a, b)
""",
    ),
    (
        "百分号格式化",
        "输入姓名和成绩，使用 %s 和 %.2f 格式化输出。",
        "easy",
        "Day02,格式化,百分号",
        [
            ("Python 3.14159", "Python 的分数是 3.14"),
            ("Tom 2.5", "Tom 的分数是 2.50"),
        ],
        """name, score = input().split()
print("%s 的分数是 %.2f" % (name, float(score)))
""",
    ),
    (
        "整数补零格式化",
        "输入一个整数，使用 %04d 输出 4 位整数，不足补 0。",
        "easy",
        "Day02,格式化,补零",
        [
            ("7", "0007"),
            ("123", "0123"),
            ("12345", "12345"),
        ],
        """n = int(input())
print("%04d" % n)
""",
    ),
    (
        "输入姓名年龄",
        "输入姓名和年龄，用空格分隔，输出 姓名今年年龄岁。",
        "easy",
        "Day02,input,f-string",
        [
            ("Tom 18", "Tom今年18岁"),
            ("小红 20", "小红今年20岁"),
        ],
        """name, age = input().split()
print(f"{name}今年{age}岁")
""",
    ),
    (
        "转义符换行",
        "不读取输入，使用 \\n 输出两行文字。",
        "easy",
        "Day02,转义符",
        [("", "第一行\n第二行")],
        """print("第一行\\n第二行")
""",
    ),
    (
        "两个字符串转整数求和",
        "输入两个整数字符串，使用 int 转换后求和输出。",
        "easy",
        "Day02,int,类型转换",
        [
            ("123 45", "168"),
            ("10 20", "30"),
            ("-5 5", "0"),
        ],
        """a, b = input().split()
print(int(a) + int(b))
""",
    ),
    (
        "eval 还原数值",
        "输入一个字符串表示的数值，使用 eval 还原后加 1 输出。",
        "medium",
        "Day02,eval,类型转换",
        [
            ("10", "11"),
            ("3.5", "4.5"),
            ("-2", "-1"),
        ],
        """value = eval(input().strip())
print(value + 1)
""",
    ),
    (
        "比较运算结果",
        "输入两个整数，输出 a > b 的比较结果。",
        "easy",
        "Day02,比较运算符",
        [
            ("3 5", "False"),
            ("5 3", "True"),
            ("4 4", "False"),
        ],
        """a, b = map(int, input().split())
print(a > b)
""",
    ),
    (
        "逻辑与范围判断",
        "输入一个年龄，使用 and 判断是否在 18 到 59 之间，输出 成年 或 其他。",
        "easy",
        "Day02,逻辑运算,and",
        [
            ("18", "成年"),
            ("17", "其他"),
            ("60", "其他"),
        ],
        """age = int(input())
print("成年" if 18 <= age < 60 else "其他")
""",
    ),
    (
        "逻辑或判断",
        "输入一个字符，使用 or 判断是否为 a 或 b，输出 是 或 否。",
        "easy",
        "Day02,逻辑运算,or",
        [
            ("a", "是"),
            ("b", "是"),
            ("c", "否"),
        ],
        """ch = input().strip()
print("是" if ch == "a" or ch == "b" else "否")
""",
    ),
    (
        "if 嵌套成绩等级",
        "输入成绩，先判断是否及格，再判断是否优秀，输出 优秀、及格 或 不及格。",
        "easy",
        "Day02,if,嵌套",
        [
            ("92", "优秀"),
            ("75", "及格"),
            ("40", "不及格"),
        ],
        """score = int(input())
if score >= 60:
    if score >= 85:
        print("优秀")
    else:
        print("及格")
else:
    print("不及格")
""",
    ),
    (
        "三元取较大值",
        "输入两个整数，使用三元运算符输出较大的数。",
        "easy",
        "Day03,三元运算符",
        [
            ("3 8", "8"),
            ("9 2", "9"),
            ("5 5", "5"),
        ],
        """a, b = map(int, input().split())
print(a if a > b else b)
""",
    ),
    (
        "while 倒序输出",
        "输入一个正整数 n，使用 while 从 n 倒序输出到 1。",
        "easy",
        "Day03,while,循环",
        [
            ("3", "3 2 1"),
            ("5", "5 4 3 2 1"),
            ("1", "1"),
        ],
        """n = int(input())
while n >= 1:
    print(n, end=" ")
    n -= 1
""",
    ),
    (
        "while 奇数和",
        "输入一个正整数 n，使用 while 计算 1 到 n 的奇数和。",
        "easy",
        "Day03,while,奇数,求和",
        [
            ("10", "25"),
            ("5", "9"),
            ("1", "1"),
        ],
        """n = int(input())
i = 1
total = 0
while i <= n:
    total += i
    i += 2
print(total)
""",
    ),
    (
        "break 提前停止",
        "输入一个正整数 n，从 1 开始输出，遇到 3 时使用 break 停止。",
        "easy",
        "Day03,break,循环",
        [
            ("3", "1 2"),
            ("5", "1 2"),
            ("2", "1 2"),
        ],
        """n = int(input())
for i in range(1, n + 1):
    if i == 3:
        break
    print(i, end=" ")
""",
    ),
    (
        "continue 打印奇数",
        "输入一个正整数 n，使用 continue 输出 1 到 n 的所有奇数。",
        "easy",
        "Day03,continue,循环",
        [
            ("5", "1 3 5"),
            ("6", "1 3 5"),
            ("1", "1"),
        ],
        """n = int(input())
for i in range(1, n + 1):
    if i % 2 == 0:
        continue
    print(i, end=" ")
""",
    ),
    (
        "for range 步长",
        "输入一个正整数 n，使用 range 步长输出 0 到 n 的所有偶数。",
        "easy",
        "Day03,for,range,步长",
        [
            ("10", "0 2 4 6 8 10"),
            ("6", "0 2 4 6"),
            ("1", "0"),
        ],
        """n = int(input())
for i in range(0, n + 1, 2):
    print(i, end=" ")
""",
    ),
    (
        "for 遍历字符串",
        "输入一个字符串，使用 for 逐字符输出，每行一个字符。",
        "easy",
        "Day03,for,字符串",
        [
            ("abc", "a\nb\nc"),
            ("hi", "h\ni"),
            ("x", "x"),
        ],
        """s = input().strip()
for ch in s:
    print(ch)
""",
    ),
    (
        "循环 else 正常结束",
        "输入正整数 n，使用 for 正常结束后输出 结束。",
        "easy",
        "Day03,for,else",
        [
            ("3", "1 2 3 结束"),
            ("1", "1 结束"),
        ],
        """n = int(input())
for i in range(1, n + 1):
    print(i, end=" ")
else:
    print("结束")
""",
    ),
    (
        "循环 else break 不执行",
        "输入正整数 n，遇到 2 时 break，观察 else 不执行。",
        "easy",
        "Day03,break,else",
        [
            ("3", "1"),
            ("5", "1"),
        ],
        """n = int(input())
for i in range(1, n + 1):
    if i == 2:
        break
    print(i)
else:
    print("没有 break")
""",
    ),
    (
        "三位水仙花数判断",
        "输入一个三位数，判断是否为水仙花数，输出 是 或 不是。",
        "medium",
        "Day03,水仙花数,循环",
        [
            ("153", "是"),
            ("370", "是"),
            ("123", "不是"),
        ],
        """n = int(input())
a = n // 100
b = n // 10 % 10
c = n % 10
print("是" if a ** 3 + b ** 3 + c ** 3 == n else "不是")
""",
    ),
    (
        "打印正三角形",
        "输入一个正整数 n，使用循环嵌套打印 n 行 * 正三角形。",
        "medium",
        "Day03,循环嵌套,三角形",
        [
            ("3", "*\n**\n***"),
            ("2", "*\n**"),
            ("1", "*"),
        ],
        """n = int(input())
for i in range(1, n + 1):
    print("*" * i)
""",
    ),
    (
        "乘法表某一行",
        "输入一个正整数 n，输出九九乘法表第 n 行。",
        "medium",
        "Day03,循环嵌套,乘法表",
        [
            ("3", "1x3=3 2x3=6 3x3=9"),
            ("2", "1x2=2 2x2=4"),
            ("1", "1x1=1"),
        ],
        """n = int(input())
for i in range(1, n + 1):
    print(f"{i}x{n}={i * n}", end=" ")
""",
    ),
    (
        "模拟登录",
        "固定密码为 123456，输入密码，正确输出 登录成功，错误输出 密码错误。",
        "medium",
        "Day03,if,登录",
        [
            ("123456", "登录成功"),
            ("000000", "密码错误"),
        ],
        """password = input().strip()
print("登录成功" if password == "123456" else "密码错误")
""",
    ),
    (
        "字符串索引",
        "第一行输入字符串，第二行输入下标，输出该下标字符。",
        "easy",
        "Day04,字符串,索引",
        [
            ("hello\n1", "e"),
            ("hello\n-1", "o"),
            ("Python\n0", "P"),
        ],
        """s = input().strip()
index = int(input())
print(s[index])
""",
    ),
    (
        "字符串切片",
        "第一行输入字符串，第二行输入起始下标，输出从该下标到末尾的子串。",
        "easy",
        "Day04,字符串,切片",
        [
            ("hello world\n6", "world"),
            ("Python\n3", "hon"),
            ("abc\n0", "abc"),
        ],
        """s = input().strip()
index = int(input())
print(s[index:])
""",
    ),
    (
        "字符串 find",
        "第一行输入字符串，第二行输入子串，使用 find 输出第一次出现位置。",
        "easy",
        "Day04,字符串,find",
        [
            ("hello world\nworld", "6"),
            ("abcabc\nbc", "1"),
            ("hello\nz", "-1"),
        ],
        """s = input().strip()
target = input().strip()
print(s.find(target))
""",
    ),
    (
        "字符串 rfind",
        "第一行输入字符串，第二行输入子串，使用 rfind 输出最后一次出现位置。",
        "easy",
        "Day04,字符串,rfind",
        [
            ("abcabc\nbc", "4"),
            ("hello\nl", "3"),
            ("hello\nz", "-1"),
        ],
        """s = input().strip()
target = input().strip()
print(s.rfind(target))
""",
    ),
    (
        "字符串 count",
        "第一行输入字符串，第二行输入子串，使用 count 输出出现次数。",
        "easy",
        "Day04,字符串,count",
        [
            ("banana\na", "3"),
            ("hello\nl", "2"),
            ("python\nx", "0"),
        ],
        """s = input().strip()
target = input().strip()
print(s.count(target))
""",
    ),
    (
        "字符串 replace",
        "输入一个字符串，把 hello 替换成 hi 后输出。",
        "easy",
        "Day04,字符串,replace",
        [
            ("hello world", "hi world"),
            ("hellohello", "hihi"),
            ("python", "python"),
        ],
        """s = input().strip()
print(s.replace("hello", "hi"))
""",
    ),
    (
        "split 单词数量",
        "输入一行英文，使用 split 输出单词数量。",
        "easy",
        "Day04,字符串,split",
        [
            ("a b c", "3"),
            ("hello", "1"),
            ("python is fun", "3"),
        ],
        """words = input().split()
print(len(words))
""",
    ),
    (
        "join 拼接",
        "输入一行英文，使用 join 以逗号连接输出。",
        "easy",
        "Day04,字符串,join",
        [
            ("a b c", "a,b,c"),
            ("python is fun", "python,is,fun"),
            ("x y", "x,y"),
        ],
        """words = input().split()
print(",".join(words))
""",
    ),
    (
        "字符串大小写",
        "输入一个字符串，分别输出大写和小写结果。",
        "easy",
        "Day04,字符串,upper,lower",
        [
            ("Hello", "HELLO\nhello"),
            ("Python", "PYTHON\npython"),
        ],
        """s = input().strip()
print(s.upper())
print(s.lower())
""",
    ),
    (
        "isdigit 判断",
        "输入一个字符串，使用 isdigit 判断是否全是数字，输出 数字 或 不是数字。",
        "easy",
        "Day04,字符串,isdigit",
        [
            ("123", "数字"),
            ("12a", "不是数字"),
            ("3.14", "不是数字"),
        ],
        """s = input().strip()
print("数字" if s.isdigit() else "不是数字")
""",
    ),
    (
        "列表 while 遍历",
        "输入一行元素，使用 while 按下标遍历输出，每行一个。",
        "easy",
        "Day04,列表,while,遍历",
        [
            ("a b c", "a\nb\nc"),
            ("1 2", "1\n2"),
        ],
        """items = input().split()
index = 0
while index < len(items):
    print(items[index])
    index += 1
""",
    ),
    (
        "列表 for 遍历",
        "输入一行元素，使用 for 直接遍历输出，每行一个。",
        "easy",
        "Day04,列表,for,遍历",
        [
            ("a b c", "a\nb\nc"),
            ("x y z", "x\ny\nz"),
        ],
        """items = input().split()
for item in items:
    print(item)
""",
    ),
    (
        "列表 append insert",
        "输入一个列表，末尾追加 9，并在下标 1 插入 0，最后输出。",
        "easy",
        "Day04,列表,append,insert",
        [
            ("1 2 3", "1 0 2 3 9"),
            ("5", "5 0 9"),
        ],
        """nums = list(map(int, input().split()))
nums.append(9)
nums.insert(1, 0)
print(" ".join(map(str, nums)))
""",
    ),
    (
        "列表 pop remove",
        "输入一个列表，先 remove 第一次出现的 2，再 pop 下标 1，最后输出。",
        "easy",
        "Day04,列表,pop,remove",
        [
            ("1 2 3", "1 3"),
            ("2 1 2", "1"),
            ("3 2 1", "3 1"),
        ],
        """nums = list(map(int, input().split()))
if 2 in nums:
    nums.remove(2)
nums.pop(1)
print(" ".join(map(str, nums)))
""",
    ),
    (
        "列表 sort reverse",
        "输入一个整数列表，升序排序后再反转，最后输出。",
        "easy",
        "Day04,列表,sort,reverse",
        [
            ("3 1 2", "3 2 1"),
            ("5 4 6", "6 5 4"),
        ],
        """nums = list(map(int, input().split()))
nums.sort()
nums.reverse()
print(" ".join(map(str, nums)))
""",
    ),
    (
        "列表嵌套取值",
        "定义矩阵 [[1,2,3],[4,5,6]]，输入两个下标，输出对应元素。",
        "medium",
        "Day04,列表,嵌套",
        [
            ("0 1", "2"),
            ("1 2", "6"),
            ("1 0", "4"),
        ],
        """matrix = [[1, 2, 3], [4, 5, 6]]
i, j = map(int, input().split())
print(matrix[i][j])
""",
    ),
    (
        "元组长度",
        "输入一行元素，把列表转成元组并输出长度。",
        "easy",
        "Day04,元组,len",
        [
            ("a b c", "3"),
            ("x y", "2"),
            ("1", "1"),
        ],
        """t = tuple(input().split())
print(len(t))
""",
    ),
    (
        "字典新增修改",
        "字典初始为空，新增 name 和 age，再把 age 改为 20，最后输出字典长度。",
        "easy",
        "Day04,字典,新增,修改",
        [("", "2")],
        """d = {}
d["name"] = "张三"
d["age"] = 18
d["age"] = 20
print(len(d))
""",
    ),
    (
        "字典删除键",
        "字典为 {'name':'张三','age':18}，输入一个键，存在则删除并输出长度，不存在直接输出长度。",
        "easy",
        "Day04,字典,删除",
        [
            ("name", "1"),
            ("age", "1"),
            ("score", "2"),
        ],
        """d = {"name": "张三", "age": 18}
key = input().strip()
if key in d:
    del d[key]
print(len(d))
""",
    ),
    (
        "字典 get",
        "字典为 {'a':1,'b':2}，输入键，使用 get 输出值，不存在输出 not found。",
        "easy",
        "Day04,字典,get",
        [
            ("a", "1"),
            ("b", "2"),
            ("c", "not found"),
        ],
        """d = {"a": 1, "b": 2}
key = input().strip()
print(d.get(key, "not found"))
""",
    ),
    (
        "字典遍历 items",
        "遍历字典 {'name':'Tom','age':18}，每行输出 键:值。",
        "easy",
        "Day04,字典,items,遍历",
        [("", "name:Tom\nage:18")],
        """d = {"name": "Tom", "age": 18}
for key, value in d.items():
    print(f"{key}:{value}")
""",
    ),
    (
        "集合交集并集差集",
        "两行输入两组整数，分别输出交集、并集和差集。",
        "medium",
        "Day05,集合,交集,并集,差集",
        [
            ("1 2 3\n2 3 4", "2 3\n1 2 3 4\n1"),
        ],
        """a = set(map(int, input().split()))
b = set(map(int, input().split()))
print(" ".join(map(str, sorted(a & b))))
print(" ".join(map(str, sorted(a | b))))
print(" ".join(map(str, sorted(a - b))))
""",
    ),
    (
        "公共 in 判断",
        "输入一行元素和一个目标值，使用 in 判断目标是否存在，输出 yes 或 no。",
        "easy",
        "Day05,公共操作,in",
        [
            ("1 2 3\n2", "yes"),
            ("a b c\nx", "no"),
        ],
        """items = input().split()
target = input().strip()
print("yes" if target in items else "no")
""",
    ),
    (
        "列表推导式 0 到 n",
        "输入正整数 n，使用列表推导式生成 0 到 n 的列表并输出。",
        "easy",
        "Day05,列表推导式",
        [
            ("5", "0 1 2 3 4 5"),
            ("3", "0 1 2 3"),
            ("0", "0"),
        ],
        """n = int(input())
nums = [i for i in range(n + 1)]
print(" ".join(map(str, nums)))
""",
    ),
    (
        "条件列表推导式整除三",
        "输入正整数 n，使用带条件的列表推导式生成 1 到 n 中能被 3 整除的数。",
        "medium",
        "Day05,列表推导式,条件",
        [
            ("10", "3 6 9"),
            ("5", "3"),
            ("1", ""),
        ],
        """n = int(input())
nums = [i for i in range(1, n + 1) if i % 3 == 0]
print(" ".join(map(str, nums)))
""",
    ),
    (
        "字典推导式合并列表",
        "两个列表 keys=['a','b'] 和 values=[1,2]，使用字典推导式合并并逐项输出。",
        "medium",
        "Day05,字典推导式,zip",
        [("", "a:1\nb:2")],
        """keys = ["a", "b"]
values = [1, 2]
d = {key: value for key, value in zip(keys, values)}
for key, value in d.items():
    print(f"{key}:{value}")
""",
    ),
    (
        "函数返回多个值",
        "输入两个整数，函数返回和与差，输出时用空格分隔。",
        "easy",
        "Day05,函数,多返回值",
        [
            ("8 3", "11 5"),
            ("10 4", "14 6"),
            ("5 9", "14 -4"),
        ],
        """def calc(a, b):
    return a + b, a - b

a, b = map(int, input().split())
total, diff = calc(a, b)
print(total, diff)
""",
    ),
    (
        "函数缺省参数",
        "输入一个或两个整数，调用缺省参数函数求乘积，第二个数缺省为 2。",
        "easy",
        "Day05,函数,缺省参数",
        [
            ("5", "10"),
            ("3 4", "12"),
            ("7 1", "7"),
        ],
        """def multiply(a, b=2):
    return a * b

args = list(map(int, input().split()))
print(multiply(*args))
""",
    ),
    (
        "*args 不定长参数求和",
        "输入一行整数，使用 *args 函数求和输出。",
        "medium",
        "Day05,函数,*args",
        [
            ("1 2 3", "6"),
            ("10 20", "30"),
            ("7", "7"),
        ],
        """def total(*args):
    return sum(args)

print(total(*map(int, input().split())))
""",
    ),
    (
        "global 修改全局变量",
        "输入一个整数，在函数内使用 global 修改全局变量并输出。",
        "medium",
        "Day05,函数,global,作用域",
        [
            ("5", "5"),
            ("10", "10"),
            ("-3", "-3"),
        ],
        """num = 0

def set_num(value):
    global num
    num = value

set_num(int(input()))
print(num)
""",
    ),
    (
        "lambda 排序",
        "输入一行英文单词，使用 lambda 按长度升序输出。",
        "medium",
        "Day06,lambda,sorted",
        [
            ("aaa b cc", "b cc aaa"),
            ("a bb ccc", "a bb ccc"),
            ("dddd a", "a dddd"),
        ],
        """words = input().split()
print(" ".join(sorted(words, key=lambda word: len(word))))
""",
    ),
    (
        "导入 math 平方根",
        "输入一个非负整数，导入 math 模块输出平方根。",
        "easy",
        "Day06,模块,math,import",
        [
            ("9", "3.0"),
            ("16", "4.0"),
            ("0", "0.0"),
        ],
        """import math

n = int(input())
print(math.sqrt(n))
""",
    ),
    (
        "导入模块别名",
        "输入一个正整数，使用 import math as m 输出它的平方根。",
        "easy",
        "Day06,模块,别名",
        [
            ("25", "5.0"),
            ("4", "2.0"),
        ],
        """import math as m

n = int(input())
print(m.sqrt(n))
""",
    ),
    (
        "编码解码",
        "输入一个字符串，使用 UTF-8 编码后再解码输出。",
        "easy",
        "Day07,编码,解码",
        [
            ("hello", "hello"),
            ("Python", "Python"),
            ("123", "123"),
        ],
        """s = input().strip()
encoded = s.encode("utf-8")
print(encoded.decode("utf-8"))
""",
    ),
    (
        "文件写入读取",
        "输入一行内容，写入 demo.txt 后再读取并输出。",
        "easy",
        "Day07,文件,写,读",
        [
            ("hello", "hello"),
            ("Python", "Python"),
        ],
        """content = input().strip()
with open("demo.txt", "w", encoding="utf-8") as f:
    f.write(content)
with open("demo.txt", "r", encoding="utf-8") as f:
    print(f.read())
""",
    ),
    (
        "os 路径拼接",
        "两行输入目录和文件名，使用 os.path.join 输出完整路径。",
        "easy",
        "Day07,os,路径",
        [
            ("dir\nfile.txt", "dir/file.txt"),
            ("home\napp.py", "home/app.py"),
        ],
        """import os

directory = input().strip()
filename = input().strip()
print(os.path.join(directory, filename))
""",
    ),
    (
        "异常 ValueError",
        "输入一个整数，转换失败输出 error，成功输出原数。",
        "easy",
        "Day07,异常,try,except",
        [
            ("abc", "error"),
            ("5", "5"),
            ("3.14", "error"),
        ],
        """try:
    n = int(input())
    print(n)
except ValueError:
    print("error")
""",
    ),
    (
        "try finally",
        "输入一个整数，转换失败输出 error，无论是否成功最后输出 finally。",
        "easy",
        "Day07,异常,finally",
        [
            ("5", "5\nfinally"),
            ("abc", "error\nfinally"),
        ],
        """try:
    n = int(input())
    print(n)
except ValueError:
    print("error")
finally:
    print("finally")
""",
    ),
    (
        "定义类和创建对象",
        "输入姓名和年龄，定义 Student 类并创建对象，输出姓名和年龄。",
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
student = Student(name, age)
print(student.name, student.age)
""",
    ),
    (
        "__init__ 默认参数",
        "输入一个可选成绩，定义 Student 类，成绩缺省为 60，输出成绩。",
        "easy",
        "进阶Day01,__init__,默认参数",
        [
            ("90", "90"),
            ("", "60"),
        ],
        """class Student:
    def __init__(self, score=60):
        self.score = score

line = input().strip()
score = int(line) if line else 60
student = Student(score)
print(student.score)
""",
    ),
    (
        "对象方法调用",
        "输入一个姓名，定义 Student 类，调用 say_hi 方法输出 你好，姓名。",
        "easy",
        "进阶Day01,方法,self",
        [
            ("Tom", "你好，Tom"),
            ("小红", "你好，小红"),
        ],
        """class Student:
    def __init__(self, name):
        self.name = name

    def say_hi(self):
        return f"你好，{self.name}"

name = input().strip()
print(Student(name).say_hi())
""",
    ),
    (
        "__str__ 输出对象",
        "输入姓名和年龄，定义 Student 类并实现 __str__，输出 姓名-年龄。",
        "easy",
        "进阶Day01,__str__",
        [
            ("Tom 18", "Tom-18"),
            ("Lily 20", "Lily-20"),
        ],
        """class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.name}-{self.age}"

name, age = input().split()
print(Student(name, age))
""",
    ),
    (
        "类属性实例属性",
        "输入一个姓名，类属性 species 为 人类，实例属性为 name，输出 人类 姓名。",
        "easy",
        "进阶Day01,类属性,实例属性",
        [
            ("Tom", "人类 Tom"),
            ("小红", "人类 小红"),
        ],
        """class Person:
    species = "人类"

    def __init__(self, name):
        self.name = name

name = input().strip()
p = Person(name)
print(p.species, p.name)
""",
    ),
    (
        "继承",
        "定义 Animal 父类和 Dog 子类，子类调用父类属性，输出 动物 和 狗。",
        "medium",
        "进阶Day02,继承",
        [("", "动物 狗")],
        """class Animal:
    kind = "动物"

class Dog(Animal):
    name = "狗"

dog = Dog()
print(dog.kind, dog.name)
""",
    ),
    (
        "方法重写",
        "定义 Animal 和 Dog 子类，重写 speak 方法，输出 汪汪。",
        "medium",
        "进阶Day02,方法重写",
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
    (
        "super 调用父类",
        "子类 __init__ 使用 super 调用父类，输出 父类名-子类名。",
        "medium",
        "进阶Day02,super,继承",
        [("", "父类名-子类名")],
        """class Parent:
    def __init__(self):
        self.name = "父类名"

class Child(Parent):
    def __init__(self):
        super().__init__()
        self.name = self.name + "-子类名"

print(Child().name)
""",
    ),
    (
        "私有属性封装",
        "定义 Student 类，私有属性 __name，通过 get_name 获取，输入姓名后输出。",
        "medium",
        "进阶Day02,封装,私有属性",
        [
            ("Tom", "Tom"),
            ("小红", "小红"),
        ],
        """class Student:
    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

name = input().strip()
print(Student(name).get_name())
""",
    ),
    (
        "多态",
        "输入 dog 或 cat，分别调用 Dog 或 Cat 的 speak，输出对应叫声。",
        "medium",
        "进阶Day02,多态",
        [
            ("dog", "汪汪"),
            ("cat", "喵喵"),
        ],
        """class Dog:
    def speak(self):
        return "汪汪"

class Cat:
    def speak(self):
        return "喵喵"

animal = input().strip()
obj = Dog() if animal == "dog" else Cat()
print(obj.speak())
""",
    ),
    (
        "抽象类",
        "使用 ABC 定义抽象类 Animal，Dog 实现 speak 后输出 汪汪。",
        "medium",
        "进阶Day02,抽象类,ABC",
        [("", "汪汪")],
        """from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "汪汪"

print(Dog().speak())
""",
    ),
    (
        "类方法",
        "定义 Book 类，类变量 count 记录创建数量，类方法输出总数。",
        "medium",
        "进阶Day03,类方法,classmethod",
        [("", "2")],
        """class Book:
    count = 0

    def __init__(self, title):
        Book.count += 1

    @classmethod
    def total(cls):
        return cls.count

Book("Python")
Book("AI")
print(Book.total())
""",
    ),
    (
        "静态方法",
        "定义 Math 类静态方法 add，输入两个整数输出和。",
        "medium",
        "进阶Day03,静态方法,staticmethod",
        [
            ("3 4", "7"),
            ("10 20", "30"),
        ],
        """class Math:
    @staticmethod
    def add(a, b):
        return a + b

a, b = map(int, input().split())
print(Math.add(a, b))
""",
    ),
    (
        "浅拷贝",
        "定义列表 a，使用 copy 浅拷贝得到 b，修改 b[0] 后输出 a 和 b。",
        "medium",
        "进阶Day03,浅拷贝,copy",
        [("", "1 2\n9 2")],
        """a = [1, 2]
b = a.copy()
b[0] = 9
print(" ".join(map(str, a)))
print(" ".join(map(str, b)))
""",
    ),
    (
        "深拷贝",
        "定义嵌套列表 a，使用 deepcopy 深拷贝得到 b，修改 b[0][0] 后输出 a 和 b。",
        "hard",
        "进阶Day03,深拷贝,deepcopy",
        [("", "1 2\n9 2")],
        """import copy

a = [[1, 2]]
b = copy.deepcopy(a)
b[0][0] = 9
print(" ".join(map(str, a[0])))
print(" ".join(map(str, b[0])))
""",
    ),
    (
        "闭包计数器",
        "定义闭包计数器，连续调用三次，输出 1、2、3。",
        "medium",
        "进阶Day04,闭包",
        [("", "1\n2\n3")],
        """def make_counter():
    count = 0
    def counter():
        nonlocal count
        count += 1
        return count
    return counter

fn = make_counter()
print(fn())
print(fn())
print(fn())
""",
    ),
    (
        "通用装饰器",
        "定义通用装饰器，给函数返回值加 后缀！，输入字符串输出结果。",
        "medium",
        "进阶Day04,装饰器",
        [
            ("hello", "hello！"),
            ("Python", "Python！"),
        ],
        """def decorate(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs) + "！"
    return wrapper

@decorate
def echo(value):
    return value

value = input().strip()
print(echo(value))
""",
    ),
    (
        "生成器 next",
        "定义生成器，使用 next 取出前两个平方数并输出。",
        "medium",
        "进阶Day07,生成器,next",
        [("", "1\n4")],
        """def squares():
    n = 1
    while True:
        yield n * n
        n += 1

gen = squares()
print(next(gen))
print(next(gen))
""",
    ),
    (
        "property 只读",
        "输入一个姓名，定义私有属性，通过 property 只读访问并输出。",
        "medium",
        "进阶Day07,property",
        [
            ("Tom", "Tom"),
            ("小红", "小红"),
        ],
        """class Student:
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

name = input().strip()
print(Student(name).name)
""",
    ),
    (
        "property setter",
        "使用 property setter 修改私有姓名，输入旧名和新名，输出新名。",
        "medium",
        "进阶Day07,property,setter",
        [
            ("Tom\nJerry", "Jerry"),
        ],
        """class Student:
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

s = Student(input().strip())
s.name = input().strip()
print(s.name)
""",
    ),
    (
        "正则 match",
        "输入一个字符串，使用 re.match 判断是否以 abc 开头，输出 是 或 否。",
        "medium",
        "进阶Day07,正则,match",
        [
            ("abc123", "是"),
            ("xyz", "否"),
        ],
        """import re

s = input().strip()
print("是" if re.match(r"^abc", s) else "否")
""",
    ),
    (
        "正则 search",
        "输入一个字符串，使用 re.search 查找第一个数字并输出。",
        "medium",
        "进阶Day07,正则,search",
        [
            ("hello123", "123"),
            ("a1b2", "1"),
            ("python", "未找到"),
        ],
        """import re

s = input().strip()
match = re.search(r"\\d+", s)
print(match.group() if match else "未找到")
""",
    ),
    (
        "正则 sub",
        "输入一个字符串，使用 re.sub 把所有数字替换为 # 后输出。",
        "medium",
        "进阶Day07,正则,sub",
        [
            ("a1b2", "a#b#"),
            ("hello123", "hello###"),
        ],
        """import re

s = input().strip()
print(re.sub(r"\\d", "#", s))
""",
    ),
    (
        "链表节点",
        "定义 Node 节点类，创建三个节点并串联，输出第二个节点的值。",
        "hard",
        "进阶Day08,链表,节点",
        [("", "2")],
        """class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

n1 = Node(1)
n2 = Node(2)
n3 = Node(3)
n1.next = n2
n2.next = n3
print(n1.next.value)
""",
    ),
    (
        "链表遍历",
        "创建链表 1 -> 2 -> 3，遍历输出每个节点值。",
        "hard",
        "进阶Day08,链表,遍历",
        [("", "1\n2\n3")],
        """class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

n1 = Node(1)
n2 = Node(2)
n3 = Node(3)
n1.next = n2
n2.next = n3

current = n1
while current:
    print(current.value)
    current = current.next
""",
    ),
]


CURRICULUM_EXTRA_PROBLEMS = [_cp(*item) for item in _EXTRA]
CURRICULUM_EXTRA_STARTER_CODES = {
    item["title"]: item["starter_code"]
    for item in CURRICULUM_EXTRA_PROBLEMS
}
