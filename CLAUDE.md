# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based static site generator that converts Markdown content into HTML websites. The project uses the `uv` package manager for Python dependency management and follows a modular architecture with separate components for text processing, HTML generation, and site building.

## Development Commands

### Testing
```bash
./test.sh
# Or directly: uv run python -m unittest discover -s src
```

### Building the Site
```bash
./build.sh
# Or directly: uv run python src/main.py "/StaticSiteGenerator"
```

### Development Server
```bash
./main.sh
# Builds the site and starts a local HTTP server on port 8888
```

## Architecture Overview

### Core Components

**Text Processing Pipeline:**
- `textnode.py`: Core text node classes and markdown parsing
  - `TextNode`: Represents text with formatting type (plain, bold, italic, code, links, images)
  - `TextType`: Enum for different text formatting types
  - `markdown_to_html_node()`: Main conversion function from markdown to HTML nodes
  - `extract_title()`: Extracts h1 headers from markdown

**HTML Generation:**
- `htmlnode.py`: HTML node hierarchy for generating valid HTML
  - `HtmlNode`: Base class for all HTML elements
  - `LeafNode`: Terminal HTML elements (no children)
  - `ParentNode`: Container HTML elements with children

**Text Splitting:**
- `splitnodes.py`: Functions to split text nodes based on markdown delimiters
  - `split_nodes_delimiter()`: Handles bold, italic, code formatting
  - `split_nodes_image()`: Processes markdown image syntax
  - `split_nodes_link()`: Processes markdown link syntax

**Site Generation:**
- `main.py`: Main site generation logic
  - `copy_static_to_public()`: Copies static assets to output directory
  - `generate_page()`: Converts single markdown file to HTML using template
  - `generate_pages_recursive()`: Processes entire content directory structure

### Key Workflows

**Content Processing Flow:**
1. Markdown text → `text_to_textnodes()` → TextNode objects
2. TextNode objects → `text_node_to_html_node()` → HTML node tree
3. HTML node tree → `to_html()` → HTML string
4. HTML string + template → final page

**Site Generation Flow:**
1. Clean/create output directory (`docs/`)
2. Copy static assets (`static/` → `docs/`)
3. Process all markdown files in `content/` directory recursively
4. Apply `template.html` with title and content substitution
5. Support for custom base paths for deployment

### Directory Structure
- `content/`: Markdown source files (mirrors final site structure)
- `static/`: Static assets (images, CSS) copied to output
- `docs/`: Generated HTML output directory
- `src/`: Python source code modules
- `template.html`: HTML template with `{{ Title }}` and `{{ Content }}` placeholders

### Testing
The project uses Python's built-in `unittest` framework with test files following the `test_*.py` naming convention. Tests cover the core text processing and HTML generation functionality.