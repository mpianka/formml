import xmltodict

from formml.exceptions import InvalidFormFileError, FormException
from formml.forms.fields import ALLOWED_FIELDS
from formml.forms.fields.base import Field


class Form:
    _form_required_args = ('id', 'version',)

    def __init__(self, filename, **kwargs):
        self.filename = filename

        self.id = kwargs.get('@id')
        self.version = kwargs.get('@version')
        self.fields = [self._field_parser(i) for i in kwargs.get('Field')]

    def __repr__(self):
        return f"<Form {self.id} ({self.version})>"

    @property
    def _exc_header(self):
        return f"[{self.filename} {self.id} ({self.version})]:"

    def _field_parser(self, field: dict) -> Field:
        """ Maps field to a correct field class, based on @type attribute"""
        field_type = field.get('@type')
        if field_type not in ALLOWED_FIELDS.keys():
            raise FormException(
                f'{self._exc_header} Found field of type {field_type}, which is unknown')

        return ALLOWED_FIELDS[field_type](**field)

    def validate_declaration(self):
        """ Validates a form declaration while parsing xml.
        Will raise an exception when fails."""
        form = self.__dict__

        for attr in self._form_required_args:
            if not form.get(attr):
                raise InvalidFormFileError(
                    f'{self._exc_header} Form should have required attribute: {attr}')

        if not form.get('fields'):
            raise InvalidFormFileError(
                f'{self._exc_header} Form has no fields')

        for field in self.fields:
            try:
                field.validate_declaration()
            except FormException as fe:
                raise FormException(
                    f'{self._exc_header} {fe}')

    @property
    def template(self):
        fields = [i.template for i in self.fields]

        return {
            'form': {
                '@method': "POST",
                '@action': "",
                'div': fields
            }
        }

    def to_html(self):
        return xmltodict.unparse(
            full_document=False,
            short_empty_elements=True,
            input_dict=self.template
        )
