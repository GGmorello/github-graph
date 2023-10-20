from flask import Flask, request, render_template
import networkx as nx
import random

app = Flask(__name__)

data = {}

def create_mock_data():
    user_names = [
        "Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hannah", 
        "Isaac", "Jack", "Kylie", "Liam", "Mia", "Nathan", "Olivia", "Paul", 
        "Quinn", "Rachel", "Steve", "Tracy", "Ursula", "Victor", "Whitney", 
        "Xander", "Yara", "Zane", "Amber", "Brian", "Celine", "Derek", "Ella", 
        "Finn", "Gloria", "Henry", "Ivy", "Joel", "Kim", "Lucas", "Mandy", "Neil", 
        "Opal", "Pete", "Quincy", "Rita", "Sam", "Tina", "Ulysses", "Vera", "Walter"
    ]
    # Tech keywords and general descriptors for generating repo names
    tech_keywords = ["Data", "AI", "Web", "App", "System", "Platform", "Net", "Node", "Base", "Tech", "Code", "Stack", "Flow", "Logic", "View", "Bit", "Byte", "Grid", "API", "Frame"]
    general_descriptors = ["Engine", "Manager", "Hub", "Analyzer", "Optimizer", "Tracker", "Interface", "Assistant", "Connector", "Resolver", "Generator", "Guide", "Insight", "Link", "Forge", "Composer", "Pilot", "Guard", "Craft", "Wise"]

    # Generate repository names
    repository_names = [f"{random.choice(tech_keywords)}{random.choice(general_descriptors)}" for _ in range(100)]
    repository_names = list(set(repository_names))  # Remove any duplicates

    # Randomly assign repositories to each user
    mock_data = {}
    for user in user_names:
        # Assign 2 to 6 repositories to each user for variety
        num_repos = random.randint(2, 6)
        repos = random.sample(repository_names, num_repos)
        mock_data[user] = repos
    return mock_data

@app.route('/')
def visualize_graph():
    G = nx.Graph()

    # Dictionary to store users for each repository pair
    repo_pair_users = {}

    # Add edges between repositories if they share a user
    for user, repos in data.items():
        for i, repo1 in enumerate(repos):
            if not G.has_node(repo1):
                G.add_node(repo1)
            for repo2 in repos[i+1:]:
                if not G.has_node(repo2):
                    G.add_node(repo2)
                if not G.has_edge(repo1, repo2):
                    G.add_edge(repo1, repo2, weight=1)
                    repo_pair_users[(repo1, repo2)] = [user]
                else:
                    key = (repo1, repo2) if (repo1, repo2) in repo_pair_users else (repo2, repo1)
                    repo_pair_users[key].append(user)
                    G[repo1][repo2]["weight"] += 1

    # Extract nodes and links to pass them to index.html
    nodes = [{"id": node, "group": 2, "degree": G.degree(node)} for node in G.nodes()]
    links = [
        {
            "source": edge[0],
            "target": edge[1],
            "weight": G[edge[0]][edge[1]]["weight"],
            "label": repo_pair_users.get(edge, [])
        }
        for edge in G.edges()]
            
    return render_template('index.html', nodes=nodes, links=links)

@app.route("/append",methods=['POST'])
def append():
    req = request.get_json()
    for r in req:
        u = r['author']
        repo = r['repo']
        c = r['count']
        if not u in data:
            data[u] = []
        if not repo in data[u]:
            data[u].append(repo)
    return []

if __name__ == "__main__":
    # data = create_mock_data()
    app.run(debug=True)
