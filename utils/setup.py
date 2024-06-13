from setuptools import setup, find_packages
from getpass import getuser

setup(
    name='OncheUtils',
    version=f'0.4.0',
    author=f'{getuser()}',
    #author_email='your.email@example.com',
    description='Contient les outils de cryptographie, de génération pour la documentation, l affichage et les logs',
    packages=find_packages(where="/home/recitasse/Desktop/programmation/Onche",
                           exclude=['config/quality', 'config/UML'],
                           include=['config/cryptage']),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='http://yourpackage.example.com',
    install_requires=[
        'flake8==7.0.0',
        'pylint==3.0.3',
        'sphinx==7.2.6',
        'pylint==3.0.3',
        'astroid>=3.0.2'
    ],
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='sample setuptools development',
    python_requires='>=3.10',
    project_urls={
        'Documentation': 'https://yourpackage.example.com/docs',
    },
    include_package_data=True,
    package_data={
        'sample': ['cryptage/profile/default.json', 'cryptage/profile/default2.json', 'quality/.flake8'],
    },
    scripts=['make_docs.sh', 'quality/quality.sh', 'UML/generate_uml.sh']
)
