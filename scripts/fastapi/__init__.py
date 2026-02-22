"""Lightweight FastAPI test shim for environments without fastapi installed."""

from dataclasses import dataclass
from typing import Any, Callable, Optional, Union


@dataclass
class _Route:
    path: str
    endpoint: Callable[..., Any]
    methods: set[str]


class Request:
    def __init__(self, payload: Optional[dict] = None, app: Any = None):
        self._payload = payload or {}
        self.app = app

    async def json(self) -> dict:
        return self._payload


class _State:
    def __init__(self):
        self._data = {}

    def __getattr__(self, name):
        return self._data.get(name)

    def __setattr__(self, name, value):
        if name == "_data":
            super().__setattr__(name, value)
        else:
            self._data[name] = value


class FastAPI:
    def __init__(self, title: str = "FastAPI", lifespan: Any = None):
        self.title = title
        self.lifespan = lifespan
        self.routes: list[_Route] = []
        self.state = _State()

    def add_middleware(self, *args, **kwargs) -> None:
        return None

    def add_api_route(
        self, path: str, endpoint: Callable[..., Any], methods: list[str] = None
    ):
        self.routes.append(
            _Route(path=path, endpoint=endpoint, methods=set(methods or []))
        )
        return endpoint

    def get(self, path: str, response_class: Any = None):
        def decorator(func: Callable[..., Any]):
            self.routes.append(_Route(path=path, endpoint=func, methods={"GET"}))
            return func

        return decorator

    def post(self, path: str):
        def decorator(func: Callable[..., Any]):
            self.routes.append(_Route(path=path, endpoint=func, methods={"POST"}))
            return func

        return decorator

    def delete(self, path: str):
        def decorator(func: Callable[..., Any]):
            self.routes.append(_Route(path=path, endpoint=func, methods={"DELETE"}))
            return func

        return decorator
