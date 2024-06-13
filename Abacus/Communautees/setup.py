from setuptools import setup, find_packages
from getpass import getuser

setup(
    name='Communautees',
    version="0.0.0",
    author=f'{getuser()}',
    #author_email='your.email@example.com',
    description="Package permettant d'effectuer toutes les opérations sur les communautés",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    packages_dir={'': 'Communautees'},
    packages=find_packages(where='Communautees', include=[]),
    url='http://yourpackage.example.com',
    install_requires=[
        'matplotlib==3.9.0',
        'networkx==3.3',
        'python-louvain==0.16',
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
            'README.md'
        ],
    }
)
