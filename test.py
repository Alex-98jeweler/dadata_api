import re
from dadata import Dadata
token = "1e6b20fd720f7f75dae41c301b8486ef6fd0db26"
secret = '56d780143aab6946897488eb4e177166bb36594c'
dadata = Dadata(token, secret)
result = dadata.suggest("address", "улан удэ терешковой д 9", count=10, language='en')
for i in result:
    print(i['value'])
