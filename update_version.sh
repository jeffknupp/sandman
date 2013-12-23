git flow release start v$1
sed -i -e "s/__version__ = '.*'/__version__ = '$1'/g" sandman/__init__.py
rm -rf docs/generated
python setup.py develop
make docs
git commit docs sandman/__init__.py -m "Update to version v$1"
git flow release finish v$1
python setup.py sdist upload -r pypi
python setup.py upload_docs -r pypi
