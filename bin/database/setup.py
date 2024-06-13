from setuptools import setup, find_packages
from getpass import getuser

setup(
    name='OncheDatabase',
    version="0.4.0",
    author=f'{getuser()}',
    #author_email='your.email@example.com',
    long_description=open("README.md").read(),
    description='Package database avec les entités et leurs sélecteurs',
    long_description_content_type='text/markdown',
    packages_dir={'': 'OncheDatabase'},
    packages=find_packages(where='OncheDatabase', include=['OncheDatabase.entities', 'OncheDatabase.selectors', 'OncheDatabase.link']),
    url='http://yourpackage.example.com',
    install_requires=[
        'mysql-connector==2.2.9',
        'mysql-connector-python==8.3.0'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.12',
    ],
    keywords='sample setupsrc development',
    python_requires='>=3.11',
    project_urls={
        'Documentation': 'https://yourpackage.example.com/docs',
    },
    include_package_data=True,
    package_data={
        'sample': [
            'OncheDatabase/schema.sql',
            'README.md'
        ],
    }
)
