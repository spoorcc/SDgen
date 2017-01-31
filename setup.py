from setuptools import setup, find_packages

version = '0.0.1'


setup(
  name                 = 'SDgen',
  version              = version,
  description          = 'Interface generator for ServiceDispatcher',
  url                  = 'http://github.com/spoorcc/SDgen',
  author               = 'Ben Spoor',
  author_email         = 'ben.spoor@gmail.com',
  packages             = find_packages(),
  zip_safe             = True,
  install_requires     = ['idl_parser'],
  extras_require       = {'test': ['behave>=1.2.4']},
  scripts              = ['bin/SDgen.py'],
)
