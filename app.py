from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json

with open('graphs/graph3.json', 'r') as file:
    nodes = json.load(file)

app = Flask(__name__)
CORS(app)

@app.route("/") 
def render_html(): 
    return render_template('index.html') 

@app.route('/search', methods=['GET'])
def search_nodes_endpoint():
    query = request.args.get('query', '').lower()  # Convert query to lowercase
    return jsonify(search_nodes(nodes, query))

@app.route('/nodes/<node_name>', methods=['GET'])
def get_node_by_name_endpoint(node_name):
    return jsonify(get_node_by_name(nodes, node_name))

@app.route('/upstream/<node_name>', methods=['GET'])
def get_upstream_dependencies_endpoint(node_name):
    output_string = upstream_output_string(nodes, node_name)
    return output_string

@app.route('/graph', methods=['GET'])
def get_graph_as_string_endpoint():
    return get_graph_as_string(nodes)

def get_upstream_dependencies(nodes, target_node_name):
    reversed_dag = {}
    
    for node_name, node_data in nodes.items():
        outgoing_edges = node_data['outgoing_edges']
        for target_name in outgoing_edges:
            if target_name not in reversed_dag:
                reversed_dag[target_name] = []
            reversed_dag[target_name].append(node_name)
    
    if target_node_name not in nodes:
        raise ValueError(f"Node with name {target_node_name} not found in nodes.")
    
    target_node = nodes[target_node_name]
    
    upstream_dependencies = set()
    
    def dfs(current_node_name, path):
        if current_node_name in reversed_dag:
            for predecessor_name in reversed_dag[current_node_name]:
                if (predecessor_name, current_node_name) not in path:
                    upstream_dependencies.add((predecessor_name, current_node_name))
                    dfs(predecessor_name, path + [(predecessor_name, current_node_name)])
    
    dfs(target_node_name, [])
    return list(upstream_dependencies)

def get_node_by_name(nodes, node_name):
    if node_name in nodes:
        return nodes[node_name]
    else:
        return f"Node with name '{node_name}' not found."

def search_nodes(nodes, query):
    query = query.lower()
    return [node_name for node_name in nodes if query in node_name.lower()]

def upstream_output_string(nodes, node_name):
    upstream_dependencies = get_upstream_dependencies(nodes, node_name)
    if not upstream_dependencies:
        return node_name
    return "; ".join(f"{item[0]}-->{item[1]}" for item in upstream_dependencies) + ";"

def get_graph_as_string(nodes):
    edges = []
    for node_key, node_value in nodes.items():
        for edge in node_value['outgoing_edges']:
            edges.append(f"{node_key}-->{edge}")
    return "; ".join(edges)

if __name__ == '__main__':
    app.run(debug=True)
