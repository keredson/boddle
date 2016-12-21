# GNU LESSER GENERAL PUBLIC LICENSE

import bottle, io
import json as lib_json

try:
  from urlparse import urlparse
  from urllib import urlencode
except ImportError:
  from urllib.parse import urlparse, urlencode


__version__ = '0.2.2'


class boddle(object):

  def __init__(self, params={}, path=None, method=None, headers=None, json=None, url=None, body=None, **extras):

    environ = {}
    self.extras = extras
    self.extra_orig = {}
    
    if params is not None:
      self._set_payload(environ, urlencode(params).encode('utf8'))
      
    if path is not None:
      environ['PATH_INFO'] = path.lstrip('/')
      
    if method is not None:
      environ['REQUEST_METHOD'] = method
      
    for k, v in (headers or {}).items():
      k = k.upper()
      environ['HTTP_'+k] = v

    if json is not None:
      environ['CONTENT_TYPE'] = 'application/json'
      self._set_payload(environ, lib_json.dumps(json).encode('utf8'))

    if body is not None:
      if body.lower:
        body = io.StringIO(unicode(body))
      environ['CONTENT_LENGTH'] = str(len(body.read()))
      body.seek(0)
      environ['wsgi.input'] = body

    if url is not None:
      o = urlparse(url)
      environ['wsgi.url_scheme'] = o.scheme
      environ['HTTP_HOST'] = o.netloc
      environ['PATH_INFO'] = o.path.lstrip('/')

    self.environ = environ
    
  def _set_payload(self, environ, payload):
    payload = bytes(payload)
    environ['CONTENT_LENGTH'] = str(len(payload))
    environ['wsgi.input'] = io.BytesIO(payload)

  def __enter__(self):
    self.orig = bottle.request.environ
    bottle.request.environ = self.environ
    for k,v in self.extras.items():
      if hasattr(bottle.request, k):
        self.extra_orig[k] = getattr(bottle.request, k)
      setattr(bottle.request, k, v)

  def __exit__(self,a,b,c):
    bottle.request.environ = self.orig
    for k,v in self.extras.items():
      if k in self.extra_orig:
        setattr(bottle.request, k, self.extra_orig[k])
      else:
        try:
          delattr(bottle.request, k)
        except AttributeError:
          pass
        


