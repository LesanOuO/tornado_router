from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tornado_router_plus",
    version="0.0.8",
    author="Lesan",
    description="function-based router for Tornado Web Framework that supports asynchronous authentication, json request and more",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'License :: OSI Approved :: MIT License', 'Programming Language :: Python',
        'Programming Language :: Python :: 3', 'Environment :: Web Environment'
    ],
    license="MIT",
    keywords="tornado router asynchronous decorator",
    url="https://github.com/LesanOuO/tornado_router",
    packages=find_packages(exclude=["tests"]),
    install_requires=['tornado'],
    include_package_data=True)
