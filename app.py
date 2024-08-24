from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json
from typing import Dict, List, Union

app = Flask(__name__)
CORS(app)

# Decide what graph you want to load
graph_name = 'graph1'

with open(f'graphs/{graph_name}.json', 'r') as file:
    nodes: Dict[str, Dict] = json.load(file)

@app.route("/")
def render_html() -> str:
    """Render the main HTML page."""
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search_nodes_endpoint() -> str:
    """Search for nodes by query."""
    query = request.args.get('query', '').lower()
    return jsonify(search_nodes(nodes, query))

@app.route('/nodes/<node_name>', methods=['GET'])
def get_node_by_name_endpoint(node_name: str) -> str:
    """Get node details by name."""
    result = get_node_by_name(nodes, node_name)
    if isinstance(result, str):  # Error message
        return jsonify({"error": result}), 404
    return jsonify(result)

@app.route('/upstream/<node_name>', methods=['GET'])
def get_upstream_dependencies_endpoint(node_name: str) -> str:
    """Get upstream dependencies of a node."""
    output_string = upstream_output_string(nodes, node_name)
    return output_string

@app.route('/graph', methods=['GET'])
def get_graph_as_string_endpoint() -> str:
    """Get the graph as a string representation."""
    return get_graph_as_string(nodes)

def get_upstream_dependencies(nodes: Dict[str, Dict], target_node_name: str) -> List[tuple]:
    """Find all upstream dependencies of a target node."""
    reversed_dag = {}
    
    for node_name, node_data in nodes.items():
        outgoing_edges = node_data.get('outgoing_edges', [])
        for target_name in outgoing_edges:
            if target_name not in reversed_dag:
                reversed_dag[target_name] = []
            reversed_dag[target_name].append(node_name)
    
    if target_node_name not in nodes:
        raise ValueError(f"Node with name '{target_node_name}' not found in nodes.")
    
    upstream_dependencies = set()
    
    def dfs(current_node_name: str, path: List[tuple]):
        if current_node_name in reversed_dag:
            for predecessor_name in reversed_dag[current_node_name]:
                if (predecessor_name, current_node_name) not in path:
                    upstream_dependencies.add((predecessor_name, current_node_name))
                    dfs(predecessor_name, path + [(predecessor_name, current_node_name)])
    
    dfs(target_node_name, [])
    return list(upstream_dependencies)

def get_node_by_name(nodes: Dict[str, Dict], node_name: str) -> Union[Dict, str]:
    """Retrieve a node by its name."""
    return nodes.get(node_name, f"Node with name '{node_name}' not found.")

def search_nodes(nodes: Dict[str, Dict], query: str) -> List[str]:
    """Search nodes based on a query."""
    return [node_name for node_name in nodes if query in node_name.lower()]

def upstream_output_string(nodes: Dict[str, Dict], node_name: str) -> str:
    """Generate a string representation of upstream dependencies."""
    upstream_dependencies = get_upstream_dependencies(nodes, node_name)
    if not upstream_dependencies:
        return node_name
    return "; ".join(f"{item[0]}-->{item[1]}" for item in upstream_dependencies) + ";"

def get_graph_as_string(nodes: Dict[str, Dict]) -> str:
    """Generate a string representation of the graph."""
    edges = []
    for node_key, node_value in nodes.items():
        outgoing_edges = node_value.get('outgoing_edges', [])
        for edge in outgoing_edges:
            edges.append(f"{node_key}-->{edge}")
    return "; ".join(edges)

if __name__ == '__main__':
    app.run(debug=True)
