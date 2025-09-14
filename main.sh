#!/bin/bash
uv run python -m src.main
cd docs && python3 -m http.server 8888
