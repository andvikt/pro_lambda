from setuptools import setup

with open('VERSION', 'r') as f:
    version = f.read()

with open('README.md', 'r') as f:
    desc = f.read()

setup(
    name='pro_lambda',
    version=version,
    python_requires='>=3.7',
    packages=['pro_lambda'],
    url='https://github.com/andvikt/pro_lambda',
    license='MIT',
    author='Viktorov A.G.',
    author_email='andvikt@gmail.com',
    description='Lambda with math operators support',
    tests_require=['pytest', 'pytest_asyncio'],
    # long_description=desc,
    # long_description_content_type='text/markdown',
)
