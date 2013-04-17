
from setuptools import setup, find_packages


setup(name='ssl-generator',
      version='0.0.0',
      author='Justin Witrick',
      author_email='justin.witrick@mailtrust.com',
      description='SSL API for auto signing an ssl request.',
      packages=find_packages(),
      entry_points={'console_scripts':
              ['ssl-generator = sslgenerator.sslgenerator:main', ]},
      install_requires=['twisted', "mock", ])


# vim:et:fdm=marker:sts=4:sw=4:ts=4
