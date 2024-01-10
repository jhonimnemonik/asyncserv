import asyncio
from argparse import ArgumentParser
from datetime import date
from ._server import Server


__all__ = ("run",)


def get_args():
    parser = ArgumentParser(prog=f"Test server{date.today()}")
    parser.add_argument("--port", type=int, default=8000, help="Port")
    parser.add_argument("--host", default="127.0.0.1", help="Host")
    return parser.parse_args()


def run():
    args = get_args()
    print(args)
    srv = Server(host=args.host, port=args.port)
    try:
        asyncio.run(srv())
    except KeyboardInterrupt:
        print("Adios, amigo!!!")
