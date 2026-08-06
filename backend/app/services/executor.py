import base64
import os
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Sequence

from .. import config
from ..config import EXECUTION_TIMEOUT, MAX_OUTPUT_LENGTH
from ..models import TestCase
from ..schemas import ExecuteResultOut, TestResultOut
from .executor_registry import EXECUTORS, register_executor


def normalize_output(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.strip().splitlines()).strip()


def _docker_command(code: str) -> list[str]:
    encoded_code = base64.b64encode(code.encode("utf-8")).decode("ascii")
    return [
        "docker",
        "run",
        "--rm",
        "-i",
        "--network",
        "none",
        "--memory",
        "256m",
        "--cpus",
        "1",
        "--pids-limit",
        "64",
        "--cap-drop",
        "ALL",
        "--security-opt",
        "no-new-privileges",
        "-e",
        "PYTHONIOENCODING=utf-8",
        "-e",
        f"CODE_B64={encoded_code}",
        config.PYTHON_RUNNER_IMAGE,
        "python",
        "-I",
        "-c",
        "import base64,os;exec(base64.b64decode(os.environ['CODE_B64']).decode())",
    ]


def run_python_code(code: str, test_cases: Sequence[TestCase], timeout: int = EXECUTION_TIMEOUT) -> ExecuteResultOut:
    if config.EXECUTION_MODE == "docker":
        return run_python_code_docker(code, test_cases, timeout)

    temp_dir = tempfile.mkdtemp(prefix="coding_platform_")
    results: list[TestResultOut] = []
    total_time = 0.0
    status = "accepted"
    error_message = ""

    try:
        script_path = os.path.join(temp_dir, "solution.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(code)

        for index, case in enumerate(test_cases):
            started = time.monotonic()
            passed = False
            actual = ""
            error = ""
            runtime_error = False
            try:
                process = subprocess.run(
                    [sys.executable, "-I", script_path],
                    input=case.input,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    cwd=temp_dir,
                    env={**os.environ, "PYTHONIOENCODING": "utf-8"},
                )
                elapsed = time.monotonic() - started
                total_time += elapsed
                actual = process.stdout[:MAX_OUTPUT_LENGTH]
                if process.returncode != 0:
                    runtime_error = True
                    error = process.stderr.strip()[:MAX_OUTPUT_LENGTH]
                else:
                    passed = normalize_output(actual) == normalize_output(case.expected_output)
                    if not passed:
                        error = "输出与预期结果不一致"
            except subprocess.TimeoutExpired:
                runtime_error = True
                elapsed = time.monotonic() - started
                total_time += elapsed
                error = f"运行超时（超过 {timeout} 秒）"
            except Exception as exc:  # pragma: no cover - defensive
                runtime_error = True
                elapsed = time.monotonic() - started
                total_time += elapsed
                error = str(exc)[:MAX_OUTPUT_LENGTH]

            if runtime_error:
                status = "error"
                error_message = error_message or error
            elif not passed:
                status = "wrong_answer"

            results.append(
                TestResultOut(
                    case_id=getattr(case, "id", None) or index + 1,
                    passed=passed,
                    input=case.input,
                    expected_output=case.expected_output,
                    actual_output=actual[:MAX_OUTPUT_LENGTH],
                    error=error[:MAX_OUTPUT_LENGTH],
                )
            )
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

    return ExecuteResultOut(
        status=status,
        execution_time=round(total_time, 4),
        results=results,
        error_message=error_message[:MAX_OUTPUT_LENGTH],
    )


def run_python_code_docker(code: str, test_cases: Sequence[TestCase], timeout: int = EXECUTION_TIMEOUT) -> ExecuteResultOut:
    temp_dir = tempfile.mkdtemp(prefix="coding_platform_")
    results: list[TestResultOut] = []
    total_time = 0.0
    status = "accepted"
    error_message = ""

    try:
        for index, case in enumerate(test_cases):
            started = time.monotonic()
            passed = False
            actual = ""
            error = ""
            runtime_error = False
            try:
                process = subprocess.run(
                    _docker_command(code),
                    input=case.input,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    cwd=temp_dir,
                    env={**os.environ, "PYTHONIOENCODING": "utf-8"},
                )
                elapsed = time.monotonic() - started
                total_time += elapsed
                actual = process.stdout[:MAX_OUTPUT_LENGTH]
                if process.returncode != 0:
                    runtime_error = True
                    error = process.stderr.strip()[:MAX_OUTPUT_LENGTH]
                else:
                    passed = normalize_output(actual) == normalize_output(case.expected_output)
                    if not passed:
                        error = "输出与预期结果不一致"
            except subprocess.TimeoutExpired:
                runtime_error = True
                elapsed = time.monotonic() - started
                total_time += elapsed
                error = f"运行超时（超过 {timeout} 秒）"
            except Exception as exc:
                runtime_error = True
                elapsed = time.monotonic() - started
                total_time += elapsed
                error = str(exc)[:MAX_OUTPUT_LENGTH]

            if runtime_error:
                status = "error"
                error_message = error_message or error
            elif not passed:
                status = "wrong_answer"

            results.append(
                TestResultOut(
                    case_id=getattr(case, "id", None) or index + 1,
                    passed=passed,
                    input=case.input,
                    expected_output=case.expected_output,
                    actual_output=actual[:MAX_OUTPUT_LENGTH],
                    error=error[:MAX_OUTPUT_LENGTH],
                )
            )
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

    return ExecuteResultOut(
        status=status,
        execution_time=round(total_time, 4),
        results=results,
        error_message=error_message[:MAX_OUTPUT_LENGTH],
    )


def _node_docker_command(code: str) -> list[str]:
    encoded_code = base64.b64encode(code.encode("utf-8")).decode("ascii")
    return [
        "docker",
        "run",
        "--rm",
        "-i",
        "--network",
        "none",
        "--memory",
        "256m",
        "--cpus",
        "1",
        "--pids-limit",
        "64",
        "--cap-drop",
        "ALL",
        "--security-opt",
        "no-new-privileges",
        "-e",
        f"CODE_B64={encoded_code}",
        config.NODE_RUNNER_IMAGE,
        "node",
        "-e",
        "eval(Buffer.from(process.env.CODE_B64,'base64').toString())",
    ]


def _run_test_cases(
    command: list[str],
    test_cases: Sequence[TestCase],
    timeout: int,
    cwd: str,
) -> ExecuteResultOut:
    results: list[TestResultOut] = []
    total_time = 0.0
    status = "accepted"
    error_message = ""

    for index, case in enumerate(test_cases):
        started = time.monotonic()
        passed = False
        actual = ""
        error = ""
        runtime_error = False
        try:
            process = subprocess.run(
                command,
                input=case.input,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd,
                env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            )
            elapsed = time.monotonic() - started
            total_time += elapsed
            actual = process.stdout[:MAX_OUTPUT_LENGTH]
            if process.returncode != 0:
                runtime_error = True
                error = process.stderr.strip()[:MAX_OUTPUT_LENGTH]
            else:
                passed = normalize_output(actual) == normalize_output(case.expected_output)
                if not passed:
                    error = "输出与预期结果不一致"
        except subprocess.TimeoutExpired:
            runtime_error = True
            elapsed = time.monotonic() - started
            total_time += elapsed
            error = f"运行超时（超过 {timeout} 秒）"
        except Exception as exc:  # pragma: no cover - defensive
            runtime_error = True
            elapsed = time.monotonic() - started
            total_time += elapsed
            error = str(exc)[:MAX_OUTPUT_LENGTH]

        if runtime_error:
            status = "error"
            error_message = error_message or error
        elif not passed:
            status = "wrong_answer"

        results.append(
            TestResultOut(
                case_id=getattr(case, "id", None) or index + 1,
                passed=passed,
                input=case.input,
                expected_output=case.expected_output,
                actual_output=actual[:MAX_OUTPUT_LENGTH],
                error=error[:MAX_OUTPUT_LENGTH],
            )
        )

    return ExecuteResultOut(
        status=status,
        execution_time=round(total_time, 4),
        results=results,
        error_message=error_message[:MAX_OUTPUT_LENGTH],
    )


def run_javascript_code(
    code: str,
    test_cases: Sequence[TestCase],
    timeout: int = EXECUTION_TIMEOUT,
) -> ExecuteResultOut:
    if config.EXECUTION_MODE == "docker":
        return run_javascript_code_docker(code, test_cases, timeout)

    temp_dir = tempfile.mkdtemp(prefix="coding_platform_")
    try:
        script_path = os.path.join(temp_dir, "solution.js")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(code)
        return _run_test_cases(["node", script_path], test_cases, timeout, temp_dir)
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def run_javascript_code_docker(
    code: str,
    test_cases: Sequence[TestCase],
    timeout: int = EXECUTION_TIMEOUT,
) -> ExecuteResultOut:
    temp_dir = tempfile.mkdtemp(prefix="coding_platform_")
    try:
        return _run_test_cases(
            _node_docker_command(code),
            test_cases,
            timeout,
            temp_dir,
        )
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def _run_custom_command(
    command: list[str],
    custom_input: str,
    timeout: int,
    cwd: str,
) -> ExecuteResultOut:
    started = time.monotonic()
    try:
        process = subprocess.run(
            command,
            input=custom_input,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        elapsed = time.monotonic() - started
        actual = process.stdout[:MAX_OUTPUT_LENGTH]
        if process.returncode == 0:
            return ExecuteResultOut(
                status="success",
                execution_time=round(elapsed, 4),
                results=[
                    TestResultOut(
                        case_id=0,
                        passed=True,
                        input=custom_input,
                        expected_output="",
                        actual_output=actual,
                    )
                ],
            )
        error = process.stderr.strip()[:MAX_OUTPUT_LENGTH]
        return ExecuteResultOut(
            status="error",
            execution_time=round(elapsed, 4),
            error_message=error,
            results=[
                TestResultOut(
                    case_id=0,
                    passed=False,
                    input=custom_input,
                    expected_output="",
                    actual_output=actual,
                    error=error,
                )
            ],
        )
    except subprocess.TimeoutExpired:
        elapsed = time.monotonic() - started
        error = f"运行超时（超过 {timeout} 秒）"
        return ExecuteResultOut(
            status="error",
            execution_time=round(elapsed, 4),
            error_message=error,
            results=[
                TestResultOut(
                    case_id=0,
                    passed=False,
                    input=custom_input,
                    expected_output="",
                    error=error,
                )
            ],
        )


def run_custom_javascript(
    code: str,
    custom_input: str,
    timeout: int = EXECUTION_TIMEOUT,
) -> ExecuteResultOut:
    if config.EXECUTION_MODE == "docker":
        return run_custom_javascript_docker(code, custom_input, timeout)

    temp_dir = tempfile.mkdtemp(prefix="coding_platform_")
    try:
        script_path = os.path.join(temp_dir, "solution.js")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(code)
        return _run_custom_command(["node", script_path], custom_input, timeout, temp_dir)
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def run_custom_javascript_docker(
    code: str,
    custom_input: str,
    timeout: int = EXECUTION_TIMEOUT,
) -> ExecuteResultOut:
    temp_dir = tempfile.mkdtemp(prefix="coding_platform_")
    try:
        return _run_custom_command(
            _node_docker_command(code),
            custom_input,
            timeout,
            temp_dir,
        )
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def _java_docker_command(code: str) -> list[str]:
    encoded_code = base64.b64encode(code.encode("utf-8")).decode("ascii")
    return [
        "docker",
        "run",
        "--rm",
        "-i",
        "--network",
        "none",
        "--memory",
        "256m",
        "--cpus",
        "1",
        "--pids-limit",
        "64",
        "--cap-drop",
        "ALL",
        "--security-opt",
        "no-new-privileges",
        "-w",
        "/tmp",
        "-e",
        f"CODE_B64={encoded_code}",
        config.JAVA_RUNNER_IMAGE,
        "sh",
        "-c",
        "printf '%s' \"$CODE_B64\" | base64 -d > Main.java "
        "&& javac -encoding UTF-8 Main.java && java Main",
    ]


def _cpp_docker_command(code: str) -> list[str]:
    encoded_code = base64.b64encode(code.encode("utf-8")).decode("ascii")
    return [
        "docker",
        "run",
        "--rm",
        "-i",
        "--network",
        "none",
        "--memory",
        "256m",
        "--cpus",
        "1",
        "--pids-limit",
        "64",
        "--cap-drop",
        "ALL",
        "--security-opt",
        "no-new-privileges",
        "-w",
        "/tmp",
        "-e",
        f"CODE_B64={encoded_code}",
        config.CPP_RUNNER_IMAGE,
        "sh",
        "-c",
        "printf '%s' \"$CODE_B64\" | base64 -d > solution.cpp "
        "&& g++ -std=c++17 -O2 -o solution solution.cpp "
        "&& ./solution",
    ]


def _compile_java_local(temp_dir: str, timeout: int) -> str | None:
    try:
        process = subprocess.run(
            ["javac", "-encoding", "UTF-8", "Main.java"],
            cwd=temp_dir,
            capture_output=True,
            text=True,
            timeout=timeout,
            env={**os.environ, "JAVA_TOOL_OPTIONS": "-Dfile.encoding=UTF-8"},
        )
    except subprocess.TimeoutExpired:
        return f"编译超时（超过 {timeout} 秒）"
    except Exception as exc:  # pragma: no cover - defensive
        return str(exc)[:MAX_OUTPUT_LENGTH]

    if process.returncode != 0:
        return (
            process.stderr.strip()[:MAX_OUTPUT_LENGTH]
            or "Java 编译失败"
        )
    return None


def run_java_code(
    code: str,
    test_cases: Sequence[TestCase],
    timeout: int = EXECUTION_TIMEOUT,
) -> ExecuteResultOut:
    if config.EXECUTION_MODE == "docker":
        return run_java_code_docker(code, test_cases, timeout)

    temp_dir = tempfile.mkdtemp(prefix="coding_platform_")
    try:
        script_path = os.path.join(temp_dir, "Main.java")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(code)
        compile_error = _compile_java_local(temp_dir, timeout)
        if compile_error:
            return ExecuteResultOut(
                status="error",
                error_message=compile_error,
                results=[],
            )
        return _run_test_cases(
            ["java", "-cp", temp_dir, "Main"],
            test_cases,
            timeout,
            temp_dir,
        )
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def run_java_code_docker(
    code: str,
    test_cases: Sequence[TestCase],
    timeout: int = EXECUTION_TIMEOUT,
) -> ExecuteResultOut:
    temp_dir = tempfile.mkdtemp(prefix="coding_platform_")
    try:
        return _run_test_cases(
            _java_docker_command(code),
            test_cases,
            timeout,
            temp_dir,
        )
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def run_custom_java(
    code: str,
    custom_input: str,
    timeout: int = EXECUTION_TIMEOUT,
) -> ExecuteResultOut:
    if config.EXECUTION_MODE == "docker":
        return run_custom_java_docker(code, custom_input, timeout)

    temp_dir = tempfile.mkdtemp(prefix="coding_platform_")
    try:
        script_path = os.path.join(temp_dir, "Main.java")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(code)
        compile_error = _compile_java_local(temp_dir, timeout)
        if compile_error:
            return ExecuteResultOut(
                status="error",
                error_message=compile_error,
                results=[
                    TestResultOut(
                        case_id=0,
                        passed=False,
                        input=custom_input,
                        expected_output="",
                        error=compile_error,
                    )
                ],
            )
        return _run_custom_command(
            ["java", "-cp", temp_dir, "Main"],
            custom_input,
            timeout,
            temp_dir,
        )
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def run_custom_java_docker(
    code: str,
    custom_input: str,
    timeout: int = EXECUTION_TIMEOUT,
) -> ExecuteResultOut:
    temp_dir = tempfile.mkdtemp(prefix="coding_platform_")
    try:
        return _run_custom_command(
            _java_docker_command(code),
            custom_input,
            timeout,
            temp_dir,
        )
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def _cpp_binary_path(temp_dir: str) -> str:
    filename = "solution.exe" if os.name == "nt" else "solution"
    return os.path.join(temp_dir, filename)


def _compile_cpp_local(temp_dir: str, timeout: int) -> str | None:
    binary_path = _cpp_binary_path(temp_dir)
    try:
        process = subprocess.run(
            ["g++", "-std=c++17", "-O2", "-o", binary_path, "solution.cpp"],
            cwd=temp_dir,
            capture_output=True,
            text=True,
            timeout=timeout,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
    except subprocess.TimeoutExpired:
        return f"编译超时（超过 {timeout} 秒）"
    except Exception as exc:  # pragma: no cover - defensive
        return str(exc)[:MAX_OUTPUT_LENGTH]

    if process.returncode != 0:
        return (
            process.stderr.strip()[:MAX_OUTPUT_LENGTH]
            or "C++ 编译失败"
        )
    return None


def run_cpp_code(
    code: str,
    test_cases: Sequence[TestCase],
    timeout: int = EXECUTION_TIMEOUT,
) -> ExecuteResultOut:
    if config.EXECUTION_MODE == "docker":
        return run_cpp_code_docker(code, test_cases, timeout)

    temp_dir = tempfile.mkdtemp(prefix="coding_platform_")
    try:
        script_path = os.path.join(temp_dir, "solution.cpp")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(code)
        compile_error = _compile_cpp_local(temp_dir, timeout)
        if compile_error:
            return ExecuteResultOut(
                status="error",
                error_message=compile_error,
                results=[],
            )
        return _run_test_cases(
            [_cpp_binary_path(temp_dir)],
            test_cases,
            timeout,
            temp_dir,
        )
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def run_cpp_code_docker(
    code: str,
    test_cases: Sequence[TestCase],
    timeout: int = EXECUTION_TIMEOUT,
) -> ExecuteResultOut:
    temp_dir = tempfile.mkdtemp(prefix="coding_platform_")
    try:
        return _run_test_cases(
            _cpp_docker_command(code),
            test_cases,
            timeout,
            temp_dir,
        )
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def run_custom_cpp(
    code: str,
    custom_input: str,
    timeout: int = EXECUTION_TIMEOUT,
) -> ExecuteResultOut:
    if config.EXECUTION_MODE == "docker":
        return run_custom_cpp_docker(code, custom_input, timeout)

    temp_dir = tempfile.mkdtemp(prefix="coding_platform_")
    try:
        script_path = os.path.join(temp_dir, "solution.cpp")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(code)
        compile_error = _compile_cpp_local(temp_dir, timeout)
        if compile_error:
            return ExecuteResultOut(
                status="error",
                error_message=compile_error,
                results=[
                    TestResultOut(
                        case_id=0,
                        passed=False,
                        input=custom_input,
                        expected_output="",
                        error=compile_error,
                    )
                ],
            )
        return _run_custom_command(
            [_cpp_binary_path(temp_dir)],
            custom_input,
            timeout,
            temp_dir,
        )
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def run_custom_cpp_docker(
    code: str,
    custom_input: str,
    timeout: int = EXECUTION_TIMEOUT,
) -> ExecuteResultOut:
    temp_dir = tempfile.mkdtemp(prefix="coding_platform_")
    try:
        return _run_custom_command(
            _cpp_docker_command(code),
            custom_input,
            timeout,
            temp_dir,
        )
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def run_custom_python(code: str, custom_input: str, timeout: int = EXECUTION_TIMEOUT) -> ExecuteResultOut:
    if config.EXECUTION_MODE == "docker":
        return run_custom_python_docker(code, custom_input, timeout)

    temp_dir = tempfile.mkdtemp(prefix="coding_platform_")
    try:
        script_path = os.path.join(temp_dir, "solution.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(code)

        started = time.monotonic()
        try:
            process = subprocess.run(
                [sys.executable, "-I", script_path],
                input=custom_input,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=temp_dir,
                env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            )
            elapsed = time.monotonic() - started
            actual = process.stdout[:MAX_OUTPUT_LENGTH]
            if process.returncode == 0:
                return ExecuteResultOut(
                    status="success",
                    execution_time=round(elapsed, 4),
                    results=[
                        TestResultOut(
                            case_id=0,
                            passed=True,
                            input=custom_input,
                            expected_output="",
                            actual_output=actual,
                        )
                    ],
                )
            error = process.stderr.strip()[:MAX_OUTPUT_LENGTH]
            return ExecuteResultOut(
                status="error",
                execution_time=round(elapsed, 4),
                error_message=error,
                results=[
                    TestResultOut(
                        case_id=0,
                        passed=False,
                        input=custom_input,
                        expected_output="",
                        actual_output=actual,
                        error=error,
                    )
                ],
            )
        except subprocess.TimeoutExpired:
            elapsed = time.monotonic() - started
            error = f"运行超时（超过 {timeout} 秒）"
            return ExecuteResultOut(
                status="error",
                execution_time=round(elapsed, 4),
                error_message=error,
                results=[
                    TestResultOut(
                        case_id=0,
                        passed=False,
                        input=custom_input,
                        expected_output="",
                        error=error,
                    )
                ],
            )
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def run_custom_python_docker(code: str, custom_input: str, timeout: int = EXECUTION_TIMEOUT) -> ExecuteResultOut:
    temp_dir = tempfile.mkdtemp(prefix="coding_platform_")
    try:
        started = time.monotonic()
        try:
            process = subprocess.run(
                _docker_command(code),
                input=custom_input,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=temp_dir,
                env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            )
            elapsed = time.monotonic() - started
            actual = process.stdout[:MAX_OUTPUT_LENGTH]
            if process.returncode == 0:
                return ExecuteResultOut(
                    status="success",
                    execution_time=round(elapsed, 4),
                    results=[
                        TestResultOut(
                            case_id=0,
                            passed=True,
                            input=custom_input,
                            expected_output="",
                            actual_output=actual,
                        )
                    ],
                )
            error = process.stderr.strip()[:MAX_OUTPUT_LENGTH]
            return ExecuteResultOut(
                status="error",
                execution_time=round(elapsed, 4),
                error_message=error,
                results=[
                    TestResultOut(
                        case_id=0,
                        passed=False,
                        input=custom_input,
                        expected_output="",
                        actual_output=actual,
                        error=error,
                    )
                ],
            )
        except subprocess.TimeoutExpired:
            elapsed = time.monotonic() - started
            error = f"运行超时（超过 {timeout} 秒）"
            return ExecuteResultOut(
                status="error",
                execution_time=round(elapsed, 4),
                error_message=error,
                results=[
                    TestResultOut(
                        case_id=0,
                        passed=False,
                        input=custom_input,
                        expected_output="",
                        error=error,
                    )
                ],
            )
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def execute_code(
    code: str,
    language: str,
    test_cases: Sequence[TestCase],
) -> ExecuteResultOut:
    executor = EXECUTORS.get(language)
    if executor is None:
        return ExecuteResultOut(
            status="error",
            error_message=f"暂不支持语言：{language}",
        )
    return executor(code, test_cases)


def execute_custom(
    code: str,
    language: str,
    custom_input: str,
) -> ExecuteResultOut:
    if language == "python":
        return run_custom_python(code, custom_input)
    if language == "javascript":
        return run_custom_javascript(code, custom_input)
    if language == "java":
        return run_custom_java(code, custom_input)
    if language == "cpp":
        return run_custom_cpp(code, custom_input)
    return ExecuteResultOut(
        status="error",
        error_message=f"暂不支持语言：{language}",
    )


@register_executor("python")
def _python_executor(code: str, test_cases: Sequence[TestCase]) -> ExecuteResultOut:
    return run_python_code(code, test_cases)


@register_executor("javascript")
def _javascript_executor(code: str, test_cases: Sequence[TestCase]) -> ExecuteResultOut:
    return run_javascript_code(code, test_cases)


@register_executor("java")
def _java_executor(code: str, test_cases: Sequence[TestCase]) -> ExecuteResultOut:
    return run_java_code(code, test_cases)


@register_executor("cpp")
def _cpp_executor(code: str, test_cases: Sequence[TestCase]) -> ExecuteResultOut:
    return run_cpp_code(code, test_cases)
