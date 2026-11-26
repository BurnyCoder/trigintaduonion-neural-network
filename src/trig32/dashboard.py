"""Serve the public explorer and the latest local epoch on loopback only."""
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
import json

from .paths import RESULTS,ROOT


class Dashboard(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.split("?",1)[0]!="/live.json":
            return super().do_GET()
        candidates=sorted(RESULTS.glob("*/live.json"),key=lambda p:p.stat().st_mtime,reverse=True)
        item=json.loads(candidates[0].read_bytes()) if candidates else {}
        if candidates:
            item["finished"]=candidates[0].with_name("train.json").exists()
        body=json.dumps(item).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type","application/json")
        self.send_header("Cache-Control","no-store")
        self.send_header("Content-Length",str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def serve(port):
    handler=partial(Dashboard,directory=str(ROOT/"docs"))
    # Windows otherwise allows two HTTP servers to bind the same socket with SO_REUSEADDR.
    class LocalServer(ThreadingHTTPServer):
        allow_reuse_address=False
    with LocalServer(("127.0.0.1",port),handler) as server:
        print(f"Live training dashboard at http://127.0.0.1:{server.server_port}/",flush=True)
        server.serve_forever()
