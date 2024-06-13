#!/bin/bash

sphinx-apidoc -o ../docs/source/ ../.
sphinx-build -M html ../docs/source/ ../docs/build/html/

echo "Génération de la documentation terminée"