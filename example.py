import bottle, unittest
from boddle import boddle


@bottle.get('/woot')
def woot():
  return bottle.request.params['name']


class TestIt(unittest.TestCase):
  def testWoot(self):
    with boddle(params={'name':'derek'}):
      self.assertEqual(woot(), 'derek')


if __name__=='__main__':
  unittest.main()
  
