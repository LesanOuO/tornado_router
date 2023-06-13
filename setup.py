from setuptools import setup

setup(
    name="tornado_router",
    version="0.0.1",
    author="Lesan",
    description="function-based router for Tornado Web Framework that supports asynchronous authentication, json request and more",
    classifiers=[
        'License :: OSI Approved :: MIT License', 'Programming Language :: Python',
        'Programming Language :: Python :: 3', 'Environment :: Web Environment'
    ],
    license="MIT",
    keywords="tornado router asynchronous decorator",
    url="https://github.com/LesanOuO/tornado_router",
    py_modules=['tornado_router'],
    install_requires=['tornado'],
    include_package_data=True)
