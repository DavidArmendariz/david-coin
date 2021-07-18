from uuid import uuid4
from flask import Flask, jsonify, request
from blockchain import Blockchain

app = Flask(__name__)

# Creating an address for the node on Port 5000
node_address = str(uuid4()).replace("-", "")

blockchain = Blockchain()


@app.route("/mine_block", methods=["GET"])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block["proof"]
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender=node_address, receiver="David", amount=1)
    block = blockchain.create_block(proof, previous_hash)
    response = {
        "message": "Congratulations, you just mined a block!",
        "index": block["index"],
        "timestamp": block["timestamp"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"],
        "transactions": block["transactions"],
    }
    return jsonify(response), 200


@app.route("/get_chain", methods=["GET"])
def get_chain():
    chain = blockchain.chain
    response = {"chain": chain, "length": len(chain)}
    return jsonify(response), 200


@app.route("/is_valid", methods=["GET"])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {"message": "The blockchain is valid"}
    else:
        response = {"message": "The blockchain is not valid"}
    return jsonify(response), 200


@app.route("/add_transaction", methods=["POST"])
def add_transaction():
    json = request.get_json()
    transaction_keys = ["sender", "receiver", "amount"]

    if not all(key in json for key in transaction_keys):
        return "Some elements of the transaction are missing", 400

    index = blockchain.add_transaction(json["sender"], json["receiver"], json["amount"])
    response = {"message": f"This transaction will be added to Block {index}"}

    return jsonify(response), 201


@app.route("/connect_node", methods=["POST"])
def connect_node():
    json = request.get_json()
    nodes = json.get("nodes")

    if nodes is None:
        return "No node", 400

    for node in nodes:
        blockchain.add_node(node)

    response = {
        "message": "All the nodes are now connected",
        "total_nodes": list(blockchain.nodes),
    }

    return jsonify(response), 201
