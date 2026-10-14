# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 BQ Cervantes 3 offline unlock contributors
# This program is free software under GPL version 3 or later.
# It is distributed without any warranty. See LICENSE for details.

import importlib.util, pathlib, threading, urllib.request, urllib.error, posixpath
from http.server import ThreadingHTTPServer
p=pathlib.Path(__file__).resolve().parents[1] / 'server.py'
s=importlib.util.spec_from_file_location('bq_download_probe',p)
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
assert posixpath.normpath('/mnt/public/'+m.PROBE_FILENAME)=='/mnt/public/bq_download_probe'
assert posixpath.normpath('/mnt/public/'+m.MARKER_FILENAME)=='/mnt/private/hackers_e60q22_ok'
assert posixpath.normpath('/mnt/public/'+m.LEGACY_MARKER_FILENAME)=='/mnt/private/hackers_ok'
assert all('.acsm' in name for name in (m.PROBE_FILENAME, *m.MARKER_ROUTES.values()))
for enabled in (False,True):
    server=ThreadingHTTPServer(('127.0.0.1',0),m.handler_class(enabled))
    t=threading.Thread(target=server.serve_forever,daemon=True);t.start()
    base=f'http://127.0.0.1:{server.server_port}'
    try:
        with urllib.request.urlopen(base+'/') as r:
            html=r.read()
            for route in m.MARKER_ROUTES:
                assert (('action="'+route+'"').encode() in html)==enabled
            assert not any(k.lower() in ('wsservicesurl','shopname') for k in r.headers)
        for _ in range(2):
            with urllib.request.urlopen(base+'/probe') as r:
                assert r.read()==m.PROBE_BODY
                assert r.headers['Content-Disposition']=='attachment; filename="'+m.PROBE_FILENAME+'"'
                assert int(r.headers['Content-Length'])==len(m.PROBE_BODY)
        for route,filename in m.MARKER_ROUTES.items():
            if enabled:
                for _ in range(2):
                    with urllib.request.urlopen(base+route) as r:
                        assert r.read()==b'ok'
                        assert r.headers['Content-Disposition']=='attachment; filename="'+filename+'"'
                        assert r.headers['Content-Length']=='2'
            else:
                try:urllib.request.urlopen(base+route);raise AssertionError('Marker unexpectedly enabled')
                except urllib.error.HTTPError as e:assert e.code==403
        try:urllib.request.urlopen(base+'/etc/passwd');raise AssertionError('Arbitrary route served')
        except urllib.error.HTTPError as e:assert e.code==404
    finally:
        server.shutdown();server.server_close();t.join()
print('PASS: local HTTP, repeat downloads, marker gating, route limits and lexical paths. These checks do not emulate a reader.')
