import requests

a="https://www.x.com/"

r=requests.get(a)
print(r.headers)