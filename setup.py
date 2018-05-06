from setuptools import setup
from lotusstat import version

setup(name='lotusstat',
      version=version,
      description='Python tools for analysing Lotus output files',
      url='https://bitbucket.org/carlosloslas/lotusstat',
      author='Carlos Losada',
      author_email='losadalastra.carlos@gmail.com',
      license='MIT',
      packages=['lotusstat'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      zip_safe=False)
