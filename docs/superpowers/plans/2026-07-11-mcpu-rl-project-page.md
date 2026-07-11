# MCP-Universe RL Project Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a polished, responsive project page at `/mcpu-rl/` that explains the EMNLP 2026 System Demonstrations submission using the current paper's claims, figures, and results.

**Architecture:** Add one dependency-free static HTML page and a colocated asset directory. The page follows the existing MCP-Universe visual system but remains isolated from the benchmark homepage; paper figures are rasterized for reliable browser rendering.

**Tech Stack:** Semantic HTML5, inline CSS, minimal vanilla JavaScript, existing Google Fonts and Font Awesome includes, PNG assets generated with Poppler.

## Global Constraints

- The public route is exactly `/mcpu-rl/`.
- The only primary external call to action is the MCP-Universe RL GitHub repository.
- Do not add Paper, arXiv, PDF, or Screencast links or placeholders.
- Label the work “EMNLP 2026 System Demonstrations Submission”; do not imply acceptance.
- Derive technical claims and numbers from the current MCP-RL paper.
- Keep the existing root homepage and its other pages unchanged.
- Support desktop and mobile layouts, keyboard navigation, reduced motion, and descriptive image alt text.

---

### Task 1: Prepare Web Figure Assets

**Files:**
- Create: `mcpu-rl/assets/overview.png`
- Create: `mcpu-rl/assets/pipeline.png`
- Create: `mcpu-rl/assets/curve-swe.png`
- Create: `mcpu-rl/assets/curve-research.png`
- Create: `mcpu-rl/assets/curve-tool-use.png`
- Create: `mcpu-rl/assets/throughput.png`

**Interfaces:**
- Consumes: The six committed PDF figures in the MCP-RL paper repository.
- Produces: Browser-compatible PNGs referenced by `mcpu-rl/index.html`.

- [ ] **Step 1: Create the asset directory**

Run:

```bash
mkdir -p mcpu-rl/assets
```

- [ ] **Step 2: Rasterize each paper figure**

Run from the website repository:

```bash
pdftoppm -png -r 180 -singlefile ../MCP-RL/figures/MCP-U-RL.pdf mcpu-rl/assets/overview
pdftoppm -png -r 180 -singlefile ../MCP-RL/figures/MCP-U-RL-Decouple.pdf mcpu-rl/assets/pipeline
pdftoppm -png -r 180 -singlefile ../MCP-RL/figures/curve_swe.pdf mcpu-rl/assets/curve-swe
pdftoppm -png -r 180 -singlefile ../MCP-RL/figures/curve_dr.pdf mcpu-rl/assets/curve-research
pdftoppm -png -r 180 -singlefile ../MCP-RL/figures/curve_awm.pdf mcpu-rl/assets/curve-tool-use
pdftoppm -png -r 180 -singlefile ../MCP-RL/figures/decouple.pdf mcpu-rl/assets/throughput
```

- [ ] **Step 3: Verify all generated assets**

Run:

```bash
for image in mcpu-rl/assets/*.png; do test -s "$image" || exit 1; done
```

Expected: exit code 0 and six non-empty PNG files.

### Task 2: Build the Static Landing Page

**Files:**
- Create: `mcpu-rl/index.html`

**Interfaces:**
- Consumes: `mcpu-rl/assets/*.png`, `../logos/mcp-universe-icon.png`, and the public GitHub URL.
- Produces: The complete page served by GitHub Pages at `/mcpu-rl/`.

