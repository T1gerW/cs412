import time
from django.http import HttpResponse
from django.shortcuts import render


# Create views here 
def home(request):
    '''
    Function to handle the URL request for /hw (home page).
    Delegate rendering to the template hw/home/html
    '''

    template_name = 'hw/home.html'

    #create dictionary of context variable for the template
    context = {
        "current_time": time.ctime(),
    }

    # create and return a response to the client 
    return render(request, template_name)

