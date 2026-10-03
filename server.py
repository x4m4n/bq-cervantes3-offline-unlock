# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 BQ Cervantes 3 offline unlock contributors
# This program is free software under GPL version 3 or later.
# It is distributed without any warranty. See LICENSE for details.

"""A narrow, two-stage test of the stock BQ browser's download filename handling.

Create the folder _bq_probe.acsm on the reader's USB-visible internal storage.
Default mode writes only a harmless public-storage probe through the reader.
--enable-marker additionally offers the source-confirmed Cervantes 3 marker.
No firmware, startup scripts, keys, or account registration are served.
"""
import argparse, json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

FOLDER = '_bq_probe.acsm'
PROBE_NAME = 'bq_download_probe'
PROBE_BODY = b'BQ browser download path probe: public storage only.\n'
PROBE_FILENAME = FOLDER + '/../' + PROBE_NAME
MARKER_FILENAME = FOLDER + '/../../private/hackers_e60q22_ok'

def handler_class(enable_marker=False):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            pass
        def do_GET(self):
            path = urlsplit(self.path).path
            print(json.dumps({'method':'GET','path':path,'host':self.headers.get('Host')}),flush=True)
            filename = None
            if path == '/':
                message = '''<!doctype html><html><head><meta charset="utf-8"><title>BQ download probe</title></head>
<body style="font:24px sans-serif;line-height:1.5">
<h1>BQ browser probe</h1>
<p>First create the folder <b>_bq_probe.acsm</b> on the reader's internal USB storage and safely disconnect USB.</p>
<p><a href="/probe">1. Download the harmless public-storage probe</a></p>
<p>Check through USB that <b>bq_download_probe</b> appeared next to that folder and contains the expected text.</p>
'''
                if enable_marker:
                    message += '<p>Only after the public probe succeeds:</p><p><a href="/marker">2. Write the Cervantes 3 authorization marker</a></p><p>This writes two bytes, ok, to the private authorization file. It does not flash firmware.</p>'
                else:
                    message += '<p>Authorization-marker download is disabled in this run.</p>'
                message += '</body></html>'
                code,content_type,body = 200,'text/html; charset=utf-8',message.encode('utf-8')
            elif path == '/probe':
                code,content_type,body = 200,'application/octet-stream',PROBE_BODY
                filename=PROBE_FILENAME
            elif path == '/marker' and enable_marker:
                code,content_type,body = 200,'application/octet-stream',b'ok'
                filename=MARKER_FILENAME
            elif path == '/marker':
                code,content_type,body = 403,'text/plain; charset=utf-8',b'Marker disabled. Run the public-storage probe first.\n'
            else:
                code,content_type,body = 404,'text/plain; charset=utf-8',b'Unknown endpoint\n'
            self.send_response(code)
            self.send_header('Content-Type',content_type)
            self.send_header('Content-Length',str(len(body)))
            self.send_header('Cache-Control','no-store')
            self.send_header('Connection','close')
            if filename:
                self.send_header('Content-Disposition','attachment; filename="'+filename+'"')
            self.end_headers()
            self.wfile.write(body)
            self.close_connection=True
    return Handler

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--bind',default='127.0.0.1')
    p.add_argument('--port',type=int,default=8000)
    p.add_argument('--enable-marker',action='store_true')
    a=p.parse_args()
    server=ThreadingHTTPServer((a.bind,a.port),handler_class(a.enable_marker))
    print(f'HTTP listener on {a.bind}:{server.server_port}; marker enabled={a.enable_marker}',flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__=='__main__':
    main()
