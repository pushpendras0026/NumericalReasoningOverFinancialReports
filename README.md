# Numerical Reasoning over Financial Reports

**Authors:** Pushpendra Singh and Badri Bishal Das
Indian Institute of Technology Guwahati, Big Data course project

**Question we study:** with one model and a fixed limit on evidence, do answers improve
if each fact keeps its headers, units, hierarchy and links with it, compared with
ordinary packing?

One pipeline runs over FinQA, ConvFinQA, TAT-QA and HybridQA (assigned), plus TAT-HQA
and MultiHiertt (added by us).

Main files to read:

- Report: [`report/main.pdf`](report/main.pdf)
- Slides: [`presentation/slides.pdf`](presentation/slides.pdf) and
  [`presentation/slide.pptx`](presentation/slide.pptx)
- Who did what: [`contribution.md`](contribution.md)

## How to run this project

Follow the steps in order. Run every command in a Linux or WSL (Ubuntu) terminal.

| Steps | What you get | Needs |
|---|---|---|
| 1 to 5 | Setup | Internet |
| 6 | Tests and offline checks | Nothing extra |
| 7 | Spark results | Java |
| 8 | Model results | Gemini API key |
| 9 | Fresh tables and figures | Step 8 finished |
| 10 | Report PDF | Only steps 1 and 2 |
| 11 | Slides and video clips | Optional |

### Step 1. Install the required programs

You need Python 3.12, Java 17 or newer, Git LFS and LaTeX.

```bash
sudo apt update
sudo apt install -y python3.12-venv default-jdk git git-lfs latexmk texlive-latex-extra texlive-publishers texlive-science
git lfs install
```

### Step 2. Download the code and data

```bash
git clone https://github.com/pushpendras0026/NumericalReasoningOverFinancialReports.git
cd NumericalReasoningOverFinancialReports
git lfs pull
```

All the commands below must be run from this folder.

### Step 3. Create the Python environment

