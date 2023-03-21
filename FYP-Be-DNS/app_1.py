from flask import Flask, render_template, request, url_for, jsonify
from blockchain import*

app = Flask(__name__, template_folder = 'templates',static_folder='static',static_url_path='')
selfChain = blockchain()
selfNode = node(selfChain, '127.0.0.1:5001')

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
    data = selfNode.getData()
    leader = data['leader']
    height = data['height']
    nodes = data['nodes']
    return render_template("chain&node.html", var1=leader, var2 = height, var3 = nodes)

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
        message = selfChain.addNewBinding(domain, ip, owner, key, ran)
        if message == 'Successfully added':
            selfNode.broadcast_block()
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
        message = selfChain.changeBinding(domain, newip, owner, key, ran)
        if message == 'Successfully changed':
            selfNode.broadcast_block()
        return render_template("add&change.html", var2 = message)

@app.route('/search', methods=['POST'])
def search():
    domain = request.form['domain']
    ip = selfChain.queryBinding(domain)
    return render_template("query.html", var1 = ip)

@app.route('/vote_request', methods=['POST'])
def vote_request():
    data = request.get_json()
    term = data['term']
    url = data['url']
    if url is not selfNode.url:
        if selfNode.voted is False:
            if term > selfNode.term :
                response = {
                    'term': term,
                    'vote': 'yes'
                }
                selfNode.term = term
                selfNode.leader = url
                selfNode.voted = True
                selfNode.votes_received = 0
                selfNode.state = 'follower'
                return jsonify(response), 200
            else :
                response = {
                    'term': selfNode.term,
                    'vote': 'no'
                }
                return jsonify(response), 200
        if selfNode.voted is True:
            response = {
                    'term': selfNode.term,
                    'vote': 'no'
                }
            return jsonify(response), 200

@app.route('/receive_heartbeat', methods=['POST'])
def receive_heartbeat():
    data = request.get_json()
    height = data['height']
    hash = data['hash']
    term = data['term']
    url = data['url']
    height_check = (height == len(selfChain.chain))
    hash_check = (hash == selfChain.getMapHash)
    term_check = (term == selfNode.term)
    if url is not selfNode.url:
        if url == selfNode.leader:
            if (height_check and hash_check and term_check):
                response = {
                    'heart': 'correct'
                }
                selfNode.received = True
                return jsonify(response), 200
            else:
                response = {
                    'heart': 'incorrect'
                }
                selfNode.received = True
                selfNode.recover()
                return jsonify(response), 200

@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {
            'chain': selfChain.chain,
            'NametoIpmap': selfChain.NametoIpmap,
            'NametoOwnermap': selfChain.NametoOwnermap,
        }
    return jsonify(response), 200


@app.route('/receive_block', methods=['POST'])
def receive_block():
    data = request.get_json()
    url = data['url']
    index = data['index']
    previousHash = data['previousHash']
    timestamp = data['timestamp']
    mapHash = data['mapHash']
    hash = data['hash']
    newNametoIpmap = data['newNametoIpmap']
    newNametoOwnermap = data['newNametoOwnermap']
    if url is not selfNode.url:
        newBlock = block(index, previousHash, timestamp, mapHash)
        selfChain.chain.append(newBlock)
        selfChain.NametoIpmap = newNametoIpmap
        selfChain.NametoOwnermap = newNametoOwnermap
        response = 'Block received'
        return response, 200









if __name__=="__main__":
    app.run(port=5001,host="127.0.0.1",debug=True)