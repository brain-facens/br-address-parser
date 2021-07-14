from setuptools import find_packages, setup

setup(
    name="br_address_parser",
    version="0.1.0",
    author="Emanuel Huber",
    author_email="emanuel.tesv@gmail.com",
    packages=find_packages(),
    license="MIT",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/brain-facens/br-address-parser",
    keywords=["br-address", "address", "address-parser"],
    extras_require={
        "dev": ["pytest>=6.2.0", "flake8>=3.9.2", "black>=21.6b0", "isort>-4.3.21"]
    },
)
