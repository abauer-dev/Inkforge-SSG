# Inkforge

A static site generator built from scratch in Python. Markdown in, HTML out — no frameworks, no dependencies, no magic.

You can see my statics sites deployed on Github Pagese: https://abauer-dev.github.io/Inkforge-SSG/

## What it does

Inkforge walks a `content/` directory of Markdown files, parses them with a hand-rolled markdown engine, slots the result into a template, and writes a complete static site to `content/`. It handles all the usual suspects:

- Inline formatting: **bold**, _italic_, `code`, links, images
- Block elements: headings, code blocks, blockquotes, ordered and unordered lists, paragraphs
- A single `template.html` shared across every page
- Configurable basepath for GitHub Pages deployment

Roughly 500 lines of Python. Zero external packages.

## Why

Every static site generator on earth — Hugo, Jekyll, Eleventy, Next — does some version of the same dance: parse markdown, convert to HTML, slot into a template, write the file. Building one from scratch turns the magic into an algorithm.

It's also a satisfying thing to own: a working tool you understand line-by-line.

## Quick start

```bash
git clone https://github.com/abauer-dev/inkforge.git
cd inkforge
./main.sh
```

Then open `http://localhost:8888`.

## Project layout

```
inkforge/
├── content/         # your markdown
│   ├── index.md
│   └── blog/
│       └── post.md
├── static/          # CSS, images, anything copied as-is
├── template.html    # wraps every generated page
├── src/             # the generator
└── public/          # generated output (gitignored)
```

## Writing content

Drop Markdown files anywhere under `content/`. The folder structure is preserved in the output:

```
content/blog/post1/index.md  →  docs/blog/post1/index.html
```

A page can use the full markdown vocabulary:

```markdown
# My Post

This has **bold** and _italic_ and `code`.

> A pull quote.

- one
- two
- three

[Read more](/blog/post2/) — and an ![image](/images/logo.png).
```

The first `# heading` becomes the `<title>` tag automatically.

## Build modes

**Local development** — basepath defaults to `/`:

```bash
./main.sh
```

**Production for GitHub Pages** — pass the repo name as basepath:

```bash
./build.sh
```

Inside `build.sh`:

```bash
python3 src/main.py "your-repo-name"
```

Every `href="/..."` and `src="/..."` in the generated HTML is rewritten with this prefix, so links keep working when the site is served from a subdirectory.

## Running the tests

```bash
./test.sh
```

The test suite covers the markdown parser end-to-end: inline splitting, block classification, HTML generation, and the full pipeline.

## Contributing

This is a learning project, but PRs and issue reports are welcome — especially edge cases the hand-rolled markdown parser fails on.
