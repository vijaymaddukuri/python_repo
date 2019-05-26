import setuptools
import re
import os

def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    print(os.path.join(package, '__init__.py'))
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.match("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)

version = get_version('ONBFactory')

with open('requirements/production.txt', 'r') as f:
    install_reqs = [
        s for s in [
            line.strip(' \n') for line in f
        ] if not s.startswith('#') and s != ''
    ]

# Fields marked as "Optional" may be commented out.
setuptools.setup(
   name="tenant_automation_service",  # Required
   version=version,  # Required
   author="VIJAY",  # Optional
   description="Tenant Automation Service",  # Required
   packages=setuptools.find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
   include_package_data=True,  # Optional
   install_requires=install_reqs
   )
