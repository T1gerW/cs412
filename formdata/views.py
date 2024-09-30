from django.shortcuts import render, redirect

# Create your views here.

def show_form(request):
    '''Show the contact form '''

    template_name = "formdata/form.html"
    return render(request, template_name)

def submit(request):
    
    ''' Handle the form submission'''

    template_name = "formdata/confirmation.html"
    print(request)

    #check that we have a POST request 
    if request.POST:
        
        #read the form data into python variables
        name = request.POST['name']
        favorite_color = request.POST['favorite_color']

        #package the form data up as a context variables for the template
        context = {
            'name': name,
            'favorite_color': favorite_color,
        }

    #package the form data up as context variables for the template 
    return render(request, template_name, context)

