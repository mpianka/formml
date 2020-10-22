class Widget:
    _field_classes = ()
    _field_type = "text"

    def __init__(self, field, **kwargs: dict) -> None:
        self.field = field
        self.custom_class = field.custom_class
        self.custom_id = field.custom_id
        self.additional_input_attrs = [i.additional_input_attrs for i in field.validators]

    @property
    def classes(self) -> list:
        """
        Concatenates a list of classes for the current widget.

        The classes will be brought from:
            - `custom_class` param on the field
            - `_field_classes` param on the widget
        :return: A list of classes.
        """
        classes = []

        if self.custom_class:
            for cls in self.custom_class:
                classes.append(cls)

        if self._field_classes:
            for cls in self._field_classes:
                classes.append(cls)

        return classes

    @property
    def template(self):
        return {
            "div": {
                "@class": "form-group",
                "@id": f"{self.field.id}_group",
                "label": {
                    "@id": f"{self.field.id}_label",
                    "#text": self.field.label
                },
                "input": {
                    "@class": " ".join(self.classes),
                    "@id": self.custom_id or f"{self.field.id}_input",
                    "@type": self._field_type,
                    "@placeholder": self.field.placeholder,
                },
                "small": {
                    "@id": f"{self.field.id}_help",
                    "@class": "form-text",
                    "#text": self.field.errors[0] if self.field.errors else self.field.tooltip
                }
            }
        }
