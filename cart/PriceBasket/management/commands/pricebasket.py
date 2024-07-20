'''
Some references

For creating custom commands: https://docs.djangoproject.com/en/5.0/howto/custom-management-commands/
https://simpleisbetterthancomplex.com/tutorial/2018/08/27/how-to-create-custom-django-management-commands.html
https://dev.to/doridoro/create-a-custom-basecommand-for-a-django-app-38k0

For a shopping cart: https://medium.com/@ayoubennaoui20/building-a-shopping-cart-in-django-a-step-by-step-guide-d696439ec6e5
https://reintech.io/blog/building-a-shopping-cart-in-django
'''

from django.core.management.base import BaseCommand, CommandError
from PriceBasket.models import *
from decimal import Decimal

# create a new class and inherit from BaseCommand
class Command(BaseCommand):
    # display the help text when calling python manage.py help
    help = 'Items price and special offers'

    # define the arguments that the command will accept
    def add_arguments(self, parser):
        # Name of the argument is "items_quantities". "nargs='+'" means that one or more arguments are expected.
        # The accepted type is string.
        parser.add_argument('items_quantities', nargs='+', type=str)

    def handle(self, *args, **options):
        try:
            # retrieve the command line argument 'items_quantities'
            items_quantities = options['items_quantities']
            # If the length of items_quantities is odd, it raises an error because each item must have a corresponding quantity. 
            # An odd number of elements would imply that there is at least one item without a quantity or vice versa.
            if len(items_quantities) % 2 != 0:
                raise CommandError("Each item must have a corresponding quantity.")
            # it uses slicing the item, starting at index 0 and taking every second element
            items = items_quantities[0::2]
            # it uses slicing starting at index 1 and taking every second element. 
            # The map fuction converts to int each element in the sliced list
            quantities = list(map(int, items_quantities[1::2]))

            # call the method create_basket to create a list of tuples with the item and the quantity
            basket = self.create_basket(items, quantities)

            # call the method to calculate the subtotal with the items and the quantity in the basket
            subtotal = self.calculate_subtotal(basket)

            # call the method to apply offers and calculate the discount
            offers, discounts = self.apply_offers(basket)

            # interpreter’s standard output (only for string data format)
            self.stdout.write(f"Subtotal: £{subtotal:.2f}")
            
            #if there are offers, it iterates through them. it returns the offer if applied
            if offers:
                for offer in offers:
                    # interpreter’s standard output (only for string data format)
                    self.stdout.write(offer)
            else:
                # interpreter’s standard output (only for string data format)
                self.stdout.write("(no offers available)")
            # calculate the total amount with the applied offers
            total = subtotal - discounts

            # interpreter’s standard output (only for string data format)
            self.stdout.write(f"Total: £{total:.2f}")

        # this will catch any logic or format error
        except Exception as e:
            raise CommandError(f"An unexpected error occurred: {str(e)}")

    def create_basket(self, items, quantities):
        # the basket is initialised as an empty list and 
        # it will store the tuple of products and quantities
        basket = []
        # it iterates over the items and the quantities. 
        # it creates pairs of each items with the corresponding quantity as a 2 input list
        for item_name, quantity in zip(items, quantities):
            try:
                # fetch the product object from the database based on the item
                product = Product.objects.get(product_name=item_name)
            # raise an error if the product doesn't exist in the database
            except Product.DoesNotExist:
                raise CommandError(f"Product '{item_name}' does not exist.")
            # append to the basket empty list the object and the quantity
            basket.append((product, quantity))
        # return the basket list with the tuple
        return basket

    def calculate_subtotal(self, basket):
        # set subtotal as decimal
        subtotal = Decimal('0.00')
        # iteration through each product and quantity in the basket.
        # it calculates the price by the quantity and add it to the subtotal
        for product, quantity in basket:
            subtotal += product.price * quantity
        return subtotal

    def apply_offers(self, basket):
        # empty list where the applied offers will be appended
        offers = []
        # applied discounts
        discounts = Decimal('0.00')
        apple_discount = Decimal('0.00')
        # count number of soup cans and bread loaf
        soup_count = 0
        bread_count = 0
        # initialise the bread price as Decimal
        bread_price = Decimal('0.00')

        # iterating through all the products in the basket
        for product, quantity in basket:
            # if the products are apples
            if product.product_name == 'Apples':
                # it calculates the 10% discount on the price by the quantity
                apple_discount += (product.price * Decimal('0.10')) * quantity
                # append the discount to the offer list
                offers.append(f"Apples 10% off: £{apple_discount:.2f}")
                # add the apple discount to the discounts
                discounts += apple_discount

            # if the product is soup
            elif product.product_name == 'Soup':
                # it adds the quantity of the soup to the soup counter
                soup_count += quantity
            # if the product is bread
            elif product.product_name == 'Bread':
                # it counts the amount of loaves and retrieve the price
                bread_count += quantity
                bread_price = product.price
 

        # Bread offer is applied only if the can of soup are greater or equal 2 and there is bread in the basket
        if soup_count >= 2 and bread_count > 0:
            # it calculates the number of times the offer can be applied
            # it uses the // floor operation (rounded to the next smallest integer)
            # the offer_count is the smallest value between the number of elegible
            # pairs of soup cans and the number of bread loaves
            offer_count = min(soup_count // 2, bread_count) 
            # bread half price multipled by the number of pair cans
            bread_discount = (bread_price / 2) * offer_count
            # the offer is appended to the empty list
            offers.append(f"Bread half price: £{bread_discount:.2f}")
            # it updates the discounts with the bread discount
            discounts += bread_discount

        # returns offers and discounts when the method is called
        return offers, discounts
        