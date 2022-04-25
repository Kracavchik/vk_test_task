##Contacts API

### Description:
This API allows you to create and manage address book.

### How to run:
* #### Create venv and install requirements
Unix/MacOS
```
    python3 -m venv env
    source env/bin/activate - for Unix or MacOS
    pip install -r requirements
```
Windows
```
    py -m venv env
    .\env\Scripts\activate
    py -m pip install -r requirements
```
* Start flask app

Unix/MacOS
```
    python3 main.py 
```
Windows
```
    py main.py 
```

* Run as docker container
```
    docker build -t contacts_api .
    docker run -dp 5001:5000 contacts_api
```