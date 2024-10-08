import os
import importlib

import strawberry

mutation_modules = []
for file in os.listdir(os.path.dirname(__file__)):
    if file.endswith(".py") and file != "__init__.py":
        module_name = file[:-3]
        module = importlib.import_module(f"src.graphql.mutations.{module_name}")
        mutation_modules.append(module)

mutation_classes = [getattr(module, cls) for module in mutation_modules for cls in dir(module) if cls.endswith("Mutation")]


@strawberry.type
class Mutation(*mutation_classes):
    pass
