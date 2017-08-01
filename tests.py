import bottle, unittest
from boddle import boddle


class TestBoddle(unittest.TestCase):
  
  def testParams(self):
    with boddle(params={'name':'derek'}):
      self.assertEqual(bottle.request.params['name'], 'derek')
 
  def test_no_params_no_throw(self):
    with boddle():
      self.assertEqual(list(bottle.request.params.items()), [])
 
  def testGetParams(self):
    with boddle(method='get', params={'name':'derek'}):
      self.assertEqual(bottle.request.params['name'], 'derek')
 
  def testPostParams(self):
    with boddle(method='post', params={'name':'derek'}):
      self.assertEqual(bottle.request.params['name'], 'derek')
 
  def testPath(self):
    with boddle(path='/derek'):
      self.assertEqual(bottle.request.path, '/derek')
      with boddle(path='/anderson'):
        self.assertEqual(bottle.request.path, '/anderson')
      self.assertEqual(bottle.request.path, '/derek')
 
  def testMethod(self):
    with boddle(method='post'):
      self.assertEqual(bottle.request.method, 'POST')
 
  def testHeaders(self):
    with boddle(headers={'x_header':'value'}):
      self.assertEqual(bottle.request.headers['X_HEADER'], 'value')

  def testHyphenatedHeaders(self):
    with boddle(headers={'x-header':'value'}):
      self.assertEqual(bottle.request.headers['X-HEADER'], 'value')
 
  def testExtraStuff(self):
    with boddle(extra='woot'):
      self.assertEqual(bottle.request.extra, 'woot')
      with boddle(extra='woot2'):
        self.assertEqual(bottle.request.extra, 'woot2')
    self.assertFalse(hasattr(bottle.request,'extra'))
 
  def testJSON(self):
    with boddle(json={'name':'derek'}):
      self.assertEqual(bottle.request.json['name'], 'derek')
 
  def testURL(self):
    with boddle(url='https://github.com/keredson/boddle'):
      self.assertEqual(bottle.request.url, 'https://github.com/keredson/boddle')
      self.assertEqual(bottle.request.fullpath, '/keredson/boddle')
      self.assertEqual(bottle.request.path, '/keredson/boddle')

  def testRevert(self):
    with boddle(params={'name':'derek'}):
      self.assertEqual(bottle.request.params['name'], 'derek')
      with boddle(params={'name':'anderson'}):
        self.assertEqual(bottle.request.params['name'], 'anderson')
      self.assertEqual(bottle.request.params['name'], 'derek')
 
  def testBody(self):
    with boddle(body='body'):
      self.assertEqual(bottle.request.body.read(), b'body')
      self.assertEqual(bottle.request.body.readline(), b'body')
 
  
if __name__=='__main__':
  unittest.main()

