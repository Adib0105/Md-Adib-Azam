# Deployment and optional model setup

## Default local operation

Use the existing VS Code/Windows instructions and `start_windows.cmd`. From the
project folder:

```bash
python -m pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000` in Chrome. The existing `start_windows.cmd` launcher,
bundled fonts/JS and offline demo catalogue still work. No Transformer dependency
or model download is needed. Hybrid runs with its transparent TF-IDF fallback.
Use `ML_STRATEGY=weighted` for the retained seven-factor baseline.

## Existing databases

Schema version 3 adds feedback/experiment/exposure tables and indexes. Local
automatic migration retains existing records and creates an integrity-checked
SQLite backup before upgrading an existing database. Production keeps the existing
manual migration gate. Back up and run `python scripts/upgrade_database.py` using
the existing deployment workflow. There are no destructive table replacements.
Old `model.joblib` files are ignored; delete them only as an operator cleanup task.
The safe TF-IDF cache rebuilds automatically as `instance/tfidf-cache.npz`.

## Optional CPU embeddings

Python 3.11/3.12 is tested for the base app. The optional Sentence Transformers
5.1.2 wheel requires Python >=3.9, Transformers >=4.41,<5 and PyTorch >=1.11;
its constructor/encode/save interfaces were checked from the pinned wheel.
Install a supported **CPU** PyTorch build deliberately before the extension,
following [PyTorch's selector](https://pytorch.org/get-started/locally/). Do not let
a generic dependency install pull unwanted CUDA packages onto a small laptop.

```bash
python -m pip install -r requirements-embeddings.txt
python scripts/prepare_embeddings.py --revision EXACT_UPSTREAM_40_CHAR_COMMIT --output instance/ml/sentence-model
```

The placeholder is intentionally not a fabricated model commit. Inspect the
upstream model's history and pin its actual commit. The preparation command is
operator-only, downloads once and writes safetensors plus revision metadata.
Then set `EMBEDDINGS_ENABLED=true`, `EMBEDDING_MODEL_PATH` to its absolute folder,
and `EMBEDDING_MODEL_REVISION` to the same commit. Restart the app. Web requests
load only the prepared local folder and cannot initiate model downloads.

The 384-dimensional MiniLM checkpoint is about 90 MB for float32 weights; the
Python/PyTorch/Transformer installation and working memory are substantially
larger. Budget and measure CPU latency and several hundred MB of runtime memory
on the target device; these are planning estimates, **not measurements from this
release**. Batch size is configurable (default 32). Long inputs are subject to
the model's 256-token truncation. Model/version metadata and content hashes avoid
re-encoding unchanged jobs. English semantic quality needs real-label validation.

## Trained rankers

```bash
python scripts/train_ranker.py --dataset instance/ml/reviewed-relevance.jsonl --model logistic
```

Set `ML_STRATEGY=ltr` to request the private `instance/ml/ranker.json`. Synthetic
rankers remain disabled unless an operator explicitly sets the demo flag. Exact
feature/dependency/embedding representation checks prevent incompatible loading;
JSON coefficients/trees are bounded and never executed as code. Changing dependency
versions requires retraining. Keep the instance directory private and backed up.
POSIX exports use owner-only file modes; on Windows, restrict the instance folder
with the operator account's NTFS ACLs because `chmod` is not an ACL privacy guarantee.

## Security and production checks

Existing production checks for a random secret, trusted HTTPS origin, secure cookies,
HSTS and encrypted/disabled mail remain. CSRF, admin permission checks and owner
scoping apply to new pages/actions. Provider credentials never enter frontend JS.
Resume workers have byte/page/expanded-ZIP/text limits and a 15-second parent
timeout; Linux additionally bounds CPU/address space. Windows requires independent
target-machine validation of worker/resource behavior. Do not expose an arbitrary
model-upload or dynamic training endpoint.

Run `python -m pytest -q`, `python -m ruff check .`, `python -m black --check .`,
`python -m compileall -q app.py config.py models routes services ml`, the evaluation
command and optional local Playwright smoke test before publishing. This upgrade
does not certify throughput, external provider availability or real hiring accuracy.
