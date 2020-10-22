class FormException(Exception):
    def __init__(self, *args: object, **kwargs) -> None:
        self.filename = kwargs.get('filename')
        super().__init__(*args, **kwargs)


class InvalidFormFileError(FormException):
    pass


class DuplicateFormError(FormException):
    pass
