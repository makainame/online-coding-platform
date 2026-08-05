EXECUTORS: dict[str, callable] = {}


def register_executor(language: str):
    def decorator(fn):
        EXECUTORS[language] = fn
        return fn
    return decorator


def get_executor(language: str):
    return EXECUTORS.get(language)
