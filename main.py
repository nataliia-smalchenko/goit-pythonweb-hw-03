from email import message
import mimetypes
import json
from pathlib import Path
import urllib.parse
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

from jinja2 import Environment, FileSystemLoader

BASE_DIR = Path(__file__).parent
jinja = Environment(loader=FileSystemLoader("templates"))


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        route = urllib.parse.urlparse(self.path)
        match route.path:
            case "/" | "/index" | "/index.html":
                self.send_html(BASE_DIR.joinpath("templates", "index.html"))
            case "/read":
                self.render_template("messages.jinja")
            case "/message" | "/message.html":
                self.send_html(BASE_DIR.joinpath("templates", "message.html"))
            case _:
                file = BASE_DIR.joinpath(route.path[1:])
                if file.exists():
                    self.send_static(file)
                else:
                    self.send_html(BASE_DIR.joinpath("templates", "error.html"), 404)

    def do_POST(self):
        size = self.headers.get("Content-Length")
        body = self.rfile.read(int(size)).decode("utf-8")
        parse_body = urllib.parse.unquote_plus(body)
        r = parse_body.split("&")
        r = {item.split("=")[0]: item.split("=")[1] for item in r}
        print(r)
        with open(
            BASE_DIR.joinpath("storage", "data.json"), "r", encoding="utf-8"
        ) as file:
            data = json.load(file)
        data[str(datetime.now())] = r
        with open(
            BASE_DIR.joinpath("storage", "data.json"), "w", encoding="utf-8"
        ) as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        self.send_response(302)
        self.send_header("Location", "/")
        self.end_headers()

    def send_html(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(filename, "rb") as file:
            self.wfile.write(file.read())

    def render_template(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        with open(
            BASE_DIR.joinpath("storage", "data.json"), "r", encoding="utf-8"
        ) as file:
            data = json.load(file)

        template = jinja.get_template(filename)
        content = template.render(messages=data)
        self.wfile.write(content.encode())

    def send_static(self, filename, status=200):
        self.send_response(status)
        mime_type, *_ = mimetypes.guess_type(filename)
        if mime_type:
            self.send_header("Content-type", mime_type)
        else:
            self.send_header("Content-type", "text/plain")
        self.end_headers()
        with open(filename, "rb") as file:
            self.wfile.write(file.read())


def run():
    server_address = ("", 3000)
    httpd = HTTPServer(server_address, MyHandler)
    print("Starting server...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server is shutting down...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    run()
