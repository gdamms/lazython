from setuptools import setup, find_packages

setup(
    name='lazython',
    version='0.1.0',
    license="MIT",
    description='Python library for lazy people.',
    long_description=open('README.md').read(),
    author='Damien Guillotin',
    author_email='damguillotin@gmail.com',
    url='https://www.github.com/gdamms/lazython',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],
)
