# `nefertari-example`
This is an example RESTful API project using:
- [Pyramid](https://github.com/Pylons/pyramid) as the web framework
- [Nefertari](https://github.com/ramses-tech/nefertari) as the REST framework
- [ElasticSearch](https://www.elastic.co/downloads/elasticsearch) for reads
- and either [Postgres](http://www.postgresql.org/download/) or [MongoDB](http://www.mongodb.org/downloads) for writes

## Installation
```
$ pip install -r requirements.txt
$ cp local.ini.template local.ini
$ nano local.ini
```
The setting `nefertari.engine` in local.ini can be set to either `nefertari_mongodb` or `nefertari_sqla`

## Run
```
$ pserve local.ini
```

### Endpoints
| uri | method(s) | description |
|-----|-----------|-------------|
| `/api/login` | POST | login w/ username, password |
| `/api/logout` | GET | logout |
| `/api/account` | POST | signup (then login) w/ username, email, password |
| `/api/users` | GET, POST, PATCH, DELETE | all users |
| `/api/users/self` | GET | currently logged-in user |
| `/api/stories` | GET, POST, PATCH, DELETE | all stories (returns only 100 records to guest users if auth = true) |
| `/api/s` | GET | endpoint dedicated to search (use with the `?q=` parameter) |

For development purposes, you can use the `_m` parameter to tunnel methods through GET in a browser.
E.g.
```
<host>/api/account?_m=POST&username=<username>&email=<email>&password=<password>
<host>/api/login?_m=POST&login=<username_or_email>&password=<password>
```

### Adding mock data
NOTE: set auth = false in local.ini file before executing
```
$ nefertari.post2api -f ./mock/Users.json -u http://localhost:6543/api/users
$ nefertari.post2api -f ./mock/Profiles.json -u http://localhost:6543/api/users/{username}/profile
$ nefertari.post2api -f ./mock/Stories.json -u http://localhost:6543/api/stories
```

