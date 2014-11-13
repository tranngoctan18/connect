# Connect

Connect is a moderated platform that help individuals connect with each other based on location, skills and interests.

##  Demo

http://kabu-connect.herokuapp.com/

[ ![Codeship Status for nlh/connect](https://codeship.io/projects/86e14520-1ec8-0132-5410-3e0b0834453b/status)](https://codeship.io/projects/35570)

## Installation:

### Ubuntu:

```bash
sudo apt-get install libyaml-dev
sudo pip install virtualenv-wrapper
mkvirtualenv --python=/bin/python3 connect
pip install -r requirements/dev.txt
```

### Fedora:

```bash
sudo yum install libyaml-devel
sudo pip install virtualenv-wrapper
mkvirtualenv --python=/bin/python3 connect
pip install -r requirements/dev.txt
```

## Setting up connect for your group or organisation

### Site settings:

Configure the following in `connect/settings.py`:

- `SITE_ID`
- `SITE_URL`
- `SITE_EMAIL`
- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `EMAIL_USE_TLS`

### Setting up the DB / Django Admin

```bash
python manage.py migrate
python manage.py loaddata accounts/fixtures/group_perms.yaml
```

#### Brands

#### Roles

#### Skills

#### Users

#### Flat Pages

#### Sites


### Customising colours

Connect is built with [Sass](http://sass-lang.com/). You can change the default pink highlight
color by editing the `$highlight` variable at the top of `_site_settings.scss`


## Misc.

### Font Awesome

Connect is currently integrated with [Font Awesome](https://fortawesome.github.io/Font-Awesome/) (v4.0.3)
