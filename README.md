## Python plagiarism
A python package to detect plagiarism in document

#### Requirements
* Python == 3.8
* scikit-learn

### Installation, run and testing

Using pip

```
pip install git+https://github.com/u2rafi/python-plagiarism.git
```

Using source

```
git clone https://github.com/u2rafi/python-plagiarism.git
cd python-plagiarism
python setup.py install
```

#### Using plagiarism as a package
```
>>> from plagiarism.core import Plagiarism
>>> plg = Plagiarism(source=...)
# get similarity percentage in number (float)
>>> plg.compare(...).get() 
# matching with dataset (multiple files)
>>> plg.compare(...).getlist()  
```

### Running web application

#### Run locally 
```
python -m plagiarism.cli runserver -h 0.0.0.0 -p 5000
```

#### Docker and docker compose

```
# docker 
cd python-plagiarism
docker build -t plagiarism .
docker run -p 5000:5000 plagiarism:latest

# docker compose
docker-compose up -d --build
```

#### Kubernetes
```
kubectl apply -f kubernetes-deployment.yml -n default
```

#### Using commandline
```
plagiarize compare --file test_input.txt
plagiarize runserver
```

### Testing

Test cases are in `.tests` directory

#### Test using pytest

```
python3 -m pytest tests
```

#### With cov
```
pytest --cov=plagiarism .
```

# python-plagiarism app deployed in heroku
A python-plagiarism app has been deployed in heroku docker and can be accessed using this link

[https://python-plagiarism.herokuapp.com/](https://python-plagiarism.herokuapp.com/)