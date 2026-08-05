PYTHON_PROBLEMS = [
    {
        "title": "两数之和",
        "description": (
            "输入一行两个整数 a 和 b，用空格分隔，输出它们的和。\n\n"
            "示例输入：\n3 4\n\n示例输出：\n7"
        ),
        "difficulty": "easy",
        "tags": "入门,变量,运算",
        "test_cases": [
            {"input": "3 4", "expected_output": "7"},
            {"input": "10 -2", "expected_output": "8"},
            {"input": "0 0", "expected_output": "0"},
        ],
    },
    {
        "title": "斐波那契数列",
        "description": (
            "输入一个正整数 n，输出第 n 项斐波那契数。\n"
            "约定：f(1)=1，f(2)=1，f(n)=f(n-1)+f(n-2)。"
        ),
        "difficulty": "medium",
        "tags": "循环,递推,函数",
        "test_cases": [
            {"input": "1", "expected_output": "1"},
            {"input": "5", "expected_output": "5"},
            {"input": "10", "expected_output": "55"},
        ],
    },
    {
        "title": "三个数之和",
        "description": "输入三个整数，用空格分隔，输出它们的和。",
        "difficulty": "easy",
        "tags": "入门,变量,运算",
        "test_cases": [
            {"input": "1 2 3", "expected_output": "6"},
            {"input": "10 20 30", "expected_output": "60"},
            {"input": "-1 -2 -3", "expected_output": "-6"},
        ],
    },
    {
        "title": "判断奇偶",
        "description": "输入一个整数 n，如果是奇数输出 odd，偶数输出 even。",
        "difficulty": "easy",
        "tags": "条件判断,取余",
        "test_cases": [
            {"input": "3", "expected_output": "odd"},
            {"input": "4", "expected_output": "even"},
            {"input": "0", "expected_output": "even"},
        ],
    },
    {
        "title": "三个数最大值",
        "description": "输入三个整数，用空格分隔，输出其中最大的数。",
        "difficulty": "easy",
        "tags": "条件判断,比较",
        "test_cases": [
            {"input": "1 5 3", "expected_output": "5"},
            {"input": "9 2 8", "expected_output": "9"},
            {"input": "-1 -5 -3", "expected_output": "-1"},
        ],
    },
    {
        "title": "字符串反转",
        "description": "输入一个字符串，输出它的反转结果。",
        "difficulty": "easy",
        "tags": "字符串,切片",
        "test_cases": [
            {"input": "abc", "expected_output": "cba"},
            {"input": "hello", "expected_output": "olleh"},
            {"input": "Python", "expected_output": "nohtyP"},
        ],
    },
    {
        "title": "列表求和",
        "description": "输入一行整数，用空格分隔，输出这些整数的和。",
        "difficulty": "easy",
        "tags": "列表,循环,sum",
        "test_cases": [
            {"input": "1 2 3 4", "expected_output": "10"},
            {"input": "10 -2 8", "expected_output": "16"},
            {"input": "0", "expected_output": "0"},
        ],
    },
    {
        "title": "判断回文",
        "description": "输入一个字符串，如果是回文输出 yes，否则输出 no。",
        "difficulty": "easy",
        "tags": "字符串,切片,条件判断",
        "test_cases": [
            {"input": "abcba", "expected_output": "yes"},
            {"input": "hello", "expected_output": "no"},
            {"input": "a", "expected_output": "yes"},
        ],
    },
    {
        "title": "统计元音",
        "description": "输入一个小写字符串，统计其中 a、e、i、o、u 的总数并输出。",
        "difficulty": "easy",
        "tags": "字符串,循环,计数",
        "test_cases": [
            {"input": "hello", "expected_output": "2"},
            {"input": "python", "expected_output": "1"},
            {"input": "aeiou", "expected_output": "5"},
        ],
    },
    {
        "title": "列表去重",
        "description": (
            "输入一行整数，用空格分隔，按出现顺序去重后输出，数字之间用空格分隔。"
        ),
        "difficulty": "medium",
        "tags": "列表,集合,去重",
        "test_cases": [
            {"input": "1 2 2 3 1", "expected_output": "1 2 3"},
            {"input": "5 5 5", "expected_output": "5"},
            {"input": "1 2 3", "expected_output": "1 2 3"},
        ],
    },
    {
        "title": "计算阶乘",
        "description": "输入一个非负整数 n，输出 n!。约定 0!=1。",
        "difficulty": "easy",
        "tags": "循环,函数,递归基础",
        "test_cases": [
            {"input": "0", "expected_output": "1"},
            {"input": "5", "expected_output": "120"},
            {"input": "10", "expected_output": "3628800"},
        ],
    },
    {
        "title": "判断素数",
        "description": "输入一个正整数 n，如果是素数输出 prime，否则输出 not prime。",
        "difficulty": "medium",
        "tags": "循环,数学,条件判断",
        "test_cases": [
            {"input": "2", "expected_output": "prime"},
            {"input": "7", "expected_output": "prime"},
            {"input": "9", "expected_output": "not prime"},
            {"input": "1", "expected_output": "not prime"},
        ],
    },
    {
        "title": "大小写转换",
        "description": "输入一个字符串，把大写字母转小写，小写字母转大写后输出。",
        "difficulty": "easy",
        "tags": "字符串,swapcase",
        "test_cases": [
            {"input": "Hello", "expected_output": "hELLO"},
            {"input": "AbC", "expected_output": "aBc"},
            {"input": "Python", "expected_output": "pYTHON"},
        ],
    },
    {
        "title": "单词词频统计",
        "description": (
            "输入一行英文单词，用空格分隔。按首次出现顺序输出每个单词和次数，"
            "格式为 word:count，每个结果一行。"
        ),
        "difficulty": "medium",
        "tags": "字典,字符串,循环",
        "test_cases": [
            {"input": "apple banana apple", "expected_output": "apple:2\nbanana:1"},
            {"input": "a b c", "expected_output": "a:1\nb:1\nc:1"},
            {"input": "hello hello hello", "expected_output": "hello:3"},
        ],
    },
    {
        "title": "冒泡排序",
        "description": "输入一行整数，用空格分隔，使用冒泡排序升序输出，数字之间用空格分隔。",
        "difficulty": "medium",
        "tags": "排序,列表,循环",
        "test_cases": [
            {"input": "3 1 2", "expected_output": "1 2 3"},
            {"input": "5 4 3 2 1", "expected_output": "1 2 3 4 5"},
            {"input": "1 1 2", "expected_output": "1 1 2"},
        ],
    },
    {
        "title": "二分查找",
        "description": (
            "第一行输入升序整数数组，第二行输入目标值。"
            "输出目标值在数组中的下标，从 0 开始；不存在输出 -1。"
        ),
        "difficulty": "medium",
        "tags": "二分查找,列表,函数",
        "test_cases": [
            {"input": "1 2 3 4 5\n3", "expected_output": "2"},
            {"input": "1 2 3 4 5\n6", "expected_output": "-1"},
            {"input": "1 2 3\n2", "expected_output": "1"},
        ],
    },
    {
        "title": "递归求和",
        "description": "输入一个正整数 n，用递归计算 1+2+...+n 并输出。",
        "difficulty": "easy",
        "tags": "递归,函数",
        "test_cases": [
            {"input": "5", "expected_output": "15"},
            {"input": "10", "expected_output": "55"},
            {"input": "1", "expected_output": "1"},
        ],
    },
    {
        "title": "平方生成器",
        "description": (
            "输入一个正整数 n，用生成器依次生成 1 到 n 的平方，"
            "输出时用空格分隔。"
        ),
        "difficulty": "medium",
        "tags": "生成器,yield,高级语法",
        "test_cases": [
            {"input": "3", "expected_output": "1 4 9"},
            {"input": "5", "expected_output": "1 4 9 16 25"},
            {"input": "1", "expected_output": "1"},
        ],
    },
    {
        "title": "筛选偶数",
        "description": "输入一行整数，用空格分隔，只输出偶数，数字之间用空格分隔。",
        "difficulty": "medium",
        "tags": "filter,lambda,列表,高级语法",
        "test_cases": [
            {"input": "1 2 3 4 5 6", "expected_output": "2 4 6"},
            {"input": "1 3 5", "expected_output": ""},
            {"input": "2 4 6", "expected_output": "2 4 6"},
        ],
    },
    {
        "title": "乘方装饰器",
        "description": (
            "实现一个装饰器 doubler，使被装饰函数返回的结果乘以 2。"
            "输入一个整数 n，输出 fn(n) 的结果，其中 fn(n)=n*2。"
        ),
        "difficulty": "medium",
        "tags": "装饰器,闭包,高级语法",
        "test_cases": [
            {"input": "4", "expected_output": "8"},
            {"input": "7", "expected_output": "14"},
            {"input": "0", "expected_output": "0"},
        ],
    },
    {
        "title": "矩形面积类",
        "description": (
            "定义一个 Rectangle 类，构造参数为 width 和 height，"
            "提供 area 方法返回面积。输入宽和高，输出面积。"
        ),
        "difficulty": "medium",
        "tags": "类,面向对象,方法",
        "test_cases": [
            {"input": "3 4", "expected_output": "12"},
            {"input": "5 6", "expected_output": "30"},
            {"input": "10 2", "expected_output": "20"},
        ],
    },
    {
        "title": "安全除法",
        "description": "输入两个整数 a 和 b，输出 a 除以 b 的整数结果；如果 b 为 0，输出 error。",
        "difficulty": "medium",
        "tags": "异常处理,try,except",
        "test_cases": [
            {"input": "8 2", "expected_output": "4"},
            {"input": "5 0", "expected_output": "error"},
            {"input": "9 3", "expected_output": "3"},
        ],
    },
    {
        "title": "字符串排序",
        "description": "输入一行英文单词，用空格分隔，按字母升序排序后每行输出一个单词。",
        "difficulty": "medium",
        "tags": "排序,字符串,sorted",
        "test_cases": [
            {"input": "banana apple cherry", "expected_output": "apple\nbanana\ncherry"},
            {"input": "z a m", "expected_output": "a\nm\nz"},
            {"input": "b b a", "expected_output": "a\nb\nb"},
        ],
    },
    {
        "title": "立方列表推导式",
        "description": "输入一个正整数 n，用列表推导式生成 1 到 n 的立方，输出时用空格分隔。",
        "difficulty": "medium",
        "tags": "列表推导式,高级语法",
        "test_cases": [
            {"input": "3", "expected_output": "1 8 27"},
            {"input": "4", "expected_output": "1 8 27 64"},
            {"input": "1", "expected_output": "1"},
        ],
    },
]


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


