import json
import asyncio
from datetime import datetime
from dataclasses import dataclass
from httpsrv.web.urls import urlpatterns

RESPONCE_H = (
    "{version} 200 OK\r\n"
    "Date: {date}\r\n"
    "Server: {srv}\r\n"
    "Content-Type: text/html\r\n"
    "Content-Lenght: {lenght}\r\n"
    "Connection: keep-alive"
)


@dataclass
class Request:
    meth: str
    path: str
    version: str
    headers: dict
    body: str

    def text(self):
        return self.body

    def json(self):
        return json.loads(self.body)


class Controller(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        raw_data = data.decode("utf-8")
        raw_info, body = raw_data.split("\r\n\r\n")
        raw_http, *raw_headers = raw_info.split("\r\n")
        headers = dict(list(map(lambda l: tuple(l.split(": ")), raw_headers)))
        meth, path, version = raw_http.split(" ")
        req = Request(meth, path, version, headers, body)

        # handler = tuple(filter(lambda v: path == v[0], urlpatterns))[0][1]
        # resp = handler(req)
        # loop = asyncio.get_running_loop()

        handler = None

        for pattern, view in urlpatterns:
            if path == pattern:
                handler = view
                break

        if handler is not None:
            resp = handler(req)
            loop = asyncio.get_running_loop()
        else:
            print(f"No handler found for path: {path}")
            self.transport.close()
            return

        def send_recp_cb(task: asyncio.Task):
            result = task.result()
            heads = RESPONCE_H.format(
                version=req.version,
                date=datetime.now().strftime("%a %d %b %Y %H:%M:%S"),
                srv="Perfect server v 0.1.0",
                lenght=len(result),
            )
            responce = f"{heads}\r\n\r\n{result}"

            self.transport.write(responce.encode("utf-8"))
            self.transport.close()

        loop.create_task(resp).add_done_callback(send_recp_cb)
