# Token-Bucket-based Dynamic Batching Client

This is the client of the TBDB algorithm. Client sends 3 types of task data:
- Inference tasks for anomaly detection of temporal data (from Wafer dataset)
- Text translation (Chinese to English, around 20-50 words per sentence)
- Image classification (from mnist)

File describe:
- `client.py` will send requests in 5 stages.
- `sin_client.py` will send a series of consecutive requests with sin rule fluctuations.
- `vis.py` is used to visualize the request log.
