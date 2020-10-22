import glob
import logging
import os
import sys

import xmltodict

from formml.exceptions import InvalidFormFileError, DuplicateFormError
from formml.forms.form import Form

logging.basicConfig()
log = logging.getLogger(__name__)


class XmlLoader:
    def __init__(self):
        pass

    @staticmethod
    def load_directory(path: str) -> list[Form]:
        forms = []
        if not os.path.exists(path) or not os.path.isdir(path):
            log.error(f"Directory {path} is not valid")
            raise NotADirectoryError

        for file in glob.glob(os.path.join(path, '*.xml'), recursive=True):
            loader = XmlLoader.load_file(file)

            for form in loader:
                for f in forms:
                    if f.id == form.id and f.version == form.version:
                        raise DuplicateFormError(f"Form {form.id} ({f.version}) already exists in {f.filename}!")
                forms.append(form)

        return forms

    @staticmethod
    def load_file(path: str) -> list[Form]:
        if not os.path.exists(path) or not os.path.isfile(path):
            log.error(f"File {path} is not valid")
            raise InvalidFormFileError

        with open(path, 'r') as xml:
            forms = []
            parsed = xmltodict.parse(
                xml_input=xml.read(),
                xml_attribs=True,
                force_list=('Validator', 'Field', 'Form', 'FormGroup'),
                dict_constructor=dict
            )

            log.info(f"Validating and parsing file {path}...")
            form_group = parsed.get('FormGroup')

            if not form_group:
                raise InvalidFormFileError(f"{path}: no FormGroup found")

            if len(form_group) > 1:
                raise InvalidFormFileError(f"{path}: too many FormGroups, only one is allowed")
            form_group = form_group[0]

            if 'Form' not in form_group:
                raise InvalidFormFileError(f"{path}: FormGroup does not have Forms")

            for form_list in form_group.values():
                for form in form_list:
                    new_form = Form(path, **form)
                    new_form.validate_declaration()
                    forms.append(new_form)

            return forms
