# BS Motos — LLM-Assisted Survey Analysis (Docker-First)

An end-to-end, Docker-first system for processing and analyzing motorcycle-buyer
survey data. It turns raw survey CSVs into structured records, uses an LLM to generate
and categorize responses across a fixed questionnaire, and presents the results in an
interactive dashboard.

## Objective

Automate the tedious part of survey analysis: take messy questionnaire exports, produce
consistent categorical answers across ten survey questions with an LLM, and give analysts
a clean, interactive view of the results, all reproducibly through containers.

## Pipeline

1. **`1_building_json.py`** — parse the survey CSV into a structured JSON schema.
2. **`2_building_prompt.py`** — build the prompts that drive LLM response generation.
3. **`3_building_output.py`** — produce the categorized output.
4. **`pipeline.py`** — orchestrates the full flow.
5. **`dashboard.py`** — interactive Streamlit dashboard over the results.

## What's inside

- `scripts/` — helper scripts for setup, secure setup, running the pipeline, and the
  dashboard.
- `Dockerfile` / `docker-compose.yml` — containerized, no local Python required.
- `inputs/` — sample survey data.
- `SECURITY.md` + `.github/workflows/security.yml` — security notes and CI checks.

## Stack

Python · OpenAI API · Streamlit · Docker.

## Quick start

```bash
./scripts/setup.sh      # one-time setup
./scripts/run.sh        # run the pipeline + dashboard
```
