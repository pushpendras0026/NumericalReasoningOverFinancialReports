# Numerical Reasoning over Financial Reports

**Authors:** Pushpendra Singh and Badri Bishal Das
Indian Institute of Technology Guwahati, Big Data course project

With one model and a fixed evidence budget, does keeping each fact's headers, units,
hierarchy and links with it improve answers compared with ordinary packing? One
pipeline runs over FinQA, ConvFinQA, TAT-QA and HybridQA (assigned), plus TAT-HQA and
MultiHiertt (added).

The report is [`report/main.pdf`](report/main.pdf). The slides are
[`presentation/slides.pdf`](presentation/slides.pdf) and
[`report/main_presentation.pptx`](report/main_presentation.pptx).

## Repository layout

| Path | Contents |
|---|---|
| `src/nrqa/` | Pipeline: readers, retrieval, packing, grounded answers, execution, scoring, Spark preparation |
| `scripts/` | Run, audit and report-generation tools |
| `tests/` | Unit tests (no API calls) |
| `experiments/` | Run configurations; `v11/` and `frozen_v11/` are the ones used in the report |
| `data/` | Supplied datasets (the two largest files use Git LFS) |
| `report/` | LaTeX source, generated tables and figures, PDF |
| `presentation/` | Slides, speaker notes, 12 Manim clips and their source |

| Stage | Code | What it does |
|---|---|---|
| Readers | `datasets.py`, `finqa.py` | Dataset to evidence facts with dependency edges; labels kept apart |
| Retrieval | `core.py: retrieve` | Deterministic BM25 over the supplied document |
| Packing | `core.py: pack_method` | Ordinary, dependency closure, or length-matched control |
| Answer plan | `grounded.py` | Model copies numbers and phrases; code resolves them to evidence |
| Execution | `execute.py` | Bounded decimal interpreter, official operations only |
| Scoring | `scoring.py`, `official_worker.py` | Official evaluators in isolated subprocesses |
| Run ledger | `runner.py`, `experiment.py` | Frozen contracts; saved raw responses; resumable runs |
| Big Data | `preparation.py` | Spark Parquet preparation, checked against a Python reference |
| Audit | `coverage.py` | Does gold evidence survive packing? Used after inference only |

## Step-by-step: run everything

Run all commands on Linux or WSL (Ubuntu), from the repository root.

### 1. Install prerequisites

You need Python 3.12, Java 17 or newer (for Spark), Git LFS, and `latexmk` with
`pdflatex` (for the report).

```bash
sudo apt install python3.12-venv default-jdk git-lfs latexmk texlive-latex-extra texlive-publishers texlive-science
git lfs install
```

### 2. Get the code and data

```bash
git clone <this repository's URL> NumericalReasoningOverFinancialReports
cd NumericalReasoningOverFinancialReports
git lfs pull
```

### 3. Create the Python environment

