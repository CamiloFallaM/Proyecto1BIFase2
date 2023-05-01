import requests

url = 'http://127.0.0.1:8000/predict/'
myobj = {'descripcion': 'Me encanto la pelicula'}

x = requests.post(url, json = myobj)

print(x.text)