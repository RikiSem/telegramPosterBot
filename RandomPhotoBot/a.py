import requests

zapros = requests.get("https://dzen.ru/?clid=1787308&win=37&yredirect=true").text
print(zapros)