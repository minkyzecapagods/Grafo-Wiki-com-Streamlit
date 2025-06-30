# Grafo-Wiki-com-Streamlit

[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)]((https://grafo-wiki-com-app-upb5gsvsdaf6w5cyfwew3s.streamlit.app/))

## Visão Geral

Este repositório contém uma aplicação web construída com Streamlit para análise e visualização interativa de um grafo de rede. A aplicação carrega um grafo direcionado que representa uma teia de artigos interconectados da Wikipédia, originada a partir do tópico "RPG Eletrônico". Ela fornece ferramentas para explorar a estrutura do grafo, identificar nós-chave e entender suas propriedades gerais por meio de diversas métricas da análise de redes.

## Funcionalidades

*   **Visualização Interativa do Grafo**: Renderiza o grafo usando PyVis, permitindo que o usuário faça zoom, movimente o grafo e inspecione nós individuais e suas conexões.
*   **Múltiplos Layouts**: Suporta diferentes layouts de visualização, incluindo ForceAtlas2, Barnes-Hut, Repulsion e Hierarchical, para melhor adequação à análise.
*   **Análise de Métricas do Grafo**: Calcula e exibe automaticamente métricas chave do grafo:
    *   Densidade
    *   Assortatividade de Grau
    *   Coeficiente Médio de Clusterização
    *   Número de Componentes Fortemente e Fracamente Conectados
*   **Análise de Centralidade**: Calcula e ranqueia os nós segundo quatro medidas diferentes de centralidade para identificar os artigos mais influentes na rede:
    *   Centralidade de Autovetor (Eigenvector)
    *   Centralidade de Grau (Degree)
    *   Centralidade de Proximidade (Closeness)
    *   Centralidade de Intermediação (Betweenness)
*   **Filtragem Dinâmica**: O usuário pode filtrar o grafo visualizado para focar em subconjuntos específicos, como o maior componente conectado ou nós com grau mínimo.
*   **Gráfico da Distribuição de Grau**: Exibe histogramas das distribuições de grau de entrada (in-degree) e saída (out-degree) para fornecer insights sobre a topologia da rede.

## Dataset

Os dados do grafo estão armazenados em `data/rpg.graphml`. Trata-se de um grafo direcionado onde:
*   **Nós**: Representam artigos individuais da Wikipédia.
*   **Arestas**: Representam um hyperlink de um artigo para outro.

O dataset foi criado a partir do rastreamento de páginas da Wikipédia começando pelo artigo "RPG Eletrônico".

## Antes de começar

Para executar esta aplicação na sua máquina local, siga os passos abaixo.

### Pré-requisitos

*   Python 3.7 ou superior
*   `pip` e `venv`

## Instalação e Execução

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/minkyzecapagods/Grafo-Wiki-com-Streamlit.git
    cd Grafo-Wiki-com-Streamlit
    ```
    
### Com scripts de conveniência
Você pode usar os scripts fornecidos para automatizar o processo de configuração e inicialização.

2.  **Execute diretamente com o script:**
*   **No macOS e Linux:**
    ```bash
    chmod +x start.sh
    ./start.sh
    ```
*   **No Windows:**
    ```bash
    start.bat
    ```
    
    Seu navegador deverá abrir uma nova aba com a aplicação em funcionamento.
    
### Manualmente

Alternativamente, você pode fazer tudo de forma manual.

2.  **Crie e ative um ambiente virtual:**

    *   **No macOS e Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    *   **No Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Instale as dependências necessárias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a aplicação Streamlit:**
    ```bash
    streamlit run app.py
    ```
    Seu navegador deverá abrir uma nova aba com a aplicação em funcionamento.

## Tecnologia Utilizada

*   **Streamlit**: Para criação da aplicação web interativa.
*   **NetworkX**: Para manipulação e análise do grafo.
*   **PyVis**: Para gerar visualizações interativas da rede.
*   **Pandas**: Para manipulação e exibição de dados.
*   **Matplotlib**: Para plotar a distribuição de grau.
