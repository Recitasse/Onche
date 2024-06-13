from setuptools import setup, find_packages
from getpass import getuser

setup(
    name='Scrapper',
    version='0.4.0',
    author=f'{getuser()}',
    #author_email='your.email@example.com',
    description='Package de récupération de donnée de Onche',
    long_description_content_type='text/markdown',
    packages=find_packages(where='WebScrapper',
                           include=['WebScrapper.OncheScrapper']),
    url='http://yourpackage.example.com',
    install_requires=[
        'mysql-connector==2.2.9',
        'mysql-connector-python==8.3.0',
        'prettytables==1.1.5',
        'bs4==0.0.2',
        'beautifulsoup4==4.12.3',
        'requests==2.32.3'
    ],
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Programming Language :: Python :: 3.12',
    ],
    keywords='sample setuptools development',
    python_requires='>=3.11',
    project_urls={
        'Documentation': 'https://yourpackage.example.com/docs',
    }
)
