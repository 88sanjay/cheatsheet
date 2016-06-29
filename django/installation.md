# Installing and configuring django based rest services

http://www.django-rest-framework.org/

# Install django
pip install django
pip install djangorestframework
pip install markdown       # Markdown support for the browsable API.
pip install django-filter  # Filtering support


# Create the project directory
mkdir proj
cd proj

# Create a virtualenv to isolate our package dependencies locally
virtualenv env
source env/bin/activate  # On Windows use `env\Scripts\activate`

# Install Django and Django REST framework into the virtualenv
pip install django
pip install djangorestframework

# Set up a new project with a single application


django-admin.py startproject website .  
cd website
python manage.py startapp app


# Define Models in models.py in app dir

# Make change list to migrate to DB using 

python manage.py makemigrations app

# Migrate all changes to reflect in DB 

python manage.py migrate

## You can add objects to bd from python shell 

python manage.py shell

b = Album(artist="artist 2",album_title="albim title 2",genre="genre 2",album_logo="https://2.bp.blogspot.com/-Gh9Drj62EFw/VeXMk3xcsOI/AAAAAAAAAxw/knYsAcpaABo/s1600/OGB-INSIDER-BLOGS-GoogleLogox2-Animated.gif")

b.save()



