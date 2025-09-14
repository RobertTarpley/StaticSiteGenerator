#!/bin/bash
uv run python -m src.main
cd public && python3 -m http.server 8888