```bash
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### Step 4. Download the official scorers and the HybridQA tables

This puts files in `third_party/` and `data/WikiTables-WithLinks/`.

```bash
bash scripts/fetch_upstream.sh
```

### Step 5. Prepare the terminal and the output folder

Run the `export` line again every time you open a new terminal.

```bash
export PYTHONPATH=src
mkdir -p artifacts/v11
```

### Step 6. Run the tests and offline checks

These do not need an API key.

```bash
.venv/bin/python -m unittest discover -s tests
.venv/bin/python scripts/run_mock_api_smoke.py
.venv/bin/python scripts/coverage_audit.py
.venv/bin/python scripts/document_sizes.py
.venv/bin/python scripts/label_cost.py
```

What to expect:

| Command | Result |
|---|---|
| Unit tests | The last line says `OK` |
| Mock run | Prints a summary. It uses a fake model, so it is only a check of the pipeline |
| Coverage | `artifacts/v11/coverage.json` (same numbers as the coverage table in the report) |
| Document sizes | `artifacts/v11/document_sizes.json` |
| Label cost | `artifacts/v11/label_cost.json` |

### Step 7. Run the Spark preparation

Start with the quick check.

```bash
bash scripts/run_spark.sh 100
```

To run all three sizes used in the report:

```bash
bash scripts/run_spark.sh 100 1000 full
```

Results are saved in `artifacts/v11/spark/<size>/`. In each `measurement_<cores>.json`
file, `equals_python` must be `true`.

### Step 8. Run the model experiments

You need a Gemini API key. Copy the example file and put your key in `.env`.

```bash
cp .env.example .env
nano .env
```

Inside `.env`, write your key after `GEMINI_API_KEY=` and save the file. Then start the
two experiments.

```bash
bash scripts/run_v11.sh a gemini-3.5-flash-lite eval finqa tatqa tathqa convfinqa hybridqa multihiertt
bash scripts/run_v11.sh b gemini-3.1-flash-lite b_grounded,b_direct finqa tatqa tathqa convfinqa hybridqa multihiertt
```

Answers and scores are saved in `artifacts/v11/a/` and `artifacts/v11/b/`.

The free Gemini plan allows about 500 requests per day, so a run can stop before it
finishes. Run the same command the next day. It continues from where it stopped and does
not repeat finished requests.

Model answers are not stored in this repository, so step 9 needs this step to finish
first. Model providers can change or remove models over time, so a new run may not give
exactly the same numbers as the report.

### Step 9. Create the report tables and figures again

Run this only after step 8 is finished. The tables from our own runs are already in
`report/generated/`, so you can skip this step.

```bash
PYTHONPATH=src:scripts .venv/bin/python scripts/error_analysis.py artifacts/v11/b b_grounded dependency
PYTHONPATH=src:scripts .venv/bin/python scripts/report_tables.py
PYTHONPATH=src .venv/bin/python scripts/report_figures.py
.venv/bin/python scripts/model_usage.py
PYTHONPATH=src:scripts .venv/bin/python scripts/video_examples.py
```

Tables and figures go to `report/generated/`. The combined numbers go to
`artifacts/v11/report_numbers.json`.

### Step 10. Build the report

This works straight after step 2 because the tables are already in the repository.

```bash
cd report
latexmk -pdf -interaction=nonstopmode main.tex
cd ..
```

The result is `report/main.pdf` (5 pages).

### Step 11. Build the slides and video clips (optional)

Slides:

```bash
cd presentation
latexmk -pdf -interaction=nonstopmode slides.tex
cd ..
```

Video clips:

```bash
sudo apt install -y ffmpeg libpango1.0-dev libcairo2-dev pkg-config
.venv/bin/pip install manim
cd presentation/video
../../.venv/bin/manim -qh -a clips.py
cd ../..
```

## Common problems

| Problem | Fix |
|---|---|
| `No module named nrqa` | Run `export PYTHONPATH=src` from the project folder |
| `IEEEtran.cls not found` | Run `sudo apt install -y texlive-publishers` |
| A dataset file looks very small or cannot be read | Run `git lfs pull` |
| `third_party` or `WikiTables-WithLinks` not found | Run step 4 again |
| Java or Spark error | Run `java -version` and check that it is 17 or newer |
| Model run stops with a quota error | Wait for the next day and run the same command |

## Repository layout

| Path | Contents |
|---|---|
| `src/nrqa/` | Pipeline: readers, retrieval, packing, grounded answers, execution, scoring, Spark preparation |
| `scripts/` | Run, audit and report tools |
| `tests/` | Unit tests (no API calls) |
| `experiments/` | Run settings. `v11/` and `frozen_v11/` are the ones used in the report |
| `data/` | Supplied datasets (the two largest files use Git LFS) |
| `report/` | LaTeX source, generated tables and figures, PDF |
| `presentation/` | Slides, 12 Manim clips and their source |

| Stage | Code | What it does |
|---|---|---|
| Readers | `datasets.py`, `finqa.py` | Turn each dataset into evidence facts and links between them. Answers are kept apart |
| Retrieval | `core.py: retrieve` | BM25 search over the supplied document |
| Packing | `core.py: pack_method` | Ordinary, dependency, or length-matched control |
| Answer plan | `grounded.py` | The model copies numbers and phrases, and code matches them to the evidence |
| Execution | `execute.py` | Does the calculation using the official operations only |
| Scoring | `scoring.py`, `official_worker.py` | Runs the official scorers in separate processes |
| Run record | `runner.py`, `experiment.py` | Fixed settings, saved model responses, runs that can continue later |
| Big Data | `preparation.py` | Spark Parquet preparation, checked against a Python version |
| Audit | `coverage.py` | Checks if the correct evidence is still there after packing |

## Results

Scores are official execution accuracy for FinQA and ConvFinQA and official F1 for the
others. Block B uses a relaxed numeric measure for FinQA and ConvFinQA, because direct
answers have no program. O = ordinary, D = dependency, L = length-matched.

| Dataset | Coverage O / D (all dev) | Block A: O / D / L | D-O (95% CI) | Block B: executor / direct |
|---|---|---|---|---|
| FinQA | 96.3 / 97.3 (n=845) | 62.0 / 64.0 / 66.0 (n=50) | +2.0 (+0.0, +6.2) | 62.5 / 67.5 (n=40) |
| ConvFinQA | 97.1 / 97.4 (n=1,486) | 73.3 / 73.3 / 68.9 (n=45) | +0.0 (-6.0, +6.4) | 75.0 / 75.0 (n=36) |
| TAT-QA | 90.1 / 91.7 (n=1,636) | 60.2 / 71.5 / 69.4 (n=50) | +11.3 (+4.1, +19.9) | 65.2 / 58.7 (n=40) |
| TAT-HQA | 84.2 / 86.9 (n=792) | 56.7 / 60.7 / 52.7 (n=50) | +4.0 (-6.4, +14.5) | 60.0 / 56.7 (n=40) |
| HybridQA | 72.0 / 76.0 (n=3,466) | 54.9 / 60.1 / 49.8 (n=50) | +5.3 (-2.4, +13.0) | 50.2 / 66.6 (n=40) |
| MultiHiertt | 84.9 / 88.6 (n=1,043) | 47.0 / 56.8 / 41.0 (n=50) | +9.8 (+0.0, +20.0) | 63.7 / 41.7 (n=40) |

- **Coverage** (no model): D keeps more correct evidence than O on all six datasets at
  the chosen limits. The gap closes as the limit grows.
- **Block A** (`gemini-3.5-flash-lite`): D is better than O on five datasets and equal on
  ConvFinQA. The interval excludes zero only on TAT-QA.
- **Block B** (`gemini-3.1-flash-lite`): no consistent gain from the executor. Direct
  answering wins on HybridQA. MultiHiertt's +22.1 comes from the scoring method. Under one
  rule for both sides it is +6.2 (-6.2, +20.0), see `scripts/multihiertt_sensitivity.py`.
- **Spark**: 1,360,644 facts and 1,884,748 edges, 0 unresolved, equal to the Python
  version on every run. Python takes 15.8 s for the same work and Spark 37.0 s at best, so
  at this size Spark's value is the checked Parquet store, not speed.
