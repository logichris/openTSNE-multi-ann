import gzip
import pickle
from time import time

import openTSNE
import openTSNE.callbacks


class Timer:
    def __init__(self, message):
        self.message = message
        self.start_time = time()

    def __enter__(self):
        print(self.message)

    def __exit__(self, *args):
        end_time = time()
        print(" --> Time elapsed: %.2f seconds" % (end_time - self.start_time))


with Timer("Loading data..."):
    with gzip.open("../examples/data/macosko_2015.pkl.gz", "rb") as f:
        data = pickle.load(f)

x = data["pca_50"]
y, cluster_ids = data["CellType1"], data["CellType2"]

with Timer("Finding nearest neighbors..."):
    affinities = openTSNE.affinity.PerplexityBasedNN(
        x, perplexity=30, method="approx", n_jobs=8, random_state=3
    )

with Timer("Creating initial embedding..."):
    init = openTSNE.initialization.random(x, random_state=3)

with Timer("Creating embedding object..."):
    embedding = openTSNE.TSNEEmbedding(
        init,
        affinities,
        negative_gradient_method="fft",
        n_jobs=8,
        callbacks=openTSNE.callbacks.ErrorLogger(),
        random_state=3,
    )


with Timer("Running optimization..."):
    embedding.optimize(n_iter=250, exaggeration=12, momentum=0.5, inplace=True)
    embedding.optimize(n_iter=750, momentum=0.8, inplace=True)
