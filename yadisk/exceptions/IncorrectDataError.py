class IncorrectDataError(Exception):
    def __init__(self, additional_info = None, error_name = None):
        self.additional = additional_info
        self.err_name = error_name

    def __str__(self):
        if self.additional is None and self.err_name is None:
            return "Your data is incorrect."
        elif self.additional is not None and self.err_name is None:
            return f"Your data is incorrect.\n{self.additional}"
        elif self.additional is not None and self.err_name is not None:
            return f"[{self.err_name}]. Your data is incorrect.\n{self.additional}"