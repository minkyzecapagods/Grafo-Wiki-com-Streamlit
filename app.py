import streamlit as st
import networkx as nx
from pyvis.network import Network
import matplotlib.pyplot as plt
import pandas as pd
import tempfile, os
from matplotlib import cm

st.set_page_config(page_title="Análise da Wiki para RPG", layout="wide")
st.title("Análise e Visualização da Wiki a partir de RPG Eletrônico")

GRAPH_PATH = os.path.join("data", "rpg.graphml")

@st.cache_data
def load_graphml(file):
    return nx.read_graphml(file)

def explain_metric(name):
    explanations = {
        "Densidade": "Proporção de arestas existentes sobre o total possível, mede quão 'cheio' está o grafo.",
        "Assortatividade": "Indica se nós tendem a se conectar a outros nós com grau semelhante.",
        "Coeficiente de Clustering": "Mede a tendência dos nós formarem triângulos (grupos fechados).",
        "Componentes Fortemente Conectados": "Subgrafos onde cada nó é alcançável de qualquer outro (direcionado).",
        "Componentes Fracamente Conectados": "Subgrafos conectados se ignorarmos a direção das arestas."
    }
    return explanations.get(name, "")

def normalize(values, min_size=10, max_size=40):
    min_val, max_val = min(values), max(values)
    if min_val == max_val:
        return [(min_size + max_size) / 2] * len(values)
    return [min_size + (val - min_val) / (max_val - min_val) * (max_size - min_size) for val in values]

def show_pyvis_graph(G, selected_nodes=None, node_values=None, height="600px", width="100%", layout="forceAtlas2Based"):
    net = Network(height=height, width=width, notebook=False, directed=G.is_directed())

    if layout == "forceAtlas2Based":
        net.force_atlas_2based()
    elif layout == "barnesHut":
        net.barnes_hut()
    elif layout == "repulsion":
        net.repulsion()
    elif layout == "hierarchical":
        net.set_options("""
        {
          "layout": {
            "hierarchical": {
              "enabled": true,
              "direction": "UD",
              "sortMethod": "hubsize"
            }
          },
          "physics": {
            "hierarchicalRepulsion": {
              "nodeDistance": 120
            }
          }
        }
        """)

    net.from_nx(G)

    if selected_nodes and node_values:
        selected_nodes = list(map(str, selected_nodes))
        sizes = normalize([node_values[n] for n in selected_nodes])
        colors = cm.get_cmap('YlOrRd')(normalize([node_values[n] for n in selected_nodes], 0, 1))
        selected_map = {str(n): (s, c) for n, s, c in zip(selected_nodes, sizes, colors)}

        for node in net.nodes:
            node_id = str(node['id'])
            if node_id in selected_map:
                size, color_rgba = selected_map[node_id]
                color_hex = '#{:02x}{:02x}{:02x}'.format(*(int(c * 255) for c in color_rgba[:3]))
                node.update({'color': color_hex, 'size': size, 'shape': 'dot'})
            else:
                node.update({'color': 'lightgray', 'size': 8, 'shape': 'dot'})
    else:
        for node in net.nodes:
            node.update({'shape': 'dot', 'size': 10})

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    net.write_html(tmp_file.name)
    tmp_file.close()

    with open(tmp_file.name, 'r', encoding='utf-8') as f:
        html = f.read()

    st.components.v1.html(html, height=600, width=900)
    os.remove(tmp_file.name)

def plot_degree_distribution(G):
    if G.is_directed():
        fig, ax = plt.subplots(1, 2, figsize=(12, 4))
        ax[0].hist([d for _, d in G.in_degree()], bins=20, color='blue', alpha=0.7)
        ax[0].set_title("In-Degree")
        ax[1].hist([d for _, d in G.out_degree()], bins=20, color='green', alpha=0.7)
        ax[1].set_title("Out-Degree")
    else:
        fig, ax = plt.subplots()
        ax.hist([d for _, d in G.degree()], bins=20, color='purple', alpha=0.7)
        ax.set_title("Distribuição de Grau")
    st.pyplot(fig)

