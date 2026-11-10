import sys

class Logger:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

    @classmethod
    def info(cls, message: str):
        print(f"{cls.CYAN}[EMOCHI INFO]{cls.ENDC} {message}")

    @classmethod
    def success(cls, message: str):
        print(f"{cls.GREEN}[EMOCHI OK]{cls.ENDC} {message}")

    @classmethod
    def warning(cls, message: str):
        print(f"{cls.WARNING}[EMOCHI WARN]{cls.ENDC} {message}")

    @classmethod
    def error(cls, message: str):
        print(f"{cls.FAIL}[EMOCHI ERROR]{cls.ENDC} {message}")

    @classmethod
    def debug(cls, message: str):
        # Có thể kích hoạt khi cần kiểm tra sâu
        pass
