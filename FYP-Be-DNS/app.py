# Import necessary libraries
from flask import Flask, render_template, request, url_for, jsonify
import json
from blockchain import*
# Create Flask app and initialize blockchain and node
app = Flask(__name__, template_folder = 'templates',static_folder='static',static_url_path='')
selfChain = blockchain()

# Input the desired IP address and port
host = '127.0.0.1'
port = 5000
ip = f'{host}:{port}'
selfNode = node(selfChain, ip)

# Route to the main page
@app.route('/', methods=['GET'])
def Index():
    return render_template("index.html")

# Route to the query page
@app.route('/query', methods=['GET'])
def Query():
    return render_template("query.html")

# Route to the account page
@app.route('/account', methods=['GET'])
def Account():
    return render_template("account.html")

# Route to the add & change page
@app.route('/add&change', methods=['GET'])
def add_change():
    data = selfNode.getData()
    leader = data['leader']
    return render_template("add&change.html", var5=leader)

# Route to the chain & node page
@app.route('/chain&node', methods=['GET'])
def chain_node():
    data = selfNode.getData()
    leader = data['leader']
    height = data['height']
    nodes = data['nodes']
    return render_template("chain&node.html", var1=leader, var2 = height, var3 = nodes)

# Route to create an account
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

# Route to add a new domain name and IP address binding
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

# Route to change the IP address for an existing domain name
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

# Route to search for an IP address associated with a domain name
@app.route('/search', methods=['POST'])
def search():
    domain = request.form['domain']
    ip = selfChain.queryBinding(domain)
    return render_template("query.html", var1 = ip)

# Route to handle voting requests among nodes
@app.route('/vote_request', methods=['POST'])
def vote_request():
    data = request.get_json()
    term = data['term']
    url = data['url']
    if url != selfNode.url:
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

# Route to handle heartbeats among nodes
@app.route('/receive_heartbeat', methods=['POST'])
def receive_heartbeat():
    height = request.form.get('height')
    hash = request.form.get('hash')
    term = request.form.get('term')
    url = request.form.get('url')
    height_check = (height == len(selfChain.chain))
    hash_check = (hash == selfChain.getMapHash)
    term_check = (term == selfNode.term)
    if url != selfNode.url:
        if url == selfNode.leader:
            if (height_check and hash_check and term_check):
                response = 'correct'
                selfNode.received = True
                return response, 200
            else:
                response = 'incorrect'
                selfNode.received = True
                selfNode.recover()
                return response, 200

# Route to retrieve the chain data
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {
            'chain': selfChain.chain,
            'NametoIpmap': selfChain.NametoIpmap,
            'NametoOwnermap': selfChain.NametoOwnermap,
        }
    return response, 200

# Route to receive new blocks from other nodes
@app.route('/receive_block', methods=['POST'])
def receive_block():
    url = request.form.get('url')
    index = request.form.get('index')
    previousHash = request.form.get('previousHash')
    timestamp = request.form.get('timestamp')
    mapHash = request.form.get('mapHash')
    hash = request.form.get('hash')
    newNametoIpmap = json.loads(request.form.get('newNametoIpmap'))
    newNametoOwnermap = json.loads(request.form.get('newNametoOwnermap'))
    if url != selfNode.url:
        newBlock = block(index, previousHash, timestamp, mapHash)
        if newBlock.hash == hash:
            selfChain.chain.append(newBlock)
            selfChain.NametoIpmap = newNametoIpmap
            selfChain.NametoOwnermap = newNametoOwnermap
            response = 'Block received'
        else:
            response = 'Block rejected'
        return response, 200