from setuptools import setup

with open('VERSION', 'r') as f:
    version = f.read()

setup(
    name='pro_lambda',
    version=version,
    packages=['pro_lambda'],
    url='',
    license='',
    author='Viktorov A.G.',
    author_email='andvikt@gmail.com',
    description='Lambda with math operators support',
    tests_require=['pytest', 'pytest_asyncio'],
)
