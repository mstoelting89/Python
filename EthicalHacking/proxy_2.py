from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import urllib
from socketserver import ThreadingMixIn

class MyRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        print(self.path)
        print(self.headers)

        if self.headers["content-type"] == "application/x-www-form-urlencoded":
            length = int(self.headers["content-length"])
            form = str(self.rfile.read(length),"UTF-8")
            data = urllib.parse.parse_qs(form)

            if "content" in data:
                if type(data["content"]) == list:
                    if len(data["content"]) == 1:
                        data["content"][0] = data["content"][0].replace("Hallo","flop")
                    print(data)

            with requests.post(self.path, data = data, stream = True) as res:
                self.send_response(res.status_code)
                for key,value in res.headers.items():
                    self.send_header(key,value)
                self.end_headers()

                self.wfile.write(res.raw.read())


    def do_GET(self):
        print(self.path)
        if self.path[-4:] == ".jpg":
            self.send_response(200)
            self.send_header("Content-Type", "image/png")
            self.end_headers()

            with open("IMG_0431.PNG", "rb") as file:
                self.wfile.write(file.read())
        else:
            with requests.get(self.path, stream=True) as res:
                self.send_response(res.status_code)
                if "text/html" in res.headers["Content-Type"]:
                    self.send_header("Content-Type", "text/html")
                    self.end_headers()
                    content = str(res.content, "utf-8")
                    content = content.replace("Bilder","Katzenbilder")
                    self.wfile.write(content.encode())
                else:
                    for key, value in res.headers.items():
                        self.send_header(key, value)
                    self.end_headers()

                    self.wfile.write(res.raw.read())

address = ("127.0.0.1", 10080)

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass

server = ThreadingHTTPServer(address, MyRequestHandler)
server.serve_forever()