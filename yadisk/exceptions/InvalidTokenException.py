class InvalidTokenException(Exception):
    def __init__(self, additional_info = None):
        self.additional = additional_info

    def __str__(self):
        if self.additional is None:
            return "Your token for Yandex API is invalid."
        else:
            return f"Your token for Yandex API is invalid.\n{self.additional}"