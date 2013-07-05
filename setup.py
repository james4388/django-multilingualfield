import os
from setuptools import setup

setup(
    name = "django-multilingualfield",
    version = open(os.path.join(os.path.dirname(__file__), 'multilingualfield', 'VERSION')).read().strip(),
    description = "MultilingualField for django models",
    long_description = open("README.rst").read(),
    url = "https://github.com/spyjamesbond0072003/django-multilingualfield",
    author = "James",
    author_email = "spyjamesbond0072003@gmail.com",
    packages = [
        "multilingualfield",
    ],
    classifiers = [
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Framework :: Django',
    ],
    test_suite='tests.main',
    include_package_data=True,
)
