JAVA_PROBLEMS = [
    {
        "title": "Java 两数之和",
        "description": (
            "输入一行两个整数 a 和 b，用空格分隔，输出它们的和。\n\n"
            "示例输入：\n3 4\n\n示例输出：\n7"
        ),
        "language": "java",
        "difficulty": "easy",
        "tags": "Java,入门,运算",
        "starter_code": (
            "import java.util.Scanner;\n"
            "\n"
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        int a = sc.nextInt();\n"
            "        int b = sc.nextInt();\n"
            "        System.out.println(a + b);\n"
            "    }\n"
            "}\n"
        ),
        "test_cases": [
            {"input": "3 4", "expected_output": "7"},
            {"input": "10 -2", "expected_output": "8"},
            {"input": "0 0", "expected_output": "0"},
        ],
    },
    {
        "title": "Java 判断奇偶",
        "description": "输入一个整数 n，如果是奇数输出 odd，偶数输出 even。",
        "language": "java",
        "difficulty": "easy",
        "tags": "Java,条件判断,取余",
        "starter_code": (
            "import java.util.Scanner;\n"
            "\n"
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        int n = sc.nextInt();\n"
            "        System.out.println(n % 2 == 0 ? \"even\" : \"odd\");\n"
            "    }\n"
            "}\n"
        ),
        "test_cases": [
            {"input": "3", "expected_output": "odd"},
            {"input": "4", "expected_output": "even"},
            {"input": "0", "expected_output": "even"},
        ],
    },
    {
        "title": "Java 字符串反转",
        "description": "输入一个字符串，输出它的反转结果。",
        "language": "java",
        "difficulty": "easy",
        "tags": "Java,字符串,StringBuilder",
        "starter_code": (
            "import java.util.Scanner;\n"
            "\n"
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        String input = sc.nextLine();\n"
            "        System.out.println(new StringBuilder(input).reverse());\n"
            "    }\n"
            "}\n"
        ),
        "test_cases": [
            {"input": "abc", "expected_output": "cba"},
            {"input": "hello", "expected_output": "olleh"},
            {"input": "Java", "expected_output": "avaJ"},
        ],
    },
    {
        "title": "Java 数组求和",
        "description": "输入一行整数，用空格分隔，输出这些整数的和。",
        "language": "java",
        "difficulty": "easy",
        "tags": "Java,数组,循环",
        "starter_code": (
            "import java.util.Scanner;\n"
            "\n"
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner sc = new Scanner(System.in);\n"
            "        int sum = 0;\n"
            "        while (sc.hasNextInt()) {\n"
            "            sum += sc.nextInt();\n"
            "        }\n"
            "        System.out.println(sum);\n"
            "    }\n"
            "}\n"
        ),
        "test_cases": [
            {"input": "1 2 3 4", "expected_output": "10"},
            {"input": "10 -2 8", "expected_output": "16"},
            {"input": "0", "expected_output": "0"},
        ],
    },
    {
        "title": "Java 欢迎输出",
        "description": "不读取输入，直接输出 Hello Java。",
        "language": "java",
        "difficulty": "easy",
        "tags": "Java,入门,输出",
        "starter_code": (
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        System.out.println(\"Hello Java\");\n"
            "    }\n"
            "}\n"
        ),
        "test_cases": [
            {"input": "", "expected_output": "Hello Java"},
        ],
    },
]
