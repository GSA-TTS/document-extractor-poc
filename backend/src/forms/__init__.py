import importlib
import inspect
import os
import pkgutil

from src.forms.form import Form


def find_form_implementations():
    implementations = []

    # Iterate over all modules in the package
    for _, module_name, _ in pkgutil.iter_modules([os.path.dirname(__file__)]):
        # Import the module
        module = importlib.import_module(f"{__name__}.{module_name}")

        # Iterate over all classes in the module
        for _, clazz in inspect.getmembers(module, inspect.isclass):
            # Check if the class is a subclass of the base class and is not the base class itself
            if issubclass(clazz, Form) and clazz is not Form:
                instantiation = clazz()
                implementations.append(instantiation)

    return implementations


supported_forms = find_form_implementations()
