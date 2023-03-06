from flask import Flask, render_template, request, url_for
from blockchain import*

app = Flask(__name__, template_folder = 'templates',static_folder='static',static_url_path='')
chainA = blockchain()

@app.route('/', methods=['GET'])
def Index():
    return render_template("index.html")


@app.route('/query', methods=['GET'])
def Query():
    return render_template("query.html")

@app.route('/account', methods=['GET'])
def Account():
    return render_template("account.html")

@app.route('/add&change', methods=['GET'])
def add_change():
    return render_template("add&change.html")

@app.route('/chain&node', methods=['GET'])
def chain_node():
    return render_template("chain&node.html")

@app.route('/create', methods=['POST'])
def createAccount():
    key = request.form['key']
    if(key == ''):
        message = 'Please enter a key'
        return render_template("account.html", var4=message)
    else:
        accountcreated = account(key)
        address = accountcreated.publickey
        ran = accountcreated.ran
        message = 'Account created successfully'
        return render_template("account.html", var1=address, var2=ran, var3=key, var4=message)


if __name__=="__main__":
    app.run(port=2020,host="127.0.0.1",debug=True)