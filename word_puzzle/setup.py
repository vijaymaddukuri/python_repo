import setuptools
import re
import os.path

from inspect import getsourcefile

current_path = os.path.abspath(getsourcefile(lambda: 0))
current_dir = os.path.dirname(current_path)

def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    print(os.path.join(package, '__init__.py'))
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.match("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)

version = get_version(current_dir)

with open('requirements/requirements.txt', 'r') as f:
    install_reqs = [
        s for s in [
            line.strip(' \n') for line in f
        ] if not s.startswith('#') and s != ''
    ]

# Fields marked as "Optional" may be commented out.
setuptools.setup(
   name="word_puzzle",  # Required
   version=version,  # Required
   author="Vijay",  # Optional
   description="Word puzzle game",  # Required
   packages=setuptools.find_packages(),  # Required
   include_package_data=True,  # Optional
   install_requires=install_reqs
   )
