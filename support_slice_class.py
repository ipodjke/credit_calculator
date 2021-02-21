from support_check_class import CheckAnything
from custom_exception import HaveNoSeporator, CannotSliceList


class Slicer:
    checker = CheckAnything()

    def __init__(self, text: str) -> None:
        self.text = text
        self.operation_history = {
            'slice_text': None,
            'slice_list': None,
        }

    def slice_text(self, seporator: str) -> list:
        try:
            type(self).checker.check_have_sep(self.text, seporator)
            self.operation_history['slice_text'] = self.text.strip().split(seporator)
            return self.operation_history['slice_text']
        except HaveNoSeporator:
            pass

    def slice_list(self, seporator: str) -> list:
        if self.operation_history['slice_text'] is not None:
            self.operation_history['slice_list'] = [text_part.split(seporator) for text_part in self.operation_history['slice_text']]
            return self.operation_history['slice_list']
        raise CannotSliceList
