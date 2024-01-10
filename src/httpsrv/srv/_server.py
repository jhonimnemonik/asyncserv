import asyncio
from functools import partial
from contextlib import asynccontextmanager
from ._controller import Controller


class Server:
    def __init__(self, *, host: str, port: int):
        self._host = host
        self._port = port

    async def _start(self):
        loop = asyncio.get_running_loop()
        srv = partial(loop.create_server, Controller, host=self._host, port=self._port)
        async with self.server(srv) as s:
            await s.serve_forever()

    def __call__(self):
        return self._start()

    @asynccontextmanager
    async def server(self, factory):
        print(f"Server start: host - {self._host}\n port - {self._port}")
        try:
            yield await factory()
        finally:
            print("\rServer is stopped")
