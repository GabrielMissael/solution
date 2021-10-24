import pandas as pd  # Working with the data
import numpy as np
import json

import plotly.express as px  # Interactive plots
import plotly

import sentence_transformers  # NLP Embeddings
import umap  # Dimensionality reduction.
import hdbscan  # Clustering

import time


def cluster(file, verbose=False, n_neighbors=15, min_dist=0.0,
            min_cluster_size=10, min_samples = 1,):

    """Create clusters of tweets with similar meaning.

    First, the tweets are transformed to vectors in a 512 dimentional space
    using sentence transformers. Next, a dimensionality reduction is made
    using UMAP. Finally, clusters are created using HDBSCAN.

    Args:
        file (str): File path with .json file with tweets.
        plot (bool): Default to False. To create .html interactive scatter plot or not.
        verbose (bool): Default to False.
        impath (str): Path and name to save .html plot file.

    Returns:
        DataFrame: Contains original .json file information.
            Includes cluster's labels, UMAPs and embeddings.
    """
    start_time = time.time()

    if verbose:
        print('Loading data...💖')

    # Load data
    with open(file, 'r') as f:
        data = json.load(f)

    # Prepare data format
    df = pd.DataFrame(data).T
    df = df.reset_index(drop=True)
    df = df.drop(columns=['created_at'])
    df = df.drop_duplicates(subset='text')

    # Load NLP model
    model = sentence_transformers.SentenceTransformer(
        'distiluse-base-multilingual-cased-v2')

    # Create and save embeddings
    if verbose:
        print('Creating embeddings...😎')

    embs = model.encode(df['text'].tolist())
    df['embs'] = list(embs)

    # Load dimensionality reduction model
    reducer = umap.UMAP(
        n_neighbors=n_neighbors,
        n_components=15,
        min_dist=min_dist,
        metric='cosine')

    # Reduce dimensionality of embeddings
    if verbose:
        print('Reducing dimensionality...🔥')

    df['umap'] = list(reducer.fit_transform(df.loc[:, 'embs'].to_list()))

    # Clustering using HDBSCAN
    if verbose:
        print('Creating clusters...🌍')

    cluster = hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples = min_samples,
        metric='euclidean',
        cluster_selection_method='eom').fit(df['umap'].to_list())

    # Save labels of clusters
    df['labels'] = cluster.labels_

    print(f'{len(set(cluster.labels_))} clusters created 🧠')
    print(f'{list(cluster.labels_).count(-1)} tweets unassigned')

    # Reduce dimensionality again (only for plotting purposes)
    umap_plot = umap.UMAP(
        n_neighbors=n_neighbors,
        n_components=2,
        min_dist=0.0,
        metric='cosine').fit_transform(df['umap'].to_list())

    # Save plot coordinates
    df['x'] = umap_plot.T[0]
    df['y'] = umap_plot.T[1]

    if verbose:
        print(time.time() - start_time, " seconds of execution ⌚")
        print('Done!✅')

    return df
