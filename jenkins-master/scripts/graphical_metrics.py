import networkx as nx
from networkx.algorithms import community 
import pandas as pd
import numpy as np
from operator import itemgetter

print('Reading CSV')
df = pd.read_csv('../Datasets/clickstream-enwiki-2020-01.tsv',sep='\t',header=None)
df.columns = ['From','To','RelationType','Count']
df = df.head(2000)
df = df[df['RelationType']=='link']

# Building the graph G
print('Building the graphical representation')
nodes_from = df['From'].values
nodes_to = df['To'].values
nodes = np.concatenate((nodes_from, nodes_to))
edges = []
for r in df.values:
    edge = (r[0],r[1])
    edges.append(edge)
G = nx.Graph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)
print('Calculating graphical metrics')


# Node Degree
degree_dict = dict(G.degree(G.nodes()))
nx.set_node_attributes(G, degree_dict, 'degree')

# Betweenness and Eigenvector Centrality
betweenness_dict = nx.betweenness_centrality(G) # Run betweenness centrality
eigenvector_dict = nx.eigenvector_centrality(G) # Run eigenvector centrality
nx.set_node_attributes(G, betweenness_dict, 'betweenness')
nx.set_node_attributes(G, eigenvector_dict, 'eigenvector')

# Greedy Modularity Community Assignment
communities = community.greedy_modularity_communities(G)
modularity_dict = {} 
for i,c in enumerate(communities): 
    for name in c: 
        modularity_dict[name] = i 
nx.set_node_attributes(G, modularity_dict, 'modularity')


# Pandas helper functions
def get_degree(article):
    return G.nodes[article]['degree']

def get_eigenvector(article):
    return G.nodes[article]['eigenvector']

def get_beweenness(article):
    return G.nodes[article]['betweenness']

def get_community(article):
    return G.nodes[article]['modularity']

# Building the pandas dataframe
articles_df = pd.DataFrame(np.unique(nodes),columns=['Article'])
articles_df['Degree'] = articles_df['Article'].apply(get_degree)
articles_df['EigenvectorCentrality'] = articles_df['Article'].apply(get_eigenvector)
articles_df['BetweennessCentrality'] = articles_df['Article'].apply(get_beweenness)
articles_df['CommunityID'] = articles_df['Article'].apply(get_community)

# Write CSV
print('Writing CSV')
articles_df.to_csv('Results/graphical_metrics.csv',index=False)