```bash
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### 4. Fetch the official evaluators and the HybridQA corpus

This downloads pinned commits into `third_party/` and `data/WikiTables-WithLinks/`.

```bash
scripts/fetch_upstream.sh
```

### 5. Prepare the shell and output folder

Repeat `export` in every new terminal.

```bash
export PYTHONPATH=src
mkdir -p artifacts/v11
```

### 6. Run the offline steps (no API key, about 5 minutes)

```bash
.venv/bin/python -m unittest discover -s tests     # 80 tests
.venv/bin/python scripts/run_mock_api_smoke.py     # pipeline check with a mock model
.venv/bin/python scripts/coverage_audit.py         # gold-evidence coverage, all dev questions
.venv/bin/python scripts/document_sizes.py         # median document sizes
.venv/bin/python scripts/label_cost.py             # cost of inline labels
```

| Output | Location |
|---|---|
| Test result | Terminal: `Ran 80 tests ... OK` |
| Mock pipeline summary | Terminal; marked as mock, not a model result |
| Coverage (matches the report's coverage table) | `artifacts/v11/coverage.json` |
| Document sizes | `artifacts/v11/document_sizes.json` |
| Label cost | `artifacts/v11/label_cost.json` |

### 7. Run Spark preparation

```bash
scripts/run_spark.sh 100         # quick check, about 1 minute
scripts/run_spark.sh 100 1000 full   # all three sizes used in the report
```

Results are in `artifacts/v11/spark/<size>/`. In each `measurement_<cores>.json`,
`equals_python` must be `true`.

### 8. Run the model experiments (needs a Gemini API key)

```bash
cp .env.example .env     # then put your key in .env
scripts/run_v11.sh a gemini-3.5-flash-lite eval finqa tatqa tathqa convfinqa hybridqa multihiertt
scripts/run_v11.sh b gemini-3.1-flash-lite b_grounded,b_direct finqa tatqa tathqa convfinqa hybridqa multihiertt
```

Saved answers and scores are written to `artifacts/v11/a/` and `artifacts/v11/b/`.
Runs stop at the provider's quota (500 requests per day on the free tier for
`gemini-3.5-flash-lite`). Run the same command again the next day: it resumes from
its ledger and never repeats a completed request.

The saved model responses are not stored in this repository, so step 9 needs this
step to finish first. The tables already in `report/generated/` are the ones from our
runs. Provider models can change or be withdrawn over time, so a new run may not match
those numbers exactly.

### 9. Regenerate the report tables and figures (needs steps 6 to 8)

```bash
PYTHONPATH=src:scripts .venv/bin/python scripts/error_analysis.py artifacts/v11/b b_grounded dependency
PYTHONPATH=src:scripts .venv/bin/python scripts/report_tables.py
PYTHONPATH=src .venv/bin/python scripts/report_figures.py
.venv/bin/python scripts/model_usage.py
PYTHONPATH=src:scripts .venv/bin/python scripts/video_examples.py
```

Tables and figures go to `report/generated/`; the combined numbers go to
`artifacts/v11/report_numbers.json`.

### 10. Build the report

This works straight after step 2, using the tables already in the repository.

```bash
cd report && make && cd ..      # writes report/main.pdf (5 pages)
```

### 11. Optional: rebuild the presentation files

```bash
.venv/bin/pip install python-pptx manim
.venv/bin/python report/build_main_pptx.py              # report/main_presentation.pptx
(cd presentation && latexmk -pdf slides.tex)            # presentation/slides.pdf
(cd presentation/video && ../../.venv/bin/manim -qh -a clips.py)   # clips
```

## Results

Scores are official execution accuracy for FinQA and ConvFinQA and official F1
otherwise. Block B uses a labelled relaxed numeric measure for FinQA and ConvFinQA,
whose direct answers have no program. O = ordinary, D = dependency, L = length-matched.

| Dataset | Coverage O / D (all dev) | Block A: O / D / L | D−O (95% CI) | Block B: executor / direct |
|---|---|---|---|---|
| FinQA | 96.3 / 97.3 (n=845) | 62.0 / 64.0 / 66.0 (n=50) | +2.0 (+0.0, +6.2) | 62.5 / 67.5 (n=40) |
| ConvFinQA | 97.1 / 97.4 (n=1,486) | 73.3 / 73.3 / 68.9 (n=45) | +0.0 (-6.0, +6.4) | 75.0 / 75.0 (n=36) |
| TAT-QA | 90.1 / 91.7 (n=1,636) | 60.2 / 71.5 / 69.4 (n=50) | +11.3 (+4.1, +19.9) | 65.2 / 58.7 (n=40) |
| TAT-HQA | 84.2 / 86.9 (n=792) | 56.7 / 60.7 / 52.7 (n=50) | +4.0 (-6.4, +14.5) | 60.0 / 56.7 (n=40) |
| HybridQA | 72.0 / 76.0 (n=3,466) | 54.9 / 60.1 / 49.8 (n=50) | +5.3 (-2.4, +13.0) | 50.2 / 66.6 (n=40) |
| MultiHiertt | 84.9 / 88.6 (n=1,043) | 47.0 / 56.8 / 41.0 (n=50) | +9.8 (+0.0, +20.0) | 63.7 / 41.7 (n=40) |

- **Coverage** (no model): D keeps more gold evidence than O on all six datasets at the
  chosen caps; the gap closes as budgets grow.
- **Block A** (`gemini-3.5-flash-lite`): D > O on five datasets and equal on ConvFinQA;
  the interval excludes zero only on TAT-QA.
- **Block B** (`gemini-3.1-flash-lite`): no consistent executor gain. Direct answering
  wins on HybridQA. MultiHiertt's +22.1 is a scoring artefact: under one rule for both
  sides it is +6.2 (−6.2, +20.0), see `scripts/multihiertt_sensitivity.py`.
- **Spark**: 1,360,644 facts and 1,884,748 edges, 0 unresolved, equal to the Python
  reference on every run. Python takes 15.8 s for the same work and Spark 37.0 s at
  best, so its value at this size is the checked Parquet store, not speed.
