#!/bin/sh

cd $(dirname "$(readlink -f "$0")")
cd ..
mkdir public_html

cp -r docs/homepage/. public_html
mkdir -p public_html/assets/arch/
cp -r docs/arch/artifacts public_html/assets/arch
mkdir -p public_html/assets/requirements/
cp -r docs/requirements/artifacts public_html/assets/requirements
# ls -lR public_html/

# cd public_html
# bundle exec jekyll build && bundle htmlproofer ./_site
# bundle exec jekyll serve

