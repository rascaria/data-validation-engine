# Data Validation Engine

A lightweight, config driven Python ETL pipeline designed to ingest, clean and validate fleet data. 

## Features
* **Config-Driven Validation:** Business rules are separated from the main pipeline logic, making it easy to add new checks.
* **Data Quality Tracking:** Invalid records are flagged with boolean masks instead of being silently dropped, preserving data lineage.
* **Object-Oriented Flow:** Clear ETL stages (load, clean, validate and analyze) for maintainability.

## Usage
Ensure you have Python 3.12+ installed.

1. Clone the repository:
    git clone https://github.com/rascaria/data-validation-engine.git
    cd data-validation-engine

2. Run the pipeline:
    python pipeline.py

## Roadmap
* Replace basic print statements with Python's `logging` module for production monitoring.
* Add automated data and logic testing using `pytest`.
* Move validation thresholds into a YAML file to fully decouple them from the Python codebase.