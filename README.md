![image](https://cloud.githubusercontent.com/assets/2049665/21398745/27452db6-c76e-11e6-8605-8e5f3301472b.png)

# boddle
A unit testing tool for Python's bottle library.  We wrote this for our own testing purposes at https://www.hvst.com.

## Install
```
sudo pip install boddle
```

## Usage
Assuming you have a bottle route like this:

```python
@app.get('/woot')
def woot():
  return bottle.request.params['name']
```

You can unit test it like:

```python
import unittest
from boddle import boddle

class TestIt(unittest.TestCase):
  def testWoot(self):
    with boddle(params={'name':'derek'}):
      self.assertEqual(woot(), 'derek')
```

## Testing
```
$ git clone https://github.com/keredson/boddle.git
$ cd boddle
$ python tests.py 
..........
----------------------------------------------------------------------
Ran 10 tests in 0.001s

OK
```