- [ ] **Step 1: Write structural assertions before the page exists**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
page = Path("mcpu-rl/index.html")
assert not page.exists(), "Expected the landing page to be absent before implementation"
PY
```

Expected: exit code 0.

- [ ] **Step 2: Implement semantic page structure**

Create `mcpu-rl/index.html` with:

```html
<header>Back-to-MCP-Universe navigation and a GitHub action</header>
<main>
  <section id="hero">Submission badge, title, authors, one-sentence thesis, GitHub button</section>
  <section id="problem">The environment- and rollout-orchestration bottlenecks</section>
  <section id="architecture">Overview figure and three reusable layer cards</section>
  <section id="pipeline">Acquire → Run → Eval explanation and pipeline figure</section>
  <section id="domains">Software engineering, deep research, and general tool-use result cards</section>
  <section id="throughput">2.8× rollout and approximately 2× end-to-end throughput evidence</section>
  <section id="opensource">Apache-2.0 release statement and GitHub button</section>
</main>
<footer>MCP-Universe RL and Salesforce AI Research attribution</footer>
```

Use the exact paper title, author list, and GitHub URL:

```text
MCP-Universe RL: A Framework for Training MCP Tool-Use Agents via Reinforcement Learning
https://github.com/SalesforceAIResearch/MCP-Universe/tree/main/mcpuniverse/rl
```

- [ ] **Step 3: Implement the visual system**

Add inline CSS using the existing site's Salesforce palette (`#0d9dda`, `#0176a3`), Salesforce Sans/Inter typography, restrained gradients, white cards, subtle borders, and generous whitespace. Add responsive breakpoints for 900px and 640px, visible focus states, `prefers-reduced-motion`, fluid images, and a single-column mobile layout.

- [ ] **Step 4: Add minimal progressive enhancement**

Add inline JavaScript that updates the current year and applies reveal classes through `IntersectionObserver`; keep all content visible when JavaScript is unavailable.

- [ ] **Step 5: Verify required content and forbidden links**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
html = Path("mcpu-rl/index.html").read_text()
required = [
    "MCP-Universe RL",
    "EMNLP 2026 System Demonstrations Submission",
    "Environment Orchestration",
    "Rollout Orchestration",
    "Training Engine",
    "Software Engineering",
    "Deep Research",
    "General Tool Use",
    "2.8×",
    "SalesforceAIResearch/MCP-Universe",
]
for text in required:
    assert text in html, text
for forbidden in ["Paper</a>", "Screencast", "Coming Soon"]:
    assert forbidden not in html, forbidden
PY
```

Expected: exit code 0.

### Task 3: Validate the Page Locally

**Files:**
- Verify: `mcpu-rl/index.html`
- Verify: `mcpu-rl/assets/*.png`

**Interfaces:**
- Consumes: The completed static page and assets.
- Produces: Evidence that the GitHub Pages route renders correctly without broken local resources.

- [ ] **Step 1: Validate HTML**

Run:

```bash
npx --yes html-validate mcpu-rl/index.html
```

Expected: 0 errors.

- [ ] **Step 2: Start a local static server**

Run:

```bash
python3 -m http.server 8000
```

Expected: `http://localhost:8000/mcpu-rl/` returns HTTP 200.

- [ ] **Step 3: Check local references**

Run in another terminal:

```bash
python3 - <<'PY'
from html.parser import HTMLParser
from pathlib import Path

class Sources(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ("src", "href"):
            value = attrs.get(key, "")
            if value and not value.startswith(("http:", "https:", "#", "mailto:")):
                self.paths.append(value)

parser = Sources()
parser.feed(Path("mcpu-rl/index.html").read_text())
base = Path("mcpu-rl")
for reference in parser.paths:
    target = (base / reference).resolve()
    assert target.exists(), f"Missing local resource: {reference}"
PY
```

Expected: exit code 0.

- [ ] **Step 4: Perform responsive browser review**

Open `http://localhost:8000/mcpu-rl/` at 1440×900 and 390×844. Verify the hero and GitHub action are visible, all six figures load, navigation remains usable, text never clips or overflows, no horizontal scrollbar appears, and the browser console has no errors.

- [ ] **Step 5: Review the final diff**

Run:

```bash
git status --short
git diff --check
```

Expected: only the new `mcpu-rl/` page, its six assets, and this plan appear; no whitespace errors.
