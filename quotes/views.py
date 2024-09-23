import random
from django.shortcuts import render

# List of quotes and images
quotes = [
    {"quote": "The time is always right to do what is right.", "person": "Martin Luther King Jr."},
    {"quote": "In the end, we will remember not the words of our enemies, but the silence of our friends.", "person": "Martin Luther King Jr."},
    {"quote": "Our lives begin to end the day we become silent about things that matter.", "person": "Martin Luther King Jr."}
    # Add more quotes and images as needed
]

images = [
    "/images/martin-luther-king-jr-9365086-2-402.jpg.avif",
    "/images/Martin-Luther-King-Jr.jpg.webp",
    "/images/mlk.jpg"
]

# View for the main page (random quote and image)
def quote(request):
    selected_quote = random.choice(quotes)  # Randomly select a quote
    selected_image = random.choice(images)  # Randomly select an image
    context = {'quote': selected_quote, 'image': selected_image}  # Pass the selected quote and image to the template
    return render(request, 'quotes/quote.html', context)  # Render the 'quote.html' template with the context

# View to show all quotes and images
def show_all(request):
    combined = [{'quote': quotes[i]['quote'], 'image': images[i]} for i in range(len(quotes))]  # Combine quotes and images
    context = {'combined': combined}  # Pass the combined list to the template
    return render(request, 'quotes/show_all.html', context)  # Render 'show_all.html' with the context

# View for the about page
def about(request):
    biographical_info = {
        'creator_name': 'Your Name',
        'creator_note': 'This application was developed to display random quotes by a notable individual.',
        'person_bio': 'This is a brief biography of the famous person whose quotes are featured.'
    }
    return render(request, 'quotes/about.html', biographical_info)