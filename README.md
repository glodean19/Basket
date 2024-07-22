
django-cart


This app calculates the total price for a basket of items, applying special offers and discount where applicable.



Quick-start


1. Clone the repository
   git clone https://github.com/<username>/<forked-repo>.git

2. create your own virtual environment and activate it
   python3 -m venv venv
   source venv/bin/activate

3. install the requirement.txt
   pip install -r requirements.txt

4. create the database
   python manage.py makemigrations
   python manage.py migrate

5. Run the command line
   python manage.py pricebasket <item 1> <quantity> <item 2> <quantity> <item 3> <quantity> <item 4> <quantity>

6. For testing run the command line
   python manage.py test



More details


Step for creating the Django project. (virtualenvwrapper already installed)

1. Created virtual environment bc_interview
     mkvirtualenv -p /usr/bin/python3 bc_interview

2. Activate the virtual environment
    workon bc_interview

3. Install Django framework in the virtual environment 
   pip install django

4. Created the Django project cart
   django-admin startproject cart

5. Created the app PriceBasket in the Django project and add it to the settings
   python manage.py startapp PriceBasket

6. Created Product model in the models.py

7. Migrated the model to the database
   python manage.py makemigrations
   python manage.py migrate

8. Created fixtures with goods.json file
   python manage.py loaddata goods.json

9. Created superuser
      username: admin
      email: admin@test.com
      password: pass-admin

10. Created admin class based on the model. 

11. The database can be also accessed via the Django admin at http://127.0.0.1:8000/admin/
    python manage.py runserver

11. Created pricebasket.py file
   python manage.py pricebasket <item 1> <quantity> <item 2> <quantity> <item 3> <quantity> <item 4> <quantity>
   example: python manage.py pricebasket Soup 4 Apples 2 Milk 1 Bread 2

12. Unittest with Factory Boy
    pip install factory_boy
    run test: python manage.py test

13. List of packages needed to run the app
    pip freeze > requirements.txt
