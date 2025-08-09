import plotly.graph_objects as go
import json

# Define the architecture data
architecture_data = {
    "architecture_components": [
        {"layer": "Client Layer", "components": ["Cursor IDE", "Claude Desktop", "VS Code", "Custom MCP Clients"]},
        {"layer": "MCP Protocol", "components": ["stdio", "SSE (Server-Sent Events)", "HTTP Transport"]},
        {"layer": "FastMCP Server", "components": ["Tools (@mcp.tool)", "Resources (@mcp.resource)", "Document Search", "Content Retrieval", "Analysis Tools"]},
        {"layer": "Document Processing", "components": ["DocumentIndexer", "Classification Engine", "Metadata Extractor", "Content Parser", "Tag Processor"]},
        {"layer": "Storage", "components": ["SQLite Database", "Full-text Index", "Metadata Tables", "Document Cache"]},
        {"layer": "File System", "components": ["/strategy/ directory", "/brand/ directory", "/messaging/ directory", "/templates/ directory", "/guidelines/ directory"]}
    ],
    "data_flow": [
        {"from": "File System", "to": "Document Processing", "action": "File Discovery"},
        {"from": "Document Processing", "to": "Storage", "action": "Index & Store"},
        {"from": "Client Layer", "to": "MCP Protocol", "action": "Query Request"},
        {"from": "MCP Protocol", "to": "FastMCP Server", "action": "Protocol Trans"},
        {"from": "FastMCP Server", "to": "Storage", "action": "Search & Retrv"},
        {"from": "Storage", "to": "FastMCP Server", "action": "Results"},
        {"from": "FastMCP Server", "to": "Client Layer", "action": "Response"}
    ]
}

# Color mapping for layers
layer_colors = {
    "Client Layer": "#1FB8CD",
    "MCP Protocol": "#DB4545", 
    "FastMCP Server": "#2E8B57",
    "Document Processing": "#5D878F",
    "Storage": "#D2BA4C",
    "File System": "#B4413C"
}

# Create nodes with abbreviated names (15 char limit)
nodes = []
node_positions = {}
layer_y_positions = {
    "Client Layer": 5,
    "MCP Protocol": 4, 
    "FastMCP Server": 3,
    "Document Processing": 2,
    "Storage": 1,
    "File System": 0
}

node_id = 0
for layer_data in architecture_data["architecture_components"]:
    layer = layer_data["layer"]
    components = layer_data["components"]
    
    # Calculate x positions for components in this layer
    layer_width = len(components)
    x_positions = [i - (layer_width-1)/2 for i in range(layer_width)]
    
    for i, component in enumerate(components):
        # Abbreviate component names to fit 15 char limit
        abbreviated_name = component
        
        # Special abbreviations for common terms
        if "directory" in abbreviated_name:
            abbreviated_name = abbreviated_name.replace(" directory", " dir")
        if "Server-Sent Events" in abbreviated_name:
            abbreviated_name = "SSE"
        if "Classification Engine" in abbreviated_name:
            abbreviated_name = "Classifier"
        if "Full-text Index" in abbreviated_name:
            abbreviated_name = "FT Index"
        if "Metadata Tables" in abbreviated_name:
            abbreviated_name = "Meta Tables"
        if "Custom MCP Clients" in abbreviated_name:
            abbreviated_name = "Custom Clients"
        if "DocumentIndexer" in abbreviated_name:
            abbreviated_name = "Doc Indexer"
        if "Metadata Extractor" in abbreviated_name:
            abbreviated_name = "Meta Extract"
        if "Content Parser" in abbreviated_name:
            abbreviated_name = "Content Parse"
        if "Tag Processor" in abbreviated_name:
            abbreviated_name = "Tag Process"
        if "Document Cache" in abbreviated_name:
            abbreviated_name = "Doc Cache"
        if "Document Search" in abbreviated_name:
            abbreviated_name = "Doc Search"
        if "Content Retrieval" in abbreviated_name:
            abbreviated_name = "Content Retrv"
        if "Analysis Tools" in abbreviated_name:
            abbreviated_name = "Analysis"
        
        # Final truncation to 15 chars
        if len(abbreviated_name) > 15:
            abbreviated_name = abbreviated_name[:12] + "..."
        
        nodes.append({
            'id': node_id,
            'name': abbreviated_name,
            'layer': layer,
            'x': x_positions[i] * 2.5,
            'y': layer_y_positions[layer],
            'color': layer_colors[layer]
        })
        
        node_positions[component] = node_id
        if layer not in node_positions:
            node_positions[layer] = []
        node_positions[layer].append(node_id)
        node_id += 1

# Create layer mapping for data flow
layer_to_nodes = {}
for layer_data in architecture_data["architecture_components"]:
    layer = layer_data["layer"]
    layer_to_nodes[layer] = [node_positions[comp] for comp in layer_data["components"]]

# Create the network diagram
fig = go.Figure()

# Add edges for data flow connections
for flow in architecture_data["data_flow"]:
    from_layer = flow["from"]
    to_layer = flow["to"]
    
    if from_layer in layer_to_nodes and to_layer in layer_to_nodes:
        from_nodes = layer_to_nodes[from_layer]
        to_nodes = layer_to_nodes[to_layer]
        
        # Connect center nodes of each layer
        from_node_idx = from_nodes[len(from_nodes)//2]
        to_node_idx = to_nodes[len(to_nodes)//2]
        
        from_node = nodes[from_node_idx]
        to_node = nodes[to_node_idx]
        
        # Add connecting line
        fig.add_trace(go.Scatter(
            x=[from_node['x'], to_node['x']],
            y=[from_node['y'], to_node['y']],
            mode='lines',
            line=dict(width=2, color='#666666'),
            showlegend=False,
            hoverinfo='skip'
        ))

# Add nodes for each layer
for layer in layer_colors.keys():
    layer_nodes = [node for node in nodes if node['layer'] == layer]
    
    if layer_nodes:
        fig.add_trace(go.Scatter(
            x=[node['x'] for node in layer_nodes],
            y=[node['y'] for node in layer_nodes],
            mode='markers+text',
            marker=dict(
                size=30,
                color=layer_colors[layer],
                line=dict(width=2, color='white')
            ),
            text=[node['name'] for node in layer_nodes],
            textposition='middle center',
            textfont=dict(size=8, color='white', family='Arial'),
            name=layer[:15],  # Truncate layer name to 15 chars
            hovertemplate='<b>%{text}</b><br>Layer: ' + layer + '<extra></extra>'
        ))

# Update layout
fig.update_layout(
    title="MCP Server Architecture",
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-8, 8]),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.5, 5.5]),
    showlegend=True,
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
    plot_bgcolor='white'
)

# Save the chart
fig.write_image("mcp_architecture_diagram.png")