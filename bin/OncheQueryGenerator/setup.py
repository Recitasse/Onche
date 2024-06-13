from setuptools import setup, find_packages
from getpass import getuser

setup(
    name='OncheQueryGenerator',
    version=f'0.2.0',
    author=f'{getuser()}',
    #author_email='your.email@example.com',
    description='Package de génération',
    packages=find_packages(where='OQG', include=[
        'OQG.OQG.OQG_App',
        'OQG.OQG_Operator',
        'OQG.OQG_Types',
        'OQG.OQG_Types_refactor'
    ]),
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
        'infos': [
            'OncheQueryGenerator/OQG/Calice',
            'OncheQueryGenerator/OQG/OQG_Types']
    },
)
