#!/bin/bash

# Create and activate virtual environment
python3 -m venv bibtex_analysis
source bibtex_analysis/bin/activate

# Install dependencies
pip install -r requirements.txt

echo "Environment setup complete."