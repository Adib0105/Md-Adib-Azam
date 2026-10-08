# Operator-managed model artifacts

Runtime artifacts are private JSON files under `instance/ml/`, not committed here.
Run the training command described in `docs/DATA_PIPELINE.md`. The loader checks the
feature contract, dependency versions, schema, size and SHA-256 content digest.
It never uses pickle and there is no web endpoint for uploading a model.
