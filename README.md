# StaticSiteGenerator

A Python-based static site generator that converts Markdown content into HTML websites. Built with `uv` package manager and a modular architecture for text processing, HTML generation, and site building.

---

## Quick Start: Making It Your Own

### Step 1: Update Homepage Content
Edit `content/index.md` to replace the tutorial content:

```markdown
# Your Name

Welcome to my portfolio! I'm a [your role] with experience in [technologies].

Check out my [projects](/projects) and [blog posts](/blog).
```

**Important:** Every markdown file MUST start with a single `# Heading` - this becomes the page `<title>` tag.

### Step 2: Clear Out Tutorial Content
```bash
rm -rf content/blog/*
rm -rf content/contact/
```

### Step 3: Create Your Content Structure

Recommended structure for a portfolio site:
```
content/
├── index.md                    # Homepage
├── about/
│   └── index.md               # About me page
├── projects/
│   └── index.md               # Projects listing page
└── blog/
    ├── first-post/
    │   └── index.md           # Blog post
    └── second-post/
        └── index.md           # Another post
```

**Directory → URL mapping:**
- `content/index.md` → `/` (homepage)
- `content/about/index.md` → `/about/`
- `content/blog/my-post/index.md` → `/blog/my-post/`

### Step 4: Add Your Images
```bash
cp ~/my-photo.jpg static/images/
cp ~/project-screenshot.png static/images/projects/
```

All files in `static/` are copied as-is to `docs/` during build.

### Step 5: Customize Styling
Edit `static/index.css` to change colors, fonts, layout (currently dark purple/gold theme).

### Step 6: Update Build Configuration

**For GitHub Pages at `username.github.io/repo-name`:**
```bash
# Edit build.sh
uv run python src/main.py "/repo-name"
```

**For custom domain or root deployment:**
```bash
# Edit build.sh
uv run python src/main.py "/"
```

The basepath rewrites all `/` links to `/basepath/` in generated HTML.

### Step 7: Build & Test
```bash
./main.sh          # Build and run local server on :8888
./build.sh         # Build for deployment
./test.sh          # Run unit tests
```

### Step 8: Deploy to GitHub Pages
```bash
git init
git add .
git commit -m "Initial portfolio site"
git remote add origin https://github.com/username/repo-name.git
git push -u origin main

# Enable GitHub Pages:
# Settings → Pages → Source: main branch → Folder: /docs
```

Site will be live at `https://username.github.io/repo-name/`

---

## Complete Markdown Syntax Guide

### ✅ Supported Features

#### Headings
```markdown
# Heading 1 (required - becomes page title)
## Heading 2
### Heading 3
```
**Rule:** Every markdown file MUST have exactly one `# Heading 1` at the top.

#### Paragraphs
```markdown
This is a paragraph.

This is another paragraph separated by a blank line.
```
Paragraphs are separated by blank lines (double newline).

#### Text Formatting
```markdown
**bold text**
*italic text* or _italic text_
`inline code`
```

#### Code Blocks
````markdown
```python
def hello_world():
    print("Hello, world!")
```
````
Use triple backticks. Language identifier is optional. No syntax highlighting by default.

#### Links
```markdown
[Link Text](/page)
[External Link](https://example.com)
```
- Internal links: Use absolute paths starting with `/`
- `/about` links to `content/about/index.md`
- Links are rewritten with basepath during build

#### Images
```markdown
![Alt Text](/images/photo.jpg)
![Project Screenshot](/images/projects/screenshot.png)
```
- Place images in `static/images/`
- Reference with `/images/filename.ext`
- Alt text is required for accessibility

#### Blockquotes
```markdown
> This is a blockquote.
> It can span multiple lines.
```
Start each line with `>` followed by space.

#### Lists
```markdown
# Unordered
- First item
- Second item

# Ordered
1. First step
2. Second step
```
Nested lists are NOT supported.

---

### ❌ NOT Supported (Limitations)

These markdown features will NOT render correctly:

- **Nested Lists** - Use flat lists only
- **Tables** - Use raw HTML instead (see below)
- **Task Lists** (`- [ ]`) - Use emoji workaround: `- ✅ Task`
- **Horizontal Rules** (`---`) - Use HTML: `<hr>`
- **Strikethrough** (`~~text~~`) - Not available
- **Footnotes** (`[^1]`) - Use inline parentheses
- **Definition Lists** - Use bold: `**Term:** Definition`
- **Syntax Highlighting** - Plain `<pre><code>` only (add library for highlighting)

---

### 🔧 Using Custom HTML

You CAN write raw HTML directly in markdown files:

