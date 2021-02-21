from custom_exception import WrongInputData, HaveNoSeporator


class CheckAnything:
    def __init__(self):
        pass

    def check_is_string(self, string: str) -> str:
        if isinstance(string, str):
            return string
        raise WrongInputData

    def check_have_sep(self, string: str, seporator: str) -> bool:
        if seporator in string:
            return True
        raise HaveNoSeporator
