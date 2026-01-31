# UMAP visualization for Qdrant embeddings

import os
import random
import numpy as np
import matplotlib.pyplot as plt
import umap

from backend.qdrant.client import get_qdrant_client
from backend.config import QDRANT_COLLECTION


# ===============================
# Config
# ===============================

MAX_POINTS = 300      # suffisant pour visualisation
RANDOM_SEED = 42

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


# ===============================
# Main
# ===============================

def main():

    client = get_qdrant_client()

    # Charger des points depuis Qdrant
    points, _ = client.scroll(
        collection_name=QDRANT_COLLECTION,
        limit=MAX_POINTS,
        with_payload=True,
        with_vectors=True
    )

    if not points:
        raise RuntimeError("No points found in Qdrant")

    vectors = []
    labels = []
    colors = []

    # Préparer données
    for p in points:
        if p.vector is None or p.payload is None:
            continue

        vectors.append(p.vector)

        fraud = p.payload.get("fraud_label", False)
        decision = p.payload.get("decision", "UNKNOWN")

        # Label texte (optionnel)
        labels.append(f"{'FRAUD' if fraud else 'NORMAL'}-{decision}")

        # Couleurs
        if fraud:
            colors.append("red")
        elif decision == "ACCEPT_WITH_GUARANTEE":
            colors.append("orange")
        elif decision == "ACCEPT":
            colors.append("blue")
        elif decision == "REJECT":
            colors.append("purple")
        else:
            colors.append("gray")

    vectors = np.array(vectors)

    print(f"Loaded {len(vectors)} vectors for UMAP")

    # Appliquer UMAP (384D → 2D)
    reducer = umap.UMAP(
        n_neighbors=15,
        min_dist=0.1,
        n_components=2,
        metric="cosine",
        random_state=RANDOM_SEED
    )

    embedding_2d = reducer.fit_transform(vectors)

    # Plot
    plt.figure(figsize=(10, 8))
    plt.scatter(
        embedding_2d[:, 0],
        embedding_2d[:, 1],
        c=colors,
        alpha=0.7,
        s=40
    )

    plt.title("UMAP Projection of Credit Case Embeddings")
    plt.xlabel("UMAP-1")
    plt.ylabel("UMAP-2")

    # Légende manuelle
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', label='Fraud', markerfacecolor='red', markersize=8),
        plt.Line2D([0], [0], marker='o', color='w', label='Accept', markerfacecolor='blue', markersize=8),
        plt.Line2D([0], [0], marker='o', color='w', label='Accept with Guarantee', markerfacecolor='orange', markersize=8),
        plt.Line2D([0], [0], marker='o', color='w', label='Reject', markerfacecolor='purple', markersize=8),
    ]
    plt.legend(handles=legend_elements, loc="best")

    # Sauvegarde
    base_dir = os.path.dirname(__file__)  # dossier backend/evaluation
    output_path = os.path.join(base_dir, "umap_projection.png")

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.show()

    print(f"UMAP visualization saved to {output_path}")



if __name__ == "__main__":
    main()