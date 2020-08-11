# GNU LESSER GENERAL PUBLIC LICENSE

import io
import json as lib_json
from base64 import b64encode


try:
  import bottle
except ImportError:
  print("you don't have bottle installed")
  

try:
  from urlparse import urlparse
  from urllib import urlencode
except ImportError:
  from urllib.parse import urlparse, urlencode


__version__ = '0.2.9'


class boddle(object):

  def __init__(self, params={}, path=None, method=None, headers=None, json=None, url=None, body=None, query={}, auth=None, **extras):

    environ = {}
    self.extras = extras
    self.extra_orig = {}
    self.orig_app_reader = bottle.BaseRequest.app

    if auth is not None:
      user, password = auth
      environ["HTTP_AUTHORIZATION"] = "Basic {}".format(b64encode(bytes(f"{user}:{password}", "utf-8")).decode("ascii"))
    
    if params is not None:
      self._set_payload(environ, urlencode(params).encode('utf8'))
      
    if path is not None:
      environ['PATH_INFO'] = path.lstrip('/')
      
    if method is not None:
      environ['REQUEST_METHOD'] = method
      
    for k, v in (headers or {}).items():
      k = k.replace('-', '_').upper()
      environ['HTTP_'+k] = v

    if json is not None:
      environ['CONTENT_TYPE'] = 'application/json'
      self._set_payload(environ, lib_json.dumps(json).encode('utf8'))

    if body is not None:
      if body.lower:
        body = io.BytesIO(bytes(body.encode('utf-8')))
      environ['CONTENT_LENGTH'] = str(len(body.read()))
      body.seek(0)
      environ['wsgi.input'] = body

    if url is not None:
      o = urlparse(url)
      environ['wsgi.url_scheme'] = o.scheme
      environ['HTTP_HOST'] = o.netloc
      environ['PATH_INFO'] = o.path.lstrip('/')

    if query is not None:
      environ['QUERY_STRING'] = urlencode(query)

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
    setattr(bottle.BaseRequest, 'app', True)

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
    setattr(bottle.BaseRequest, 'app', self.orig_app_reader)


