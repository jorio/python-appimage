import json
import os
import setuptools
import ssl
import subprocess
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

from python_appimage.utils.deps import fetch_all


CLASSIFIERS = '''\
Development Status :: 4 - Beta
Intended Audience :: Developers
License :: OSI Approved :: GNU General Public License v3 (GPLv3)
Programming Language :: Python
Topic :: Software Development
Operating System :: POSIX :: Linux
'''


with open('README.md') as f:
    long_description = f.read()


def get_version():
    '''Get the next version number from PyPI
    '''
    version = os.getenv('PYTHON_APPIMAGE_VERSION')
    if not version:
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context

        meta = json.load(
                urlopen('https://pypi.org/pypi/python-appimage/json'))

        version = meta['info']['version']
        numbers = version.split('.')
        numbers[-1] = str(int(numbers[-1]) + 1)
        version = '.'.join(numbers)

    p = subprocess.Popen('git describe --match=NeVeRmAtCh --always --dirty',
                       shell=True, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT)
    stdout, _ = p.communicate()
    try:
        stdout = stdout.decode()
    except AttributeError:
        stdout = str(stdout)
    git_revision = stdout.strip()

    with open('python_appimage/version.py', 'w+') as f:
        f.write('''\
# This file was generated by setup.py
version = '{version:}'
git_revision = '{git_revision:}'
'''.format(version=version, git_revision=git_revision))

    return version


def get_package_data():
    '''Get the list of package data
    '''
    prefix = os.path.dirname(__file__) or '.'
    return ['data/' + file_
            for file_ in os.listdir(prefix + '/python_appimage/data')]


setuptools.setup(
    name = 'python_appimage',
    version = get_version(),
    author = 'Valentin Niess',
    author_email = 'valentin.niess@gmail.com',
    description = 'Appimage releases of Python',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/niess/python-appimage',
    download_url = 'https://pypi.python.org/pypi/python-appimage',
    project_urls = {
        'Bug Tracker' : 'https://github.com/niess/python-appimage/issues',
        'Source Code' : 'https://github.com/niess/python-appimage',
    },
    packages = setuptools.find_packages(),
    classifiers = [s for s in CLASSIFIERS.split(os.linesep) if s.strip()],
    license = 'GPLv3',
    platforms = ['Linux'],
    python_requires = '>=2.7',
    include_package_data = True,
    package_data = {'': get_package_data()}
)
