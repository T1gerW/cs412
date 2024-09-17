from django.http import HttpResponse
from django.shortcuts import render


# Create views here 
def main(request):
    '''Handle the main URL for the hw app'''

    response_text = '''
    <html> 
    <h1> Hello, World! </h1>
    </html>
    '''

    # create and return a response to the client 
    return HttpResponse(response_text)