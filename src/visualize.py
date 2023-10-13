from flask import Flask, render_template
import networkx as nx
import json

app = Flask(__name__)

data = {
    "user1": ["repo1", "repo2"],
    "user2": ["repo1", "repo3"],
    "user3": ["repo2", "repo4"],
    "user4": ["repo1", "repo5"],
    "user5": ["repo2", "repo5"],
    "user6": ["repo4", "repo8"],
    "user7": ["repo3", "repo5"],
    "user8": ["repo5", "repo11"],
    "user9": ["repo4", "repo51"],
    "user10": ["repo5", "repo6"],
    #... add more data as needed
}

@app.route('/')
@app.route('/')
def visualize_graph():
    G = nx.Graph()

    # Dictionary to store users for each repository pair
    repo_pair_users = {}

    # Add edges between repositories if they share a user
    for user, repos in data.items():
        for i, repo1 in enumerate(repos):
            for repo2 in repos[i+1:]:
                if not G.has_edge(repo1, repo2):
                    G.add_edge(repo1, repo2)
                    repo_pair_users[(repo1, repo2)] = [user]
                else:
                    repo_pair_users[(repo1, repo2)].append(user)

    # Extract nodes and links for visualization
    nodes = [{"id": node, "group": 2} for node in G.nodes()]
    links = [
        {
            "source": edge[0],
            "target": edge[1],
            "value": 1,
            "label": repo_pair_users[edge]  # Add the 'id' field here
        }
        for edge in G.edges()]

    # Convert the graph to nodes and links for D3 visualization
    # nodes = [{"id": node, "group": 1 if node in data else 2} for node in G.nodes()]
    # links = [{"source": edge[0], "target": edge[1], "value": 1} for edge in G.edges()]


    print("Nodes:", nodes)
    print("Links:", links)
    print(G)


    return render_template('index.html', nodes=nodes, links=links)


if __name__ == "__main__":
    app.run(debug=True)
