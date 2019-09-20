# python-lcs-client
a client for using lcs inteded for server side python
the general idea is for this to be used with a json based web api
for every request to your api you would ask for an email and lcs token

alternatively you could have your own tokens, and have the user pass
the password again to you but this will be annoying if they already
logged into the normal frontend

## documentation
 - [documentation for this client](lcs_client.md)
 - [documentation for lcs](https://github.com/hackru/lcs/wiki)

## development setup
```bash
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements
```
## generating documentation
```bash
# do local setup
python -m pydocmd build
cp _build/pydocmd/lcs_client.md .
# check it out before you push
python -m pydocmd server
```

## running the example web application
```bash
# do local setup
pip install -r example_requirements.txt
python example_api.py
```

## release on pypi
```bash
#do local setup
pip install setuptools twine
python setup.py sdist
twine upload dist/<version>.tar.gz
```