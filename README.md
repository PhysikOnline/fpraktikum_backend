# Fpraktikum Backend

This project is the Backend Part of the Fpraktikum at the PhysikOnline
platform.

The project is Deployed via [Dokku]( http://dokku.viewdocs.io/dokku/  "Dokku")


The purpose of this project is the implementation of a custom registration
mechanism for the Ilias platform. Our Forntend is produced by this [project](https://github.com/PhysikOnline/fpraktikum_frontend "Fpraktikum Frontend")

## Local Development

For local development we use [docker-compose](https://docs.docker.com/compose/),
with the corresponding Files in the directory `docker/local`. Environment variables
needed, even for development, can be retrieved for the Server and played in a `.env` file.
No worries, the .env file is ignored by GIT.


## Testing

Test can be run via the django builtin test module with the docker-compose run
utility.


## Production/Staging

Both the production and the staging environment are staged with [Dokku]( http://dokku.viewdocs.io/dokku/  "Dokku")
on one of our servers.