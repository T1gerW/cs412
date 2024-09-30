# restaurant/views.py

from django.shortcuts import render
import random
from datetime import datetime, timedelta

# Daily Specials List
DAILY_SPECIALS = {
    "THE FRAYwich": 8,
    "Chicken Alfraydo": 12,
    "Fray's Cheesecake": 6
}

# Menu Items with Options
MENU_ITEMS = {
    "Frayed Chicken": 12,
    "Famous Fray Burger": 9,
    "Veggie Salad": 5,
    "Fray's hotdog": 6,
    "Double Beef Burger": 2  # Price for "Make it double!" option
}


def main(request):
    """View to render the main page with restaurant information."""
    return render(request, 'restaurant/main.html')


def order(request):
    """View to render the online order form."""
    # Choose a random daily special from the list
    daily_special_name = random.choice(list(DAILY_SPECIALS.keys()))
    daily_special_price = DAILY_SPECIALS[daily_special_name]
    
    # Pass the daily special to the context
    context = {
        'daily_special': {'name': daily_special_name, 'price': daily_special_price}
    }
    return render(request, 'restaurant/order.html', context)


def confirmation(request):
    """View to process the submission of an order and display a confirmation page."""
    if request.method == 'POST':
        # Retrieve ordered items and extras from the form
        ordered_items = request.POST.getlist('items')  # Get list of selected menu items
        extras = request.POST.getlist('extras')  # Get list of extra items (e.g., "Make it double!" option)
        
        # List to hold items and their prices for confirmation display
        items_with_prices = []
        total_price = 0



        # Loop through each ordered item and add it to the confirmation list
        for item in ordered_items:
                # Initialize the item's name and price
            if item in MENU_ITEMS:
                formatted_name = item
                price = MENU_ITEMS[item]
                # Handle the special case of "Famous Fray Burger" and its "Double" extra option
                if item == "Famous Fray Burger" and "Double Beef Burger" in extras:
                # Modify the name to show "(double)" and add the extra price
                    formatted_name = f"{item} (double)"
                    price += MENU_ITEMS["Double Beef Burger"]  # Add the double price
                    items_with_prices.append({'name': formatted_name, 'price': price})
                    total_price += price
                else:
                    # Append the item with its formatted name and price
                    items_with_prices.append({'name': formatted_name, 'price': price})
                    # Update the total price
                    total_price += price
            else:
                formatted_name = item
                price = DAILY_SPECIALS[item]
                items_with_prices.append({'name': formatted_name, 'price': DAILY_SPECIALS[item]})
                total_price += price


        # Generate a random expected time between 30-60 minutes from the current time
        expected_time = datetime.now() + timedelta(minutes=random.randint(30, 60))

        # Format the expected time to "Mon Sep 30 23:34:34 2024"
        formatted_expected_time = expected_time.strftime("%a %b %d %H:%M:%S %Y")
        
        # Prepare context for the confirmation page
        context = {
            'customer_name': request.POST.get('name', 'Guest'),
            'customer_phone': request.POST.get('phone', ''),
            'customer_email': request.POST.get('email', ''),
            'items_ordered': items_with_prices,  # List of items with their formatted names and prices
            'total_price': total_price,
            'expected_time': (formatted_expected_time),
        }

        # Render the confirmation page with the order details
        return render(request, 'restaurant/confirmation.html', context)

    # If not a POST request, render the order page again
    return render(request, 'restaurant/order.html')