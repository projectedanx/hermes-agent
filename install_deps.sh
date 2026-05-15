#!/bin/bash
cd tinker-atropos
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
