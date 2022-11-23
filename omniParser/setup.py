import setuptools
from platform import python_version

tests_require = [
    "pytest",
    "mypy",
]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    install_requires = f.readlines()

setuptools.setup(
    name="omniParser",
    version="1.0.0",
    author="Suresh Nakkeran",
    author_email="suresh.nakkeran@healthec.com",
    description="A python wrapper for omniParser",
    long_description=long_description,
    python_requires= ">=3.8",
    packages=[
        "omniparser",
        "omniparser.bin",
        "omniparser.schemas",
    ],
    include_package_data=True,
    install_requires=install_requires,
    tests_require=tests_require,
)