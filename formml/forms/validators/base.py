from formml.exceptions import FormException


class Validator:
    _validator_required_args = ('type', 'message')

    def __init__(self, **kwargs):
        self.type = kwargs.get('@type')
        self.message = kwargs.get('@message')
        self.is_warning = kwargs.get('@is_warning') or False
        self.additional_input_attrs = None

    def validate_declaration(self) -> None:
        """ Validates a field declaration while parsing xml.
        Will raise an exception when fails."""
        validator = self.__dict__

        for attr in self._validator_required_args:
            if not validator.get(attr):
                raise FormException(f'Validator should have required attribute: {attr}')
