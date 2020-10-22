from formml.exceptions import InvalidFormFileError, FormException
from formml.forms.validators.base import Validator
from formml.forms.widgets.base import Widget


class Field:
    _widget: Widget = None
    _field_required_args: tuple = ('id', 'type',)
    _allowed_validators: dict = dict()

    def __init__(self, **kwargs):
        self.id = kwargs.get('@id')
        self.type = kwargs.get('@type')
        self.label = kwargs.get('@label')
        self.tooltip = kwargs.get('@tooltip')
        self.validators = [self._validator_parser(i) for i in kwargs.get('Validator')]

        self.custom_class = (kwargs.get('@custom_class') or "").split(" ") or []
        self.custom_id = kwargs.get('@custom_id')

        self.errors: list = []

    def validate_declaration(self) -> None:
        """ Validates a field declaration while parsing xml.
        Will raise an exception when fails."""
        field = self.__dict__

        for attr in self._field_required_args:
            if not field.get(attr):
                raise InvalidFormFileError(f'Field should have required attribute: {attr}')

        for validator in self.validators:
            validator.validate_declaration()

    def _validator_parser(self, validator) -> Validator:
        """ Maps field to a correct field class, based on @type attribute"""
        validator_type = validator.get('@type')
        if validator_type not in self._allowed_validators.keys():
            raise FormException(
                f'Found validator of type {validator_type}, which is not allowed for field of type {self.type}.')

        return self._allowed_validators[validator_type](**validator)

    @property
    def template(self) -> dict:
        return self._widget(self).template
