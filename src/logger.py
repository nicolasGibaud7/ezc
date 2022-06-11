class Logger:
    def __init__(self) -> None:
        self.is_log_activated = False

    def set_log_activation(self, is_log_activated: bool):
        self.is_log_activated = is_log_activated

    def debug(self, message: str):
        if self.is_log_activated:
            print(message)

    def warning(self, message: str):
        print(message)

    def error(self, message: str):
        print(message)
