import factory
from PriceBasket.models import Product

# the factory class ProductFactory is a subclass of DjangoModelFactory from the factory_boy library
class ProductFactory(factory.django.DjangoModelFactory):
    # the product name is a sequence where the lamba function creates the product name and appends 
    # the sequence number 'n' to the string 'Product'
    product_name = factory.Sequence(lambda n: f'Product {n}')
    # it uses the faker library to generate fake data. it specifies the data are decimal,
    # with 2 digits to the left and 2 digits to the right and the number are positive
    price = factory.Faker('pydecimal', left_digits=2, right_digits=2, positive=True)
    # this specifies the model. when the factory creates the instance is for the 'Product' model
    class Meta:
        model = Product

