#!/bin/bash

# effacer le fichier zip précédent
file_pattern="bdd_Onche_*.zip"

# Check if a file matching the pattern exists
rm -rf $2BDD/export/*.zip

timestamp=$(date +%Y%m%d%H%M%S)
zip $2BDD/export/bdd_$1_$timestamp.zip $2BDD/export/bdd_$1.sql

FILE="$2BDD/export/bdd_$1_$timestamp.zip"

# Track the file with Git LFS
git lfs track "$FILE"

# Add, commit, and push the file
git add "$FILE"
git commit -m "Update de la base de donnée"
git push origin main

rm -rf $2BDD/export/bdd_$1.sql