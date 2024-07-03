class ServerError(Exception):
    def __init__(self, additional_info = None):
        self.additional = additional_info

    def __str__(self):
        if self.additional is None:
            return "Error has occurred. "
        else:
            return f"Error has occurred.\n{self.additional}"