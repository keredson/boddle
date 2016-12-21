import os

from setuptools import setup

def long_description():
  os.system('pandoc --from=markdown --to=rst --output=README.rst README.md')
  readme_fn = os.path.join(os.path.dirname(__file__), 'README.rst')
  if os.path.exists(readme_fn):
    with open(readme_fn) as f:
      return f.read()
  else:
    return 'not available'

setup(
  name='boddle',
  version=__import__('boddle').__version__,
  description="A unit testing tool for Python's bottle library.",
  long_description=long_description(),
  author='Derek Anderson',
  author_email='public@kered.org',
  url='https://github.com/keredson/boddle',
  packages=[],
  py_modules=['boddle'],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
  ],
  install_requires=[],
)

