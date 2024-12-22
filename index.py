import yaml
import json

def parse_yaml_to_tree(yaml_content):
    """
    Parses YAML content into a tree structure, assigning unique document IDs to all nodes.
    """
    data = yaml.safe_load(yaml_content)
    node_ids = {}  # Dictionary to store node names and their corresponding IDs
    id_counter = 0  # Counter for generating unique IDs

    def build_tree(data):
        nonlocal id_counter

        id_counter += 1
        
        if isinstance(data, dict):
            children = []
            for key, value in data.items():
                if key not in node_ids:
                    id_counter += 1
                    node_ids[key] = id_counter
                if not value is None:
                    children.append({"text": key, "id": node_ids[key], "children": build_tree(value)})
                else: 
                    children.append({"text": key, "id": node_ids[key], "children": []})
            return children
        elif isinstance(data, list):
            return [{"text": item, "id": node_ids.setdefault(item, id_counter := id_counter + 1), "children": []} for item in data]
        else:
            # Single value (e.g., strings or unstructured content) as leaf node
            if data not in node_ids:
                id_counter += 1
                node_ids[data] = id_counter
            return [{"text": data, "id": node_ids[data], "children": []}]

    return {"text": "root", "children": build_tree(data)}

def generate_html_from_tree(tree):
    """
    Converts a tree structure to a nested HTML list (ul/li), with document IDs
    and checkboxes.
    """
    html = ""
    
    # Start a new unordered list
    if tree["children"]:
        html += "<ul>\n"
        for child in tree["children"]:
            html += (
                f'<li id="node-{child["id"]}">'
                f'<label for="checkbox-{child["id"]}">{child["text"]}</label>\n'
                f'<input type="checkbox" id="checkbox-{child["id"]}" />'
            )
            html += generate_html_from_tree(child)  # Recursively generate nested lists
            html += "</li>\n"
        html += "</ul>\n"
    
    return html

def generate_acheivements(yaml_content):
    """
    each acheivement is a name with a list of required list items to complete the acheivement
    eg:
    tesla chad:
    - opencv
    - motion_tracking
    """

    data = yaml.safe_load(yaml_content)
    acheivements = {}
    for key, values in data.items():
        acheivements[key] = []
        for val in values:
            acheivements[key].append(val)
    return acheivements

# Function to generate HTML for each achievement
def generate_acheivements_html(achievements):
    html_content = ""
    index = 0
    for achievement in achievements:
        tasks = achievements[achievement]

        html_content += f"""
        <div class="achievement">
            <h3>{achievement}</h3>
            <div class="progress-container" id="ach-{index}">
                <div class="progress-bar" style="width: {0}%;">{0}/{len(tasks)}</div>
            </div>
        </div>
        """
        index += 1

    return html_content

def generate_complete_html(tree, acheivements):
    """
    Generates a complete HTML document with the tree structure and embedded JavaScript.
    """
    tree_html = generate_html_from_tree(tree)
    acheivements_html = generate_acheivements_html(acheivements)

    with open('./script.js', 'r') as file:
        scriptCode = file.read()
    javascript = f"""
    <script>
    const acheivements = {json.dumps(acheivements)}
    const progress = {json.dumps(list(map(lambda x : 0, acheivements)))}
    const maxs = {json.dumps(list(map(lambda x : len(acheivements[x]), acheivements)))}

    {scriptCode}
    </script>
    """
    
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Achievement Tracker</title>
        <style>
            .progress-container {
                width: 100%;
                background-color: #f3f3f3;
                border-radius: 25px;
                margin: 20px 0;
                height: 30px;
            }
            .progress-bar {
                height: 100%;
                width: 0%;
                background-color: #4caf50;
                text-align: center;
                line-height: 30px;  /* Vertically centers the text */
                color: black;       /* Make the text color black */
                border-radius: 25px;
                font-weight: bold;  /* Make the progress number bold */
            }
            .achievement {
                margin-bottom: 20px;
            }
            .achievement-title {
                font-size: 18px;
                font-weight: bold;
            }
            .task-list {
                list-style-type: none;
                padding-left: 0;
            }
            .task-list li {
                margin: 5px 0;
            }
            .task-checkbox {
                margin-right: 10px;
            }
        </style>
    </head>
    <body>
    """ + f"""
        {tree_html}
        {javascript}
        <h1>Achievement Tracker</h1>
        {acheivements_html}
    </body>
    </html>
    """

# Example YAML content
yaml_content = """
computer_graphics:
  computer_vision:
    - image_processing
    - pattern_recognition
machine_learning:
  supervised_learning:
    - regression
    - classification
  unsupervised_learning:
    - clustering
    - dimensionality_reduction
  classification:
    - womp
formal_methods:
  SAT_and_SMT_solvers: 
  automated_theorem_provers:
    - proof_assistants
    - model_checkers
"""

ach_yaml = """
    tesla cuck:
        - machine_learning
        - computer_graphics
    stats nerd:
        - regression
    """

# Parse the YAML content into a tree structure
tree = parse_yaml_to_tree(yaml_content)
acheivements = generate_acheivements(ach_yaml)

# Generate the nested HTML list from the tree structure
html_output = generate_complete_html(tree, acheivements)

# Print the resulting HTML
print(html_output)