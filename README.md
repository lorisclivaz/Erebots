# Profiles Demo

## Local Development

Following tools must be installed on your system:
- git
- [docker](https://docs.docker.com/install/)
- [docker-compose](https://docs.docker.com/compose/install/)
- any Python IDE (for example [Pycharm](https://www.jetbrains.com/pycharm/) or [Visual Studio Code](https://code.visualstudio.com/))


1. Clone repository.
2. To start the XMPP server, in your cloned repository run:
```bash
docker-compose up --detach prosody_server
```
3. Since the deployment uses environment variables, make sure to set and use the variable 'LOCAL' to store the domain identified of the XMPP jid (e.g. `romeo@LOCAL`). During development, you can simply use `localhost` as there is already a virtualhost specified and a ssl certificate added in the config.
4. An example how to dockerize Spade can be found in the folder `spade`.
4. Code away!

## Deployment

1. Clone repository.
2. To retrieve the current SSL certificate and private key, run the extract_certs.sh script in /srv/traefik/ and move both certificate and key into the folder `containers/prosody/config/certs/`.
3. Change the file permissions of the folder `containers/prosody/config` to `777`.
4. Make sure to specify environment variables in the file `deployment.env`.
5. Store all docker secrets in the folder `secrets/` (e.g. database passwords etc.) and specify them in `docker-compose.yml`.

## TODOs
- [ ] ...

## Links

- [Spade Tutorials](https://spade-mas.readthedocs.io/en/latest/usage.html)
- [MongoDB Full Stack Tutorials](https://www.fullstackpython.com/mongodb.html)
- [Prosody Default Config](https://github.com/joschi/docker-prosody-alpine/blob/master/prosody.cfg.lua)
- [Retrieve Certificates from acme.json](https://stackoverflow.com/questions/47218529/store-traefik-lets-encrypt-certificates-not-as-json)
