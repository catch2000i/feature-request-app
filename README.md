# feature-request-app
Project created using Ubuntu, Python, Flask, Sql-Alchemy, KnockoutJS, Bootstrap

This is simple demo project of feature request web UI.

Application consists of two parts: server side which includes Flask web server, mariadb, and server app which uses sqlalchemy for db operations, and webapp based on knockout.js and styled with bootstrap 3.

The whole project is deployed as a docker image.

The build process requires two steps:
- build.sh (or build.bat for windows platform) creates base docker image from ubuntu 18.04; it contains all necessary software to run the server including mariadb, though in real production environment database would be placed in a separate VM (or container)
- run.sh (run.bat) creates a final app image which is a layer on top of base image and includes all python files, html templates, css and javascript files; it also starts the container

Application listens on port 5000.
Starting URL is /demo.html
Application has been deployed on digitalocean droplet and can be accessed at http://157.230.186.213:5000/demo.html


Notes:
1. Paging has not been implemented
2. There is no security (no authentication, no authorization)
3. Changing priorities function uses python process lock which works only for one process and obviously will not work in production environment. Possible solutions would be to implement the journal which insert new record each time when priority for the record at the future table increased or use database-wide locking/transactions.
