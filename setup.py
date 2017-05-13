from distutils.core import setup
from json import loads
from os.path import dirname, realpath

setup(
    author = 'Jascha Casadio',
    author_email = 'jaschac@hotmail.com',
    description = 'A web application to manage Fallout Shelter(C) Vaults',
    license = 'LICENSE',
    long_description = open('README').read(),
    name = 'pyshelter',
    packages =[
                'pyshelter',
                'pyshelter.classes',
                'pyshelter.tests',
                'pyshelter.utils'
                ],
    scripts = [],
    url = 'https://github.com/jaschac/pyshelter',
    version = loads(open("%s/metadata.json" % (dirname(realpath(__file__))),  \
        "r").read()).get("version"),
)