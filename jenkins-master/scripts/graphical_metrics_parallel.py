import os
import sys
import networkx as nx
from networkx.algorithms import community 
import pandas as pd
import numpy as np

G = nx.Graph()

# Pandas helper functions
def get_degree(article):
    return G.nodes[article]['degree']

#def get_eigenvector(article):
#    return G.nodes[article]['eigenvector']

def get_beweenness(article):
    return G.nodes[article]['betweenness']

#def get_community(article):
#    return G.nodes[article]['modularity']

# Checking a directory
def check_path(inputPath):
    try:
        if not os.path.exists(inputPath):
            print("[Warning] Create the path. Path:[{}]".format(inputPath))
            os.makedirs(inputPath)
    except OSError:
        print ("[Error] Checking the directory %s failed" % inputPath)
        sys.exit(1)
        
        
def main(pathfile):        
    # pathfile = '../clickstream-enwiki-2020-01.tsv'

    print('Reading CSV')
#     df = pd.read_csv(pathfile,sep='\t',nrows=20000,header=None)
    df = pd.read_csv(pathfile, sep='\t', nrows=20000, header=None)
    df.columns = ['From','To','RelationType','Count']
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
#     G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    print('Calculating graphical metrics')


    # Node Degree
    degree_dict = dict(G.degree(G.nodes()))
    nx.set_node_attributes(G, degree_dict, 'degree')

    # Betweenness and Eigenvector Centrality
    betweenness_dict = nx.betweenness_centrality(G) # Run betweenness centrality#
    #eigenvector_dict = nx.eigenvector_centrality(G) # Run eigenvector centrality
    nx.set_node_attributes(G, betweenness_dict, 'betweenness')
    #nx.set_node_attributes(G, eigenvector_dict, 'eigenvector')

    # Greedy Modularity Community Assignment
    #communities = community.greedy_modularity_communities(G)
    #modularity_dict = {} 
    #for i,c in enumerate(communities): 
    #    for name in c: 
    #        modularity_dict[name] = i 
    #nx.set_node_attributes(G, modularity_dict, 'modularity')

    # Building the pandas dataframe
    articles_df = pd.DataFrame(np.unique(nodes),columns=['Article'])
    articles_df['Degree'] = articles_df['Article'].apply(get_degree)
    #articles_df['EigenvectorCentrality'] = articles_df['Article'].apply(get_eigenvector)
    articles_df['BetweennessCentrality'] = articles_df['Article'].apply(get_beweenness)
    #articles_df['CommunityID'] = articles_df['Article'].apply(get_community)

    # Write CSV
    outputPath = "../Outputs/clickstream/"
    check_path(outputPath)
    
    print('Writing CSV')
    left = pathfile.find('_')
    right = pathfile.find('.txt')
    outputPath = outputPath + "/" + "graphical_metrics_"+ str(pathfile[left+1:right]) + ".csv"    
    articles_df.to_csv(outputPath, index=False)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("[Error] Invalid inputs")
        sys.exit(1)

    path = sys.argv[1]
    print(path)
    
    check_path(path)
    main(path)
    