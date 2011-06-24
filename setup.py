
import os
from setuptools import setup

from mongo_storage import VERSION

REQUIREMENTS = (
    'django',
    'pymongo'
) 
README = os.path.join(os.path.dirname(__file__), 'README.txt')
LONG_DESCRIPTION = open(README).read()
CLASSIFIERS = (
    "Development Status :: 3 - Alpha",
    "Environment :: Web Environment",
    "Framework :: Django",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Topic :: Software Development",
    "Topic :: Software Development :: Libraries",
    "Topic :: Software Development :: Libraries :: Application Frameworks",
)

setup(
    version=VERSION,
    name="django-mongo-storage",
    author="Aaron Madison and Matt Morrison",
    description="A mongo GridFS storage backend for django",
    long_description=LONG_DESCRIPTION,
    packages=('mongo_storage',),
    install_requires = REQUIREMENTS,
    classifiers=CLASSIFIERS,
    zip_safe=False,
)