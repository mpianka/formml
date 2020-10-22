from formml.forms.fields.base import Field
from formml.forms.validators.base import Validator
from formml.forms.widgets.input import InputWidget


class StringField(Field):
    _widget = InputWidget
    _allowed_validators = {
        'regex': Validator,
        'length': Validator,
        'required': Validator
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.placeholder = kwargs.get('@placeholder')

