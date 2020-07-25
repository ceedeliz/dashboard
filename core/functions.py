import numpy as np
filename=""
def handle_uploaded_file(f, filename):
    with open(filename, 'wb+') as destination:
        for chunk in f.chunks():  
            destination.write(chunk)  

def mainApp1Function():
    numA = 10
    numB = 20
    res = 20 +10
    return res