def display_top(centrality_dict, name, k):
    if not centrality_dict:
        st.write(f"Centralidade {name} não disponível.")
        return
    st.write(f"**Top {k} nós por {name}:**")
    df_top = pd.DataFrame(sorted(centrality_dict.items(), key=lambda x: x[1], reverse=True)[:k],
                          columns=["Nó", "Valor"])
    st.table(df_top)

def calculate_centralities(G):
    try:
        eigen = nx.eigenvector_centrality(G, max_iter=1000, tol=1e-6)
    except Exception as e:
        st.error(f"Erro ao calcular eigenvector: {e}")
        eigen = None
    return {
        "Eigenvector": eigen,
        "Degree": nx.degree_centrality(G),
        "Closeness": nx.closeness_centrality(G),
        "Betweenness": nx.betweenness_centrality(G)
    }

def display_graph_metrics(G):
    st.markdown("### Métricas")
    st.write("**Densidade:**", nx.density(G))
    st.caption(explain_metric("Densidade"))

    try:
        st.write("**Assortatividade:**", nx.degree_assortativity_coefficient(G))
        st.caption(explain_metric("Assortatividade"))
    except:
        st.warning("Assortatividade não pôde ser calculada.")

    if not G.is_directed():
        st.write("**Coeficiente de Clustering:**", nx.average_clustering(G))
        st.caption(explain_metric("Coeficiente de Clustering"))

    if G.is_directed():
        st.write("**Componentes Fortemente Conectados:**", len(list(nx.strongly_connected_components(G))))
        st.caption(explain_metric("Componentes Fortemente Conectados"))
        st.write("**Componentes Fracamente Conectados:**", len(list(nx.weakly_connected_components(G))))
        st.caption(explain_metric("Componentes Fracamente Conectados"))
    else:
        st.write("**Componentes Conectados:**", len(list(nx.connected_components(G))))

def main():
    try:
        G = load_graphml(GRAPH_PATH)
        st.success(f"Grafo carregado: `{GRAPH_PATH}`")
    except FileNotFoundError:
        st.error(f"Arquivo `{GRAPH_PATH}` não encontrado.")
        st.stop()

    st.sidebar.header("Visualização do Grafo")
    view_option = st.sidebar.selectbox("Selecione um subgrafo:",
        ["Grafo Completo", "Maior Componente Conectado", "Nós com grau ≥ X"])

    if view_option == "Maior Componente Conectado":
        components = list(nx.strongly_connected_components(G) if G.is_directed() else nx.connected_components(G))
        G_view = G.subgraph(max(components, key=len))
    elif view_option == "Nós com grau ≥ X":
        try:
            max_grau = max(dict(G.degree()).values())
        except ValueError:
            max_grau = 1
        grau_min = st.sidebar.slider("Grau mínimo:", 1, max_grau, 100)
        G_view = G.subgraph([n for n, d in G.degree() if d >= grau_min])
    else:
        G_view = G

    layout_option = st.sidebar.selectbox("Layout do grafo:",
        ["forceAtlas2Based", "barnesHut", "repulsion", "hierarchical"])

    display_graph_metrics(G)
    st.markdown("### Distribuição de Grau")
    plot_degree_distribution(G)

    st.sidebar.header("Centralidade dos Nós")
    top_k = st.sidebar.slider("Top-k nós", 1, 20, 5)
    centrality_choice = st.sidebar.selectbox("Centralidade destacada:",
        ["Nenhuma", "Eigenvector", "Degree", "Closeness", "Betweenness"])

    with st.spinner("Calculando centralidades..."):
        centralities = calculate_centralities(G_view)

    selected_nodes = node_values = None
    if centrality_choice != "Nenhuma" and centralities.get(centrality_choice):
        c_dict = centralities[centrality_choice]
        top_nodes = sorted(c_dict.items(), key=lambda x: x[1], reverse=True)[:top_k]
        selected_nodes = [node for node, _ in top_nodes]
        node_values = {node: c_dict[node] for node in selected_nodes}

    st.markdown("### Visualização Interativa")
    show_pyvis_graph(G_view, selected_nodes, node_values, layout=layout_option)

    for name in ["Eigenvector", "Degree", "Closeness", "Betweenness"]:
        display_top(centralities.get(name), name, top_k)

if __name__ == "__main__":
    main()