#!/bin/bash
cd tinker-atropos
source venv/bin/activate
echo "Running tests..."
python3 -m pytest tests/ || echo "Tests dir might not exist or tests failed"
echo "Running black..."
black .
echo "Running ruff..."
ruff check .
