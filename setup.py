
import os
from setuptools import setup

from mongo_storage import VERSION

REQUIREMENTS = [
    'django',
    'pymongo',
]
README = os.path.join(os.path.dirname(__file__), 'README.txt')
LONG_DESCRIPTION = open(README, 'r').read()
CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Environment :: Web Environment",
    "Framework :: Django",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Topic :: Software Development",
    "Topic :: Software Development :: Libraries :: Application Frameworks",
]

setup(
    name="django-mongo-storage",
    version=VERSION,
    author="Aaron Madison",
    author_email="aaron.l.madison@gmail.com",
    description="A mongo GridFS storage backend for django.",
    long_description=LONG_DESCRIPTION,
    url="https://github.com/madisona/django-mongo-storage",
    packages=("mongo_storage",),
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    zip_safe=False,
)
