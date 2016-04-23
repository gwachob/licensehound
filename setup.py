from setuptools import setup

setup(name='licensehound',
      version='0.1',
      description='Tool for discovering actual licensing for PyPI projects',
      url='http://github.com/gwachob/licensehound',
      author='Gabe Wachob',
      author_email='gwachob@wachob.com',
      license='Apache 2.0',
      packages=['licensehound'],
      zip_safe=False,
      install_requires=[
          'requests',
      ],
      entry_points={
        'console_scripts': ['get-package-info=licensehound.command_line:get_package_info'],
      }
      )
