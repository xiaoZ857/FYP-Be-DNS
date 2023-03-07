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

@app.route('/add', methods=['POST'])
def add():
    domain = request.form['domain']
    ip = request.form['ip']
    owner = request.form['owner']
    key = request.form['key']
    ran = request.form['ran']
    if((domain == '')|(ip == '')|(owner == '')|(key == '')|(ran == '')):
        message = 'Please enter the information'
        return render_template("add&change.html", var1 = message)
    else:
        message = chainA.addNewBinding(domain, ip, owner, key, ran)
        return render_template("add&change.html", var1 = message)

@app.route('/change', methods=['POST'])
def change():
    domain = request.form['newdomain']
    newip = request.form['newip']
    owner = request.form['newowner']
    key = request.form['newkey']
    ran = request.form['newran']
    if((domain == '')|(newip == '')|(owner == '')|(key == '')|(ran == '')):
        message = 'Please enter the information'
        return render_template("add&change.html", var2 = message)
    else:
        message = chainA.changeBinding(domain, newip, owner, key, ran)
        return render_template("add&change.html", var2 = message)

@app.route('/search', methods=['POST'])
def search():
    domain = request.form['domain']
    ip = chainA.queryBinding(domain)
    return render_template("query.html", var1 = ip)



if __name__=="__main__":
    app.run(port=2020,host="127.0.0.1",debug=True)