EXTRA_PYTHON_PROBLEMS = [
    _p(
        "输出 Hello World",
        "编写程序，不读取输入，直接输出 Hello World。",
        "easy",
        "入门,print",
        [("", "Hello World")],
    ),
    _p(
        "整数除法与余数",
        "输入两个整数 a 和 b，输出 a 整除 b 的商和余数，用空格分隔。",
        "easy",
        "运算,整除,取余",
        [
            ("7 2", "3 1"),
            ("10 3", "3 1"),
            ("8 4", "2 0"),
        ],
    ),
    _p(
        "字符串长度",
        "输入一个字符串，输出它的长度。",
        "easy",
        "字符串,len",
        [
            ("abc", "3"),
            ("hello", "5"),
            ("Python", "6"),
        ],
    ),
    _p(
        "字符串拼接",
        "第一行输入字符串 a，第二行输入字符串 b，输出 a 和 b 直接拼接的结果。",
        "easy",
        "字符串,拼接",
        [
            ("Hello\nWorld", "HelloWorld"),
            ("foo\nbar", "foobar"),
            ("Python\n3", "Python3"),
        ],
    ),
    _p(
        "字符串替换",
        "输入一个字符串，把其中所有 hello 替换成 hi 后输出。",
        "easy",
        "字符串,replace",
        [
            ("hello world hello", "hi world hi"),
            ("aaa", "aaa"),
            ("hellohello", "hihi"),
        ],
    ),
    _p(
        "字符串转整数",
        "输入一个整数字符串，把它转成整数后加 1 输出。",
        "easy",
        "类型转换,int",
        [
            ("123", "124"),
            ("45", "46"),
            ("-7", "-6"),
        ],
    ),
    _p(
        "f-string 格式化",
        "输入姓名和年龄，用空格分隔，输出 姓名 is 年龄 years old。",
        "easy",
        "f-string,格式化",
        [
            ("Tom 18", "Tom is 18 years old"),
            ("Lily 20", "Lily is 20 years old"),
            ("Bob 7", "Bob is 7 years old"),
        ],
    ),
    _p(
        "列表索引",
        "第一行输入整数列表，第二行输入下标 index，输出列表中该下标位置的元素。",
        "easy",
        "列表,索引",
        [
            ("10 20 30 40\n2", "30"),
            ("5 6 7\n0", "5"),
            ("1 2 3\n-1", "3"),
        ],
    ),
    _p(
        "列表尾部添加",
        "第一行输入整数列表，第二行输入一个整数，把它添加到列表末尾后输出完整列表。",
        "easy",
        "列表,append",
        [
            ("1 2 3\n4", "1 2 3 4"),
            ("5 6\n7", "5 6 7"),
            ("1\n2", "1 2"),
        ],
    ),
    _p(
        "列表反转",
        "输入一行整数，用空格分隔，反转列表顺序后输出。",
        "easy",
        "列表,reverse,切片",
        [
            ("1 2 3 4", "4 3 2 1"),
            ("5 5 6", "6 5 5"),
            ("1", "1"),
        ],
    ),
    _p(
        "元素出现次数",
        "第一行输入列表元素，第二行输入一个目标值，输出目标值在列表中出现的次数。",
        "easy",
        "列表,count",
        [
            ("1 2 2 3 2\n2", "3"),
            ("a b a\nx", "0"),
            ("x y x x\nx", "3"),
        ],
    ),
    _p(
        "元组解包",
        "输入两个值，用空格分隔，使用元组解包赋值给 a 和 b，输出 a=值 b=值。",
        "easy",
        "元组,解包",
        [
            ("3 5", "a=3 b=5"),
            ("x y", "a=x b=y"),
            ("10 20", "a=10 b=20"),
        ],
    ),
    _p(
        "集合交集",
        "两行输入两组整数，输出两组的交集，按升序排列，数字之间用空格分隔。",
        "medium",
        "集合,交集",
        [
            ("1 2 3\n2 3 4", "2 3"),
            ("1 2\n3 4", ""),
            ("5 5 6\n6 6", "6"),
        ],
    ),
    _p(
        "集合并集",
        "两行输入两组整数，输出两组的并集，按升序排列，数字之间用空格分隔。",
        "medium",
        "集合,并集",
        [
            ("1 2 3\n2 3 4", "1 2 3 4"),
            ("1 2\n3 4", "1 2 3 4"),
            ("1 1\n1", "1"),
        ],
    ),
    _p(
        "while 循环求和",
        "输入一个非负整数 n，使用 while 循环计算 0 到 n 的和并输出。",
        "easy",
        "while,循环",
        [
            ("5", "15"),
            ("10", "55"),
            ("0", "0"),
        ],
    ),
    _p(
        "第一个偶数",
        "输入一行整数，用空格分隔，输出第一个偶数；如果不存在输出 -1。",
        "medium",
        "break,循环,列表",
        [
            ("1 3 5 6 7", "6"),
            ("1 3 5", "-1"),
            ("2 4", "2"),
        ],
    ),
    _p(
        "enumerate 下标",
        "输入一行字符串，用空格分隔，使用 enumerate 输出 下标:元素，每行一个。",
        "medium",
        "enumerate,循环",
        [
            ("a b c", "0:a\n1:b\n2:c"),
            ("x", "0:x"),
            ("m n", "0:m\n1:n"),
        ],
    ),
    _p(
        "zip 合并",
        "第一行输入一组字符串，第二行输入一组字符串，使用 zip 合并输出 a-b，每行一个。",
        "medium",
        "zip,循环",
        [
            ("a b c\n1 2 3", "a-1\nb-2\nc-3"),
            ("x y\n9 8", "x-9\ny-8"),
            ("p\nq", "p-q"),
        ],
    ),
    _p(
        "条件表达式",
        "输入一个整数，使用条件表达式输出 positive 或 non-positive。",
        "easy",
        "条件表达式,三元运算",
        [
            ("5", "positive"),
            ("-2", "non-positive"),
            ("0", "non-positive"),
        ],
    ),
    _p(
        "函数默认参数",
        "输入一个或两个整数，调用 def multiply(a, b=2)，输出两数乘积。",
        "medium",
        "函数,默认参数",
        [
            ("5", "10"),
            ("3 4", "12"),
            ("7 1", "7"),
        ],
    ),
    _p(
        "*args 求和",
        "输入一行整数，使用接收 *args 的函数求所有参数的和并输出。",
        "medium",
        "函数,*args,高级语法",
        [
            ("1 2 3", "6"),
            ("10 20", "30"),
            ("7", "7"),
        ],
    ),
    _p(
        "lambda 长度排序",
        "输入一行英文单词，用 lambda 按长度升序排序后输出，数字之间用空格分隔。",
        "medium",
        "lambda,sorted,高级语法",
        [
            ("aaa b cc", "b cc aaa"),
            ("a bb ccc", "a bb ccc"),
            ("dddd a", "a dddd"),
        ],
    ),
    _p(
        "map 平方",
        "输入一行整数，使用 map 求每个数的平方，输出时用空格分隔。",
        "medium",
        "map,高级语法",
        [
            ("1 2 3", "1 4 9"),
            ("2 4", "4 16"),
            ("0", "0"),
        ],
    ),
    _p(
        "filter 长度筛选",
        "输入一行英文单词，使用 filter 只保留长度大于 2 的单词，输出时用空格分隔。",
        "medium",
        "filter,高级语法",
        [
            ("a bb ccc dddd", "ccc dddd"),
            ("a bb", ""),
            ("hello hi", "hello"),
        ],
    ),
    _p(
        "二进制转换",
        "输入一个非负整数，输出它的二进制表示，不包含 0b 前缀。",
        "easy",
        "bin,进制转换",
        [
            ("5", "101"),
            ("10", "1010"),
            ("0", "0"),
        ],
    ),
    _p(
        "十六进制转换",
        "输入一个非负整数，输出它的十六进制表示，不包含 0x 前缀，字母使用小写。",
        "easy",
        "hex,进制转换",
        [
            ("255", "ff"),
            ("16", "10"),
            ("0", "0"),
        ],
    ),
    _p(
        "最大公约数",
        "输入两个正整数，用空格分隔，输出它们的最大公约数。",
        "medium",
        "math,数学,循环",
        [
            ("12 18", "6"),
            ("7 13", "1"),
            ("20 10", "10"),
        ],
    ),
    _p(
        "最小公倍数",
        "输入两个正整数，用空格分隔，输出它们的最小公倍数。",
        "medium",
        "math,数学,循环",
        [
            ("4 6", "12"),
            ("3 5", "15"),
            ("6 8", "24"),
        ],
    ),
    _p(
        "水仙花数",
        "输入一个正整数，判断是否为水仙花数，是则输出 yes，否则输出 no。",
        "medium",
        "循环,数学,幂运算",
        [
            ("153", "yes"),
            ("9474", "yes"),
            ("123", "no"),
        ],
    ),
    _p(
        "完数",
        "输入一个正整数，判断它是否等于除自身外所有正因数之和，是则输出 yes，否则输出 no。",
        "medium",
        "循环,数学,因数",
        [
            ("6", "yes"),
            ("28", "yes"),
            ("12", "no"),
        ],
    ),
    _p(
        "反转数字",
        "输入一个整数，输出它的数字反转结果，保留正负号，去掉前导零。",
        "medium",
        "整数,字符串,反转",
        [
            ("123", "321"),
            ("-123", "-321"),
            ("100", "1"),
        ],
    ),
    _p(
        "首字母大写",
        "输入一行英文，把每个单词首字母大写后输出。",
        "easy",
        "字符串,title",
        [
            ("hello world", "Hello World"),
            ("python is fun", "Python Is Fun"),
            ("a", "A"),
        ],
    ),
    _p(
        "最长单词",
        "输入一行英文单词，输出长度最长的单词；长度相同输出先出现的。",
        "easy",
        "字符串,max,key",
        [
            ("I love Python", "Python"),
            ("a bb ccc", "ccc"),
            ("hello world", "hello"),
        ],
    ),
    _p(
        "装饰器转大写",
        "实现装饰器 uppercase，让被装饰函数返回的字符串转为大写。输入一个字符串，输出大写结果。",
        "medium",
        "装饰器,高级语法",
        [
            ("hello", "HELLO"),
            ("python", "PYTHON"),
            ("abc def", "ABC DEF"),
        ],
    ),
    _p(
        "类继承",
        "定义 Animal 基类和 Dog/Cat 子类。输入 dog 输出 bark，输入 cat 输出 meow。",
        "medium",
        "类,继承,面向对象",
        [
            ("dog", "bark"),
            ("cat", "meow"),
            ("dog", "bark"),
        ],
    ),
    _p(
        "自定义异常",
        "输入一个整数。如果为负数，抛出自定义异常并输出 error；否则输出原数。",
        "medium",
        "异常,raise,面向对象",
        [
            ("-5", "error"),
            ("5", "5"),
            ("0", "0"),
        ],
    ),
]


PYTHON_PROBLEMS.extend(EXTRA_PYTHON_PROBLEMS)
