# config centralisée 
# ===============================
# Vector & Embedding Configuration
# ===============================

TEXT_EMBEDDING_MODEL = "all-MiniLM-L6-v2"
IMAGE_EMBEDDING_MODEL = "openclip-vit-b32"  

USE_IMAGE_EMBEDDING = True   # tu peux le désactiver si besoin

# ===============================
# Vector Fusion
# ===============================

NORMALIZE_L2 = True

# ===============================
# Qdrant Configuration
# ===============================

QDRANT_COLLECTION = "credit_cases"
QDRANT_DISTANCE = "Cosine"
TOP_K_SIMILAR = 10

# ===============================
# Similarity Thresholds
# ===============================

SIMILARITY_THRESHOLD = 0.75
FRAUD_SIMILARITY_THRESHOLD = 0.80
COLD_START_THRESHOLD = SIMILARITY_THRESHOLD
CONFIDENCE_LOW = 0.6

# ===============================
# Evaluation
# ===============================

PRECISION_K = 5

# ===============================
# Performance
# ===============================

ENABLE_LATENCY_LOGGING = True

# ===============================
# Qdrant Cloud Configuration
# ===============================

QDRANT_URL = "https://880b58fd-3475-43fb-b1d1-3d084b21b497.us-east4-0.gcp.cloud.qdrant.io:6333"
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.LHDHXiBzEP64sRK8XDGN81SFO_3F2CePlTTemz38KVM"
QDRANT_COLLECTION = "Credit_Cases"

# ===============================
# JWT Configuration
# ===============================

JWT_SECRET = "SECRET123"
JWT_ALGORITHM = "HS256"








