import os
import base64
from flask import Flask, request, redirect, url_for
from model import Message
from markupsafe import escape
import peewee

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            m = Message(content=request.form['content'])
            m.save()
        except peewee.IntegrityError:
            return "Duplicate entry detected. Please submit a unique message."

    body = """
<html>
<body>
<h1>Class Message Board</h1>
<h2>Contribute to the Knowledge of Others</h2>
<form method="POST">
    <textarea name="content"></textarea>
    <input type="submit" value="Submit">
</form>

<h2>Wisdom From Your Fellow Classmates</h2>
"""
    
    for m in Message.select():
        body += """
<div class="message">
{}
</div>
""".format(escape(m.content))

    body += """
</body>
</html>
"""
    
    return body

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)


