import setuptools

with open('requirements/production.txt', 'r') as f:
    install_reqs = [
        s for s in [
            line.strip(' \n') for line in f
        ] if not s.startswith('#') and s != ''
    ]

# Fields marked as "Optional" may be commented out.
setuptools.setup(
    name="middleware_service",  # Required
    version="0.0.1",  # Required
    author="Virtustream",  # Optional
    description="Middleware Service",  # Required
    packages=setuptools.find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
    include_package_data=True,  # Optional
    install_requires=install_reqs)
