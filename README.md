<h1 align="center">BS Motos — LLM-Assisted Survey Analysis</h1>

<p align="center">
  <strong>A Docker-first system that turns raw motorcycle-buyer survey data into structured, categorized results and an interactive dashboard.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11+-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/OpenAI-API-412991?logo=openai&logoColor=white" alt="OpenAI">
  <img src="https://img.shields.io/badge/Streamlit-dashboard-ff4b4b?logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Docker-first-2496ed?logo=docker&logoColor=white" alt="Docker">
</p>

---

## Overview

An end-to-end, **Docker-first** system for processing and analyzing motorcycle-buyer survey data.
It parses messy survey exports into structured records, uses an LLM to generate and categorize
responses across a fixed questionnaire, and presents the results in an interactive dashboard —
automating the tedious part of survey analysis, reproducibly, with no local Python setup.

## Pipeline

| Step | File | What it does |
|---|---|---|
| 1 | `1_building_json.py` | Parse the survey CSV into a structured JSON schema |
| 2 | `2_building_prompt.py` | Build the prompts that drive LLM response generation |
| 3 | `3_building_output.py` | Produce the categorized output |
| — | `pipeline.py` | Orchestrates the full flow |
| — | `dashboard.py` | Interactive Streamlit dashboard over the results |

## What's inside

- **`scripts/`** — setup, secure setup, pipeline, and dashboard helpers.
- **`Dockerfile` / `docker-compose.yml`** — containerized, no local Python required.
- **`inputs/`** — sample survey data.
- **`SECURITY.md` + `.github/workflows/security.yml`** — security notes and CI checks.

## Tech Stack

Python · OpenAI API · Streamlit · Docker.

## Quick start

```bash
./scripts/setup.sh      # one-time setup
./scripts/run.sh        # run the pipeline + dashboard
```
