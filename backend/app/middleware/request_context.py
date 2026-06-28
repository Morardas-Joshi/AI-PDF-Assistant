from time import perf_counter
from typing import Any
from uuid import uuid4


class RequestContextMiddleware:
    def __init__(self, app: Any) -> None:
        self.app = app

    async def __call__(self, scope: dict[str, Any], receive: Any, send: Any) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        headers = dict(scope.get("headers", []))
        request_id = headers.get(b"x-request-id", str(uuid4()).encode()).decode()
        started_at = perf_counter()

        async def send_with_context(message: dict[str, Any]) -> None:
            if message["type"] == "http.response.start":
                duration_ms = (perf_counter() - started_at) * 1000
                message.setdefault("headers", [])
                message["headers"].append((b"x-request-id", request_id.encode()))
                message["headers"].append((b"x-response-time-ms", f"{duration_ms:.2f}".encode()))
            await send(message)

        await self.app(scope, receive, send_with_context)
