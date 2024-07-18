## Django Groceries Challenge - an API backend platform for an online shop

### Technology Stack
[![workflow](https://github.com/StanislavBerezovskii/django_groceries_challenge/actions/workflows/main.yml/badge.svg)
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)
[![DRF Spectacular](https://img.shields.io/badge/-DRF%20Spectacular-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=008080)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=56C0C0&color=008080)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=56C0C0&color=008080)](https://gunicorn.org/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/products/docker-hub)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat&logo=GitHub%20actions&logoColor=56C0C0&color=008080)](https://github.com/features/actions)

The Django Groceries Challenge project is a backend API platform for an online shop with a postgresSQL database and
DRF-Spectacular based documentation.The platform is capable of:
- Creating, editing, and deleting categories and subcategories of products in the admin panel.
- Categories and subcategories have a name, slug name, and an image.
- Subcategories are linked to their parent category.
- An endpoint is implemented to view all categories with subcategories, with pagination provided.
- There is a possibility to add, edit, and delete products in the admin panel.
- Products belong to a specific subcategory and, accordingly, a category, and have a name, slug name, images in three sizes, and a price.
- An endpoint is implemented to display products with pagination. Each product in the output has the following fields: name, slug, category, subcategory, price, and a list of images.
- An endpoint for adding, updating (changing quantity), and deleting a product in the cart is implemented.
- An endpoint to display the contents of the cart with the calculation of the number of items and the total cost of items in the cart is implemented.
- There is the ability to completely clear the cart.
- Operations on the category and product endpoints can be performed by any user.
- Operations on the cart endpoints can only be performed by an authorized user and only with their own cart.
- Token-based authorization is implemented.

### Technologies used:
- Python               3.11
- Django               5.0.7
- djangorestframework  3.15.2
- Pillow               10.4.0

### Deploying the project locally:
1.Clone the project and deploy a virtual environment:
```
py -3.11 -m venv venv
```    
2. Activate the virtual environment:
```
. venv/Scripts/activate
```

3. Update the pip package manager:
```
py -m pip install --upgrade pip
```
4. Install dependencies from requirements.txt into the virtual environment:
```
pip install -r backend/requirements.txt
```
5. Run migrations:
```
py backend/manage.py migrate
```
6. Create a superuser:
```
python backend/manage.py createsuperuser
```
7. Run the project:
```
py backend/manage.py runserver
```

### Workflow tasks:

* tests - Checks the code for PEP8 compliance (uses flake8 package). Use setup.cfg to adjust the scope of testing. Further steps will only be executed if the push was to the master branch.
* build_and_push_to_docker_hub - Builds and uploads a docker image of the backend django project module to Docker Hub
* deploy - Automaticly deploys the project to the production server. Files are copied from the Docker Hub repository to the server
* send_message - Sends a notification via Telegram bot about the successful deployment of the project on the production server

### Preparation for running the workflow:

1. Clone the project and deploy a virtual environment:
```
py -3.11 -m venv venv
```    
2. Activate the virtual environment:
```
. venv/Scripts/activate
```

3. Update the pip package manager:
```
py -m pip install --upgrade pip
```    
4. Install dependencies from requirements.txt into the virtual environment:
```
pip install -r backend/requirements.txt
```
5. Edit the `nginx.conf` file and enter the IP of the virtual machine (server) in the `server_name` line,
    and copy the prepared `docker-compose.yml` and `nginx.conf` files from the local project to the home directory of the server:
```
scp ./infra/docker-compose.yml <username>@<host>:
scp ./infra/nginx.conf <username>@<host>:
```

6. In the Github repository, add the following data to `Settings - Secrets - Actions secrets`:

```
BOT_TOKEN - token of the TG bot you wish to use (you can use 5542550097:AAEvLPtl01dBQN6xqX4K3OwhqMQy0ocww0U for testing)
DB_ENGINE - django.db.backends.postgresql
DB_HOST - db by default
POSTGRES_DB - name of yor database (postgres by default)
DB_PORT - 5432 by default
DOCKER_PASSWORD - DockerHub user password
DOCKER_USERNAME - DockerHub username
HOST - your server ip address
PASSPHRASE - passphrase for your ssh key (if created)
POSTGRES_PASSWORD - postgres by default
POSTGRES_USER - postgres by default
SECRET_KEY - django app secret key (try to avoid brackets if possible as they clash with Actions Secrets)
SSH_KEY - private ssh key from your LOCAL pc (one that has access to the deploy server), public one must be declared to the server
TELEGRAM_TO - id of your telegram account (you can get it from @userinfobot, command /start)
USER - your username on the deploy server
```

### Launching a project on the deploy server:

1. Login to the deploy server and install Docker and Docker-compose:
```
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo apt install docker-compose
```

2. Check that Docker-Compose is installed correctly:
```
sudo  docker-compose --version
```

### Make a push to your repository main branch and wait for the deployment workflow to complete. Make sure the system is working correctly:

1. Create a superuser by logging in on the production server:
```
sudo docker-compose exec web python manage.py createsuperuser
```

### Project developer
```
Stanislav Berezovskii
```

### Project URLs:

```
http://<ip-address>/admin/ - Access to the bot admin panel
http://<ip-address>/api/ - API access to news objects in .json format
http://<ip-address>/api/docs/ - API access to the documentation
http://<ip-address>/api/docs/swagger/ - DRF-Spectacular generated interactive project documentation
```