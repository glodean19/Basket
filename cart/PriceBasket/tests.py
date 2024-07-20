'''
Some references

For the factory boy library: https://factoryboy.readthedocs.io/en/stable/recipes.html
https://medium.com/analytics-vidhya/factoryboy-usage-cd0398fd11d2

For the run_command function:
https://docs.djangoproject.com/en/5.0/topics/testing/tools/#topics-testing-management-commands
https://www.geeksforgeeks.org/stringio-module-in-python/
'''

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from decimal import Decimal
from io import StringIO
from .model_factories import ProductFactory

class PriceBasketCommandTest(TestCase):
    def setUp(self):
        # these are the factory instances for each product with prices
        ProductFactory(product_name='Soup', price=Decimal('0.65'))
        ProductFactory(product_name='Bread', price=Decimal('0.80'))
        ProductFactory(product_name='Apples', price=Decimal('1.00'))
        ProductFactory(product_name='Milk', price=Decimal('1.30'))

    # helper method to run the 'pricebasket' command with the specified arguments and captures the output.
    def run_command(self, *args):
        # in-memmory file-like object
        out = StringIO()
        call_command('pricebasket', *args, stdout=out)
        return out.getvalue()
    
    # this test checks that the command handles a basket with items 
    # that have no offers
    def test_pricebasket_command_no_offers(self):
        out = self.run_command('Bread', '1', 'Milk', '3')
        self.assertIn("Subtotal: £4.70", out)
        self.assertIn("(no offers available)", out)
        self.assertIn("Total: £4.70", out)

    # this test is to check the application of the apple discount
    def test_pricebasket_command_with_apple_offer(self):
        out = self.run_command('Apples', '3')
        self.assertIn("Subtotal: £3.00", out)
        self.assertIn("Apples 10% off: £0.30", out)
        self.assertIn("Total: £2.70", out)

    # this test checks the application of the soup and bread offer
    def test_pricebasket_command_with_soup_and_bread_offer(self):
        out = self.run_command('Soup', '4', 'Bread', '1')
        self.assertIn("Subtotal: £3.40", out)
        self.assertIn("Bread half price: £0.40", out)
        self.assertIn("Total: £3.00", out)

    # this test checks the application of multiple offers
    def test_pricebasket_command_with_multiple_offers(self):
        out = self.run_command('Soup', '4', 'Bread', '1', 'Apples', '3')
        self.assertIn("Subtotal: £6.40", out)
        self.assertIn("Apples 10% off: £0.30", out)
        self.assertIn("Bread half price: £0.40", out)
        self.assertIn("Total: £5.70", out)

    # this test checks the scenario where there is only one bread in the basket, 
    # despite having enough soup for more than one offer
    def test_pricebasket_command_insufficient_bread(self):
        out = self.run_command('Soup', '4', 'Bread', '1')
        self.assertIn("Subtotal: £3.40", out)
        self.assertIn("Bread half price: £0.40", out)
        self.assertIn("Total: £3.00", out)

    # this test checks the scenario where there is not enough soup for the bread discount offer
    def test_pricebasket_command_insufficient_soup_for_offer(self):
        out = self.run_command('Soup', '1', 'Bread', '1')
        self.assertIn("Subtotal: £1.45", out)
        self.assertIn("(no offers available)", out)
        self.assertIn("Total: £1.45", out)

    # This test checks that the command raises an error when given an item without a corresponding quantity
    def test_pricebasket_command_odd_number_of_arguments(self):
        with self.assertRaises(CommandError) as cm:
            self.run_command('Soup', '2', 'Bread')
        self.assertEqual(str(cm.exception), "Each item must have a corresponding quantity.")

    
