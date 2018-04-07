from setuptools import setup

setup(name='lotusstat',
      version='0.0.1',
      description='Python tools for analysing Lotus output files',
      url='https://bitbucket.org/carlosloslas/lotusstat',
      author='Carlos Losada',
      author_email='losadalastra.carlos@gmail.com',
      license='MIT',
      packages=['lotusstat'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      zip_safe=False)