```markdown
# My Page

<div class="custom-section">
  <p>This is raw HTML.</p>
</div>

<iframe width="560" height="315"
  src="https://www.youtube.com/embed/VIDEO_ID">
</iframe>

<hr>

<table>
  <tr><td>Cell 1</td><td>Cell 2</td></tr>
</table>
```

**Use cases:** Custom CSS classes, embedded videos, tables, horizontal rules, complex layouts.

---

## Architecture Overview

### Core Components

**Text Processing Pipeline:**
- `textnode.py`: Core text node classes and markdown parsing
  - `TextNode`: Represents text with formatting type (plain, bold, italic, code, links, images)
  - `markdown_to_html_node()`: Main conversion function from markdown to HTML nodes
  - `extract_title()`: Extracts h1 headers from markdown

**HTML Generation:**
- `htmlnode.py`: HTML node hierarchy for generating valid HTML
  - `HtmlNode`: Base class for all HTML elements
  - `LeafNode`: Terminal HTML elements (no children)
  - `ParentNode`: Container HTML elements with children

**Text Splitting:**
- `splitnodes.py`: Functions to split text nodes based on markdown delimiters
  - Handles bold, italic, code formatting, images, and links

**Site Generation:**
- `main.py`: Main site generation logic
  - `copy_static_to_public()`: Copies static assets to output directory
  - `generate_page()`: Converts single markdown file to HTML using template
  - `generate_pages_recursive()`: Processes entire content directory structure

### Content Processing Flow
1. Markdown text → `text_to_textnodes()` → TextNode objects
2. TextNode objects → `text_node_to_html_node()` → HTML node tree
3. HTML node tree → `to_html()` → HTML string
4. HTML string + template → final page

### Site Generation Flow
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

---

## Logical Next Steps

### Phase 1: Enhanced Portfolio Features
- **Navigation Menu**: Add nav bar to `template.html`
- **Footer with Social Links**: GitHub, LinkedIn, email links
- **SEO Meta Tags**: Description, Open Graph tags
- **Favicon**: Add to `static/` and reference in template

### Phase 2: Blog Enhancements
- **Blog Index Page**: Manual listing at `content/blog/index.md`
- **Post Metadata**: Add dates/tags at top of posts

### Phase 3: Advanced Features (Requires Code Changes)
- **Automatic Blog Index**: Generate blog listing from directory scan
- **RSS Feed**: Create `docs/feed.xml` from blog posts
- **Syntax Highlighting**: Add Prism.js or Highlight.js to template
- **Dark/Light Mode Toggle**: JavaScript theme switcher
- **Search Functionality**: Generate search index JSON, add client-side search
- **Tags/Categories**: Parse frontmatter, generate tag pages
- **Reading Time**: Calculate and display estimated reading time
- **Table of Contents**: Parse headings, generate TOC with anchor links

### Phase 4: Deployment & Automation
- **GitHub Actions**: Auto-build and deploy on push
- **Custom Domain**: Add CNAME file, configure DNS
- **Analytics**: Add Google Analytics or Plausible

---

## Testing Your Content

### Before You Build
```bash
./test.sh                                   # Run unit tests
grep -L "^# " content/**/*.md              # Check for missing h1 headers
```

### After You Build
```bash
./main.sh                                   # Start local server on :8888
```

**Checklist:**
- All pages load correctly
- All links work (internal and external)
- Images display properly
- Mobile responsive
- No console errors (browser DevTools)

### Common Issues

| Issue | Fix |
|-------|-----|
| "Markdown file must have a single h1 header" | Add `# Title` as first line of markdown |
| Images don't load (404 error) | Use `/images/file.jpg` not `images/file.jpg` |
| Links broken on GitHub Pages | Update basepath in `build.sh` to match repo name |
| CSS not loading | Check `template.html` has `<link href="/index.css">` |

---

## Summary

**What You Have:**
- Clean, minimal static site generator
- Markdown → HTML conversion with template system
- Static asset handling and local development server

**What It Supports:**
- Headings, paragraphs, bold, italic, code, code blocks
- Links (internal and external), images
- Blockquotes, ordered/unordered lists, raw HTML

**What It Doesn't Support:**
- Nested lists, tables (without HTML), task lists
- Strikethrough, footnotes, syntax highlighting
- Automatic blog indexes, RSS, search

**Deployment Ready:**
- GitHub Pages compatible
- Basepath support for subdirectories
- Clean URLs with `/index.html` pattern

This is a solid foundation for a personal portfolio site. Start with basic content and styling, then add advanced features as needed!
