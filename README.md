### How to run the project

`docker-compose up`

### How to run the tests:

`docker exec -it messaging-web-1 python3 -m pytest`

### Notes, limitations and design alternatives

- The 5 user stories were implemented. Endpoints that create data are accessible via POST, and the ones that retrieve data are accessible via GET.
- The tests exercise the endpoints with the current database, in a production environment those tests should run against a different database (test db).
- There is no authentication layer, but a header is used as the id for the impersonating user.
- In a production environment, the DB configuration/credentials will need to be injected via a combinatino of hypervisor with a secrets management system.
- If the "messages" table needs to scale an alternative design based on a key-value database (like DynamoDB) could be explored, as it can scale horizontally with more ease.
- The database schema may need to be generated as part of a build process, and tables should not be created by the web app.
- The database container might be fine for testing or for a development environment, but in the real world a stateful service may need to be set up with a Cloud API, or some other way of provisioning PostgreSQL.
- In a production environment, the application might need to run under a WSGI server like Gunicorn, and not through Flask itself.
- Development dependencies (such as those required to run tests) can be separated from `requirements.txt`. For simplicity all of them were bundled together.
