from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json
from typing import Dict, List, Tuple, Union

# Decide what graph you want to load
GRAPH_FILENAME = 'graph1'

app = Flask(__name__)
CORS(app)

with open(f'graphs/{GRAPH_FILENAME}.json', 'r') as file:
    graph_nodes: Dict[str, Dict] = json.load(file)

@app.route("/")
def render_html() -> str:
    """Render the main HTML page."""
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search_nodes_endpoint() -> str:
    """Search for nodes by query."""
    query = request.args.get('query', '').lower()
    return jsonify(search_nodes(graph_nodes, query))

@app.route('/nodes/<node_name>', methods=['GET'])
def node_details_endpoint(node_name: str) -> str:
    """Get node details by name."""
    result = get_node_by_name(graph_nodes, node_name)
    if isinstance(result, str):
        return jsonify({"error": result}), 404
    return jsonify(result)

@app.route('/upstream/<node_name>', methods=['GET'])
def upstream_dependencies_endpoint(node_name: str) -> str:
    """Get upstream dependencies of a node."""
    max_depth = int(request.args.get('depth', float('inf')))
    output_string = generate_upstream_dependencies_string(graph_nodes, node_name, max_depth)
    return output_string

@app.route('/graph', methods=['GET'])
def graph_string_representation_endpoint() -> str:
    """Get the graph as a string representation."""
    return generate_graph_string_representation(graph_nodes)

def get_upstream_dependencies(graph_nodes: Dict[str, Dict], target_node_name: str, max_depth: int) -> List[Tuple[str, str]]:
    """Find all upstream dependencies of a target node with a depth limit."""
    reversed_dag = {}

    for node_data in graph_nodes.values():
        node_name = node_data.get('node_name')
        outgoing_edges = node_data.get('outgoing_edges', [])
        for target_name in outgoing_edges:
            if target_name not in reversed_dag:
                reversed_dag[target_name] = []
            reversed_dag[target_name].append(node_name)

    if target_node_name not in (node.get('node_name') for node in graph_nodes.values()):
        raise ValueError(f"Node with name '{target_node_name}' not found in nodes.")

    upstream_dependencies = set()

    def dfs(current_node_name: str, path: List[Tuple[str, str]], current_depth: int):
        if current_depth >= max_depth:
            return
        if current_node_name in reversed_dag:
            for predecessor_name in reversed_dag[current_node_name]:
                if (predecessor_name, current_node_name) not in path:
                    upstream_dependencies.add((predecessor_name, current_node_name))
                    dfs(predecessor_name, path + [(predecessor_name, current_node_name)], current_depth + 1)

    dfs(target_node_name, [], 0)
    return list(upstream_dependencies)

def get_node_by_name(graph_nodes: Dict[str, Dict], node_name: str) -> Union[Dict, str]:
    """Retrieve a node by its name."""
    for node_data in graph_nodes.values():
        if node_data.get('node_name') == node_name:
            return node_data
    return f"Node with name '{node_name}' not found."

def search_nodes(graph_nodes: Dict[str, Dict], query: str) -> List[str]:
    """Search nodes based on a query."""
    return [node_data.get('node_name') for node_data in graph_nodes.values() if query in node_data.get('node_name', '').lower()]

def generate_upstream_dependencies_string(graph_nodes: Dict[str, Dict], node_name: str, max_depth: int) -> str:
    """Generate a string representation of upstream dependencies."""
    upstream_dependencies = get_upstream_dependencies(graph_nodes, node_name, max_depth)
    if not upstream_dependencies:
        return node_name
    return "; ".join(f"{item[0]}-->{item[1]}" for item in upstream_dependencies) + ";"

def generate_graph_string_representation(graph_nodes: Dict[str, Dict]) -> str:
    """Generate a string representation of the graph."""
    edges = []
    for node_data in graph_nodes.values():
        node_name = node_data.get('node_name')
        outgoing_edges = node_data.get('outgoing_edges', [])
        for edge in outgoing_edges:
            edges.append(f"{node_name}-->{edge}")
    return "; ".join(edges)

if __name__ == '__main__':
    app.run(debug=True)
