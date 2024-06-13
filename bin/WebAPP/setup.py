from setuptools import setup, find_packages
from getpass import getuser

setup(
    name='BabelOnche',
    version='0.1.0',
    author=f'{getuser()}',
    #author_email='your.email@example.com',
    description='Package de la WebApp',
    packages=find_packages(where='BabelOnche',
                           include=['BabelOnche.API']),
    install_requires=[
        'mysql-connector==2.2.9',
        'mysql-connector-python==8.3.0',
        'flask==3.0.3',
        'tornado==6.4.1'
    ],
    url='http://yourpackage.example.com',
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Programming Language :: Python :: 3.12',
    ],
    keywords='sample setuptools development',
    python_requires='>=3.10',
    project_urls={
        'Documentation': 'https://yourpackage.example.com/docs',
    },
    include_package_data=True,
    package_data={
        'sample': ['BabelOnche/html/*'],
    }
)
