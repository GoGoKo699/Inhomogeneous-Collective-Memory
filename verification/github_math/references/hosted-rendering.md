# Checking the mathematics displayed by GitHub

The collector compares every mathematical expression in a pinned set of Markdown files with the actual GitHub rendering of that same commit. It supplements the [scientific numerical checks](../../README.md); it does not establish the truth of a proof or replace visual inspection.

## Reproduce a capture

Use Node.js 18 or newer, Python 3.10 or newer, Git, Playwright and MathJax. Install the browser dependencies in a temporary directory outside the checkout. The workflow uses Playwright 1.56.1 and MathJax 3.2.1.

```bash
npm install --prefix /absolute/temporary/dependencies playwright@1.56.1 mathjax-full@3.2.1
/absolute/temporary/dependencies/node_modules/.bin/playwright install chromium
NODE_PATH=/absolute/temporary/dependencies/node_modules node verification/github_math/scripts/capture_hosted_math.cjs \
  --root /absolute/scientific-checkout \
  --repository GoGoKo699/Inhomogeneous-Collective-Memory \
  --revision FULL_40_CHARACTER_COMMIT \
  --output /absolute/new-empty-evidence-directory
```

Replace the illustrative paths and revision with actual values. The commit must exist in the checkout and have public commit-pinned GitHub pages. The browser is anonymous; the collector does not sign in or retrieve private content. A transport or access failure remains a failed check.

The default scope is every tracked Markdown file in that commit. Repeated `--page PATH` options can declare a deliberately smaller diagnostic sample, which must not be reported as full-repository coverage. The collector reads Git objects, so uncommitted edits are not included.

## What the output establishes

The source inventory records page and expression hashes. MathJax compiles each source expression locally to provide a comparison target. Chromium then visits the real GitHub pages at viewport widths 1440 and 760, captures their mathematical structures, and checks counts, symbols, fractions, scripts, relations and display geometry. It saves the actual page HTML, full-page screenshots, structural captures, comparison results and a `hosted-report.json` with artifact hashes.

Exit zero means those automated comparisons passed for that exact revision and page scope. Source compilation alone is not hosted evidence. Inspect the screenshots separately for the main claims, substantial equations, tables, learning pages and any repaired content. A structural pass does not certify every pixel, non-mathematical layout, other browser versions, or future changes to GitHub's renderer.

The [Actions workflow](../../../.github/workflows/hosted-math.yml) runs on pull requests with `contents: read`, checks out the explicit proposed head commit without retained Git credentials, and uploads evidence even when comparison fails. It has no repository-write step and requires no secret. Its artifacts expire after the configured retention period; they are reproducible diagnostics, not permanent scientific records.

[Verification overview](../../README.md) · [Collector](../scripts/capture_hosted_math.cjs) · [Source and capture checker](../scripts/check_rendered_math.py)
