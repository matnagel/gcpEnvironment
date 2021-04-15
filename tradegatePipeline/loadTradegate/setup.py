from setuptools import setup

setup(
    name='loadTradegatePipeline',
    author='Matthias Nagel',
    author_email='matthinagel@gmail.com',
    url='https://github.com/matnagel/gcpEnvironment',
    version='0.1',
    install_requires=[
        'sqlalchemy',
        'pymysql'
    ],
    packages={'gcp':'gcp'}
    #setuptools.find_namespace_packages()
)
