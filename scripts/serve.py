#!/usr/bin/env python3
"""Static server for Haazinu with no-cache headers (so edits show up on plain reload). Usage: python3 scripts/serve.py [port]"""
import http.server, sys, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
class H(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store"); super().end_headers()
    def send_response_only(self, code, message=None):  # never answer 304
        super().send_response_only(code, message)
    def do_GET(self):
        self.headers.replace_header("If-Modified-Since", "") if "If-Modified-Since" in self.headers else None
        super().do_GET()
http.server.ThreadingHTTPServer(("", int(sys.argv[1]) if len(sys.argv) > 1 else 8787), H).serve_forever()
