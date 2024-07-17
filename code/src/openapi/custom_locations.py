from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI
from typing import Any, Dict

def custom_openapi(app: FastAPI) -> Dict[str, Any]:
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Your API",
        version="1.0.0",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    # Добавление префикса /api ко всем путям
    paths = {}
    for path, path_info in openapi_schema["paths"].items():
        paths[f"/api{path}"] = path_info
    openapi_schema["paths"] = paths
    app.openapi_schema = openapi_schema
    return app.openapi_schema
