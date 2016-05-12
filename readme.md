# Accio
Automatic deployments :rocket: [![Build status][build-badge]][build-link]

![Screenshot][screenshot]

## Install
```bash
pip install -Ur requirements.txt
npm install --production # drop --production if you are not deploying
```

## Running accio
### Production
See [docs/production](docs/production.md) for details on how to run it in
production. Also see [docs/configuration](docs/configuration.md) on how to
configure.

### Development
Start backend and frontend with these commands and head to [localhost:3000](http://localhost:3000).
```bash
python manage.py runserver
npm start
```

If you want to to test queues you need to start celery. However, be aware
that tasks are run synchronously in development unless configured otherwise.

[build-link]: https://ci.frigg.io/relekang/accio
[build-badge]: https://ci.frigg.io/relekang/accio.svg
[screenshot]: docs/screenshot.png
