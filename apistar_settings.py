import os

from apistar import Component, validators
from inspect import Parameter
from typing import Dict

__all__ = ["Settings", "SettingsComponent", "__version__"]
__version__ = "0.0.0"


class Settings(dict):
    """The type of settings dictionaries.

    Annotate your handler parameters with this to have a settings
    dictionary injected into those handlers.
    """


class SettingsComponent(Component):
    """A component that builds a settings dictionary from environment
    variables.
    """

    def __init__(self, properties: Dict[str, validators.Validator], defaults: dict = None) -> None:
        settings = defaults or {}
        required = [name for name, prop in properties.items() if not prop.has_default()]
        validator = validators.Object(properties, required=required)
        for name in validator.properties:
            value = os.getenv(name.upper())
            if value is not None:
                settings[name] = value

        self.settings = validator.validate(settings, allow_coerce=True)

    def can_handle_parameter(self, parameter: Parameter) -> bool:
        # Micro-optimization given that we know that this component
        # only ever injects values of type Settings.
        return parameter.annotation is Settings

    def resolve(self) -> Settings:
        return self.settings
