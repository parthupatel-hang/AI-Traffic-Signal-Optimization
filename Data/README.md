# Traffic Dataset

The original project uses a 20,000-record traffic dataset with 14 input features and `BestRoad` as the target.

For a public, source-focused repository, the full local dataset is not committed here. Place the project's `traffic_dataset.csv` at:

```text
Data/traffic_dataset.csv
```

The training script also contains a deterministic demo-data fallback so the application can be initialized when the private/full dataset is unavailable.
