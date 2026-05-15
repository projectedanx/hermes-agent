#!/bin/bash
cd tinker-atropos
source venv/bin/activate
echo "Running formatters and linters..."
black tinker_atropos/trainer.py
ruff check tinker_atropos/trainer.py
