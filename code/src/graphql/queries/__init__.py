import os
import importlib
import strawberry


QUERY_CLASSES = []

for filename in os.listdir(os.path.dirname(__file__)):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = f'src.graphql.queries.{filename[:-3]}'
        module = importlib.import_module(module_name)
        query_class_name = filename[:-3].capitalize() + 'Query'
        if hasattr(module, query_class_name):
            QUERY_CLASSES.append(getattr(module, query_class_name))


@strawberry.type
class Query(*QUERY_CLASSES):
    pass
