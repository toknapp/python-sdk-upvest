import os

import setuptools

_VERSION = "0.0.7"

_README = open(os.path.join(os.path.dirname(__file__), "README.md")).read()

_INSTALL_REQUIRES = ("requests>=2.21.0,<3", "environs==4.1.0")
_OPTIONAL_REQUIRES = {
    "dev": ("pre-commit==1.10.5", "prospector==1.1.6.2"),
    "test": ("pytest==4.2.0", "py-ecc==1.7.0", "pysha3==1.0.2", "bitcoin==1.1.42", "ethereum==2.3.2"),
}

_CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

_KEYWORDS = ["api", "upvest", "bitcoin", "ethereum", "oauth2", "client"]

_PACKAGES = setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])

setuptools.setup(
    name="upvest",
    version=_VERSION,
    author="Upvest GmbH",
    author_email="tech@upvest.co",
    maintainer="Alexander Reichhardt",
    maintainer_email="alexander@upvest.co",
    description="Upvest API client library",
    keywords=_KEYWORDS,
    long_description=_README,
    long_description_content_type="text/markdown",
    url="https://github.com/upvestco/upvest-python/",
    packages=_PACKAGES,
    include_package_data=True,
    classifiers=_CLASSIFIERS,
    install_requires=_INSTALL_REQUIRES,
    extras_require=_OPTIONAL_REQUIRES,
    license="MIT",
)
