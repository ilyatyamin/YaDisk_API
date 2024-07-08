class IncorrectDataError(Exception):
    def __init__(self, additional_info=None, error_name=None):
        self.additional = additional_info
        self.err_name = error_name

    def __str__(self):
        if self.additional is None and self.err_name is None:
            return "Your data is incorrect."
        elif self.additional is not None and self.err_name is None:
            return f"Your data is incorrect.\n{self.additional}"
        elif self.additional is not None and self.err_name is not None:
            return f"[{self.err_name}]. Your data is incorrect.\n{self.additional}"


class InvalidTokenError(Exception):
    def __init__(self, additional_info=None):
        self.additional = additional_info

    def __str__(self):
        if self.additional is None:
            return "Your token for Yandex API is invalid."
        else:
            return f"Your token for Yandex API is invalid.\n{self.additional}"


class ServerError(Exception):
    def __init__(self, additional_info=None):
        self.additional = additional_info

    def __str__(self):
        if self.additional is None:
            return "Error has occurred. "
        else:
            return f"Error has occurred.\n{self.additional}"
