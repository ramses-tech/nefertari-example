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

## URL parameters
| url parameter | description |
|---------------|-------------|
| `_m=<method>` | to force an http method using GET, e.g. _m=POST |
| `q=<keywords>` | to filter an ElasticSearch collection using 'keyword ((AND|OR) more_keyword)' syntax |
| `_fields=<field_list>` | to display only specific fields, use - before field names to exclude those fields, e.g. `_fields=-descripton` |
| `_search_fields=<field_list>` | use with `?q=<keywords>` to restrict search to specific fields |
| `_limit=<n>` | to limit the returned collection to n results (default is 20, max limit is 100 for unauthenticated users) |
| `_sort=<field>` | to sort collection by `<field>` |
| `_start=<n>` | to start collection from the `<n>`th resource |
| `_page=<n>` | to start collection at page `<n>` (n * _limit) |

## Add mock data
```
$ nefertari.post2api -f ./mock/Users.json -u http://localhost:6543/api/users
$ nefertari.post2api -f ./mock/Profiles.json -u http://localhost:6543/api/users/{username}/profile
$ nefertari.post2api -f ./mock/Stories.json -u http://localhost:6543/api/stories
```
NOTE: set auth = false in local.ini file before executing
