#!/bin/sh

cd $(dirname "$(readlink -f "$0")")
cd ..
mkdir public_html

rsync -avh --exclude ".gitignore" --exclude "template_project" docs/homepage/. public_html
mkdir -p public_html/assets/arch/
rsync -avh --exclude ".gitignore" docs/arch/artifacts public_html/assets/arch
mkdir -p public_html/assets/requirements/
rsync -avh --exclude ".gitignore" docs/requirements/artifacts public_html/assets/requirements

cd docs/homepage/
zip -r ../../public_html/assets/template_project.zip template_project
cd -

ls -lR public_html/

# cd public_html
# bundle exec jekyll build && bundle htmlproofer ./_site
# bundle exec jekyll serve

