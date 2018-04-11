import os

from apistar import Component, validators
from inspect import Parameter
from typing import Any, Dict

__all__ = ["Settings", "SettingsComponent", "__version__"]
__version__ = "0.2.0"


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
        required = []
        settings = defaults or {}
        for name, prop in properties.items():
            value = os.getenv(name)
            if value is not None:
                settings[name] = value

            if not prop.has_default():
                required.append(name)

        validator = validators.Object(properties, required=required)
        self.settings = Settings(validator.validate(settings, allow_coerce=True))

    def can_handle_parameter(self, parameter: Parameter) -> bool:
        # Micro-optimization given that we know that this component
        # only ever injects values of type Settings.
        return parameter.annotation is Settings

    def resolve(self) -> Settings:
        return self.settings

    def __getattr__(self, name: str) -> Any:
        return getattr(self.settings, name)

    def __getitem__(self, name: str) -> Any:
        return self.settings[name]

    def __setitem__(self, name: str, value: Any) -> None:
        self.settings[name] = value
