# `nefertari-example`
This is an example RESTful API project using:
- [Pyramid](https://github.com/Pylons/pyramid) as the web framework
- [Nefertari](https://github.com/brandicted/nefertari) as the REST framework
- [ElasticSearch](https://www.elastic.co/downloads/elasticsearch) for reads
- and either [Postgres](http://www.postgresql.org/download/) or [MongoDB](http://www.mongodb.org/downloads) for writes

## Installation
```
$ pip install -r requirements.txt
$ cp local.ini.template local.ini
$ nano local.ini
```
The setting `nefertari.engine` can be set to either `nefertari_mongodb` or `nefertari_sqla`

## Run
```
$ pserve local.ini
```

## Login
POST `<host>/api/login`
```json
{
    "login": "<config.system.user>",
    "password": "<config.system.password>"
}
```

or in the browser:
```
<host>/api/login?_m=POST&login=<config.system.user>&password=<config.system.password>
```

## Endpoints
| uri | description |
|-----|-------------|
| `/api/login` | login |
| `/api/logout` | logout |
| `/api/users` | all users |
| `/api/users/self` | currently logged-in user |
| `/api/stories` | all stories (first 100 records availble to guest users) |
| `/api/s` | ES endpoint dedicated to search (use with the `?q=` parameter) |
| `/api/account?_m=POST&email=<email>&password=<password>` | to create a user and login right away |
| `/api/admin/settings` | to view/edit settings at runtime (requires admin permissions or auth=false) |
| `/api/admin/loglevels/<logger_key>` | to view/edit loglevels at runtime (requires admin permissions or auth=false) |

## Add mock data
```
$ nefertari.post2api -f ./mock/Users.json -u http://localhost:6543/api/users
$ nefertari.post2api -f ./mock/Profiles.json -u http://localhost:6543/api/users/{username}/profile
$ nefertari.post2api -f ./mock/Stories.json -u http://localhost:6543/api/stories
```
NOTE: set auth = false in local.ini file before executing
