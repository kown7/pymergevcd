#!/bin/sh

cd $(dirname "$(readlink -f "$0")")
cd ..
mkdir public_html

cp -r docs/homepage/. public_html
rm -rf public_html/template_project  # remove again
mkdir -p public_html/assets/arch/
cp -r docs/arch/artifacts public_html/assets/arch
mkdir -p public_html/assets/requirements/
cp -r docs/requirements/artifacts public_html/assets/requirements

cd docs/homepage/
zip -r ../../public_html/assets/template_project.zip template_project
cd -
# ls -lR public_html/

# cd public_html
# bundle exec jekyll build && bundle htmlproofer ./_site
# bundle exec jekyll serve

