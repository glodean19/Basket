
from django.db import models

# this class correspond to the table Product in the database.
# Table's attributes are product_id, product_name and price
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    # returns a human-readable representation of the model
    def __str__(self):
        return self.product_name
