"""Local preview gateway for the NanoPro AI Lab.

Serves the production edge gateway (Cloudflare Worker -> Render origin) on
localhost so it can be rendered inside TRAE's right-side Preview panel, which
only proxies local HTTP servers.

Run:  python3 nanopro_preview_gateway.py
Then open: http://localhost:8000/
"""

import http.server
import socketserver
import urllib.error
import urllib.request

TARGET = "https://nanopro-prod.mangeshbagul15.workers.dev"
PORT = 8000

HOP_BY_HOP = {
    "connection", "keep-alive", "proxy-authenticate", "proxy-authorization",
    "te", "trailers", "transfer-encoding", "upgrade", "host", "content-length",
}


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_OPENER = urllib.request.build_opener(_NoRedirect)


class Gateway(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _forward(self):
        url = TARGET + self.path
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length) if length else None

        headers = {
            k: v for k, v in self.headers.items()
            if k.lower() not in HOP_BY_HOP
        }

        try:
            req = urllib.request.Request(url, data=body, headers=headers, method=self.command)
            resp = _OPENER.open(req, timeout=90)
        except urllib.error.HTTPError as e:
            resp = e
        except Exception as e:  # noqa: BLE001 - surface upstream failure as 502
            payload = f"NanoPro gateway upstream error: {e}".encode()
            self.send_response(502)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return

        try:
            data = resp.read()
            status = resp.status if hasattr(resp, "status") else resp.code
            self.send_response(status)
            for k, v in resp.headers.items():
                if k.lower() in HOP_BY_HOP:
                    continue
                self.send_header(k, v)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(data)
        finally:
            resp.close()

    do_GET = _forward
    do_POST = _forward
    do_PUT = _forward
    do_DELETE = _forward
    do_OPTIONS = _forward
    do_HEAD = _forward

    def log_message(self, fmt, *args):
        print(f"[gateway] {self.address_string()} {fmt % args}", flush=True)


class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == "__main__":
    with ThreadingHTTPServer(("0.0.0.0", PORT), Gateway) as httpd:
        print(f"NanoPro preview gateway -> {TARGET} on http://localhost:{PORT}/", flush=True)
        httpd.serve_forever()
