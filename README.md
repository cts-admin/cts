# About

[![Build Status](https://travis-ci.org/cts-admin/cts.svg?branch=master)](https://travis-ci.org/cts-admin/cts)
[![Coverage Status](https://coveralls.io/repos/github/cts-admin/cts/badge.svg?branch=master)](https://coveralls.io/github/cts-admin/cts?branch=master)
[<img src="https://img.shields.io/badge/built%20with-Python3-brightgreen.svg">](https://docs.python.org/3.5/)

This project is being developed to support the 501(c)(3) nonprofit Conservation Technology Solutions Inc.

CTS aims to make life easier for anyone involved in environmental conservation work. We’ve made it our goal to leverage 
the power of existing technologies as well as develop our own. From web apps, to DIY hardware-based citizen science 
projects, we have a lot of ideas for how we can move towards a more environmentally conscious future.

### So what is this repo?

This repository houses CTS's website which also includes web applications and tools that we hope can be of use to
others. Tools built for use outside of the web environment will be hosted in their own repositories. We'll talk more
about any such tools on our [blog](https://conservationtechnologysolutions.org/cts-blog) and
[twitter account](https://twitter.com/ctsadmin).

Our latest project can be found under the 'plant-tracker' branch. There we'd like to develop a mapping web application
which targets those involved in native seed collection. The aim will be to help track and prioritize both seed
collections themselves as well as conservation of the land from which the seed sources derived by correlating seed
collection locations with their underlying 
[Provisional Seed Zones](https://www.fs.fed.us/wwetac/threat-map/TRMSeedZoneMapper.php).

# Get Involved

Check out our website at [conservationtechnologysolutions.org](https://conservationtechnologysolutions.org)
where you can find our blog to learn a bit more about what we're trying to do.

Please also follow us on twitter [@ctsadmin](https://twitter.com/ctsadmin) for updates and general news about natural
resource conservation. You can also find us [on Facebook](https://www.facebook.com/ConservationTechnologySolutions/)!
Feel free to reach out with any questions or comments; we'd love to hear from you!

## Deployment

Follow these steps for deploying locally:


1. First, you'll need to [install Docker](https://docs.docker.com/engine/installation/) and 
[Docker Compose](https://docs.docker.com/compose/install/)

2. Change into the root web application directory:
    ```bash
    $ cd cts/
    ```

3. Customize environment variables
    1. Review the included example*.env files in the ```cts/``` directory.
    2. Modify as needed.
    3. The ```cts/cts/docker-compose.yml``` file expects to find the database ```.env``` file at 
    ```/opt/db_secrets.env```, the RabbitMQ credential file at ```/opt/rabbit_secrets.env``` and the django ```.env``` 
    file at ```/opt/django_secrets.env```. You can either:
        * Place each respective ```.env``` in your ```/opt``` directory. Or...
        * Modify the three occurrences of ```env_file:``` in ```cts/docker-compose.yml``` to point to your customized 
        ```.env``` files.
        * Note that values should be consistent across the three files. For example, the password listed under 
        ```PG_PASS``` in ```db_secrets.env``` should be the same password listed under ```PG_PASS``` in
        ```django_secrets.env```.

4. Create a super user
    ```bash
    $ docker-compose run web python manage.py createsuperuser
    ```

5. Start the app with docker-compose:
    ```bash
    $ docker-compose up
    ```

You should now be able to navigate to [http://0.0.0.0:8000](http://127.0.0.1:8000) to view the web server. Nginx is
configured with basic auth, but for local testing you can use the following credentials:

username: `testuser`
password: `testpassword`

# License

This software is distributed under the terms of the GNU General Public License v3.0.