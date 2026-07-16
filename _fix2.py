#!/usr/bin/env python3
"""
Fix pass:
1. Remove all border-radius → flat/sharp (0) everywhere
2. Berkeley conclusion → light steel-blue #D6E8F4 (not dark)
3. Lighten all dark blacks → softer charcoal / tinted darks
"""
import re
from pathlib import Path

BASE = Path("/Users/wangyilin22/Downloads/portfolio_html")

# ─── Project-specific conclusion colors (not jet-black) ───────────────────────
CONCLUSION_BG = {
    "lyft":      "#2A1A20",   # dark plum-rose
    "hci":       "#2A1E12",   # dark warm brown
    "berkeley":  "#D6E8F4",   # ← LIGHT STEEL BLUE (user request)
    "cartabio":  "#1A2540",   # deep navy
    "sensetime": "#0E2E20",   # deep forest
}

CONCLUSION_INK = {          # text color inside conclusion
    "berkeley":  "var(--ink-1)",   # dark text on light bg
}

# ─── 1. Strip ALL border-radius from a CSS string ─────────────────────────────
def strip_radius(css):
    # set all border-radius values to 0
    css = re.sub(r'border-radius:\s*[^;]+;', 'border-radius: 0;', css)
    # also handle --r / --r-lg / --r-sm variables
    css = re.sub(r'--r(?:-sm|-lg)?:\s*[0-9]+px;', lambda m: re.sub(r'[0-9]+px', '0', m.group(0)), css)
    return css

# ─── 2. Lighten raw black hex values (but keep white) ─────────────────────────
def soften_blacks(html):
    # pure #000 → keep, but #1A1814 style jet-blacks used for backgrounds → soften
    # We replace the ink-1 root token to a softer charcoal
    html = re.sub(r'--ink-1:\s*#1A1814;', '--ink-1:   #1E1B18;', html)
    # body text color stays, but bg/footer heavy blacks: replace raw very-dark hex
    # in conclusion/stat-band background rules only
    return html

def fix(name):
    path = BASE / f"{name}.html"
    html = path.read_text()

    # ── border-radius: strip from all <style> blocks
    def process_style(m):
        return strip_radius(m.group(0))
    html = re.sub(r'<style>.*?</style>', process_style, html, flags=re.DOTALL)

    # ── conclusion background: per-project color
    bg = CONCLUSION_BG.get(name)
    if bg:
        html = re.sub(
            r'(\.conclusion\s*\{[^}]*)background:[^;]+;',
            lambda m: m.group(1) + f'background: {bg};',
            html
        )
        # Also fix proj-nav (bottom nav band) to match
        html = re.sub(
            r'(\.proj-nav\s*\{[^}]*)background:[^;]+;',
            lambda m: m.group(1) + f'background: {bg};',
            html
        )

    # ── Berkeley special: text colors → dark (light bg)
    if name == "berkeley":
        html = re.sub(
            r'(\.conclusion h2\s*\{[^}]*)color:\s*#fff',
            r'\1color: var(--ink-1)',
            html
        )
        html = re.sub(
            r'(\.c-eyebrow\s*\{[^}]*)color:\s*rgba\(255,255,255,\.[0-9]+\)',
            r'\1color: var(--ink-3)',
            html
        )
        html = re.sub(
            r'(\.conclusion p\s*\{[^}]*)color:\s*rgba\(255,255,255,\.[0-9]+\)',
            r'\1color: var(--ink-2)',
            html
        )
        html = re.sub(
            r'(\.conclusion p strong\s*\{[^}]*)color:\s*rgba\(255,255,255,\.[0-9]+\)',
            r'\1color: var(--ink-1)',
            html
        )
        # outcome items
        html = re.sub(
            r'(\.oi \.ot\s*\{[^}]*)color:\s*rgba\(255,255,255,\.[0-9]+\)',
            r'\1color: var(--ink-1)',
            html
        )
        html = re.sub(
            r'(\.oi \.od\s*\{[^}]*)color:\s*rgba\(255,255,255,\.[0-9]+\)',
            r'\1color: var(--ink-2)',
            html
        )
        # borders
        html = re.sub(r'border-top:\s*1px solid rgba\(255,255,255,\.15\)',
                      'border-top: 1px solid rgba(28,25,22,.15)', html)
        html = re.sub(r'border-bottom:\s*1px solid rgba\(255,255,255,\.1\)',
                      'border-bottom: 1px solid rgba(28,25,22,.1)', html)
        # proj-nav text
        html = re.sub(
            r'(\.pn-dir\s*\{[^}]*)color:\s*rgba\(255,255,255,\.[0-9]+\)',
            r'\1color: rgba(28,25,22,.4)',
            html
        )
        html = re.sub(
            r'(\.pn-title\s*\{[^}]*)color:\s*rgba\(255,255,255,\.[0-9]+\)',
            r'\1color: var(--ink-1)',
            html
        )
        html = re.sub(
            r'(\.nav-icon\s*\{[^}]*)color:\s*rgba\(255,255,255,\.[0-9]+\)',
            r'\1color: rgba(28,25,22,.3)',
            html
        )
        html = html.replace(
            'border-top: 1px solid rgba(255,255,255,.1)',
            'border-top: 1px solid rgba(28,25,22,.12)'
        )
        # proj-nav hover
        html = re.sub(r"a:hover \.pn-title \{ color: #A8D5B5; \}",
                      "a:hover .pn-title { color: var(--accent); }", html)
        html = re.sub(r"a:hover \.nav-icon \{ color: #A8D5B5; \}",
                      "a:hover .nav-icon { color: var(--accent); }", html)

    # ── index: stat-band keep dark, but soften by using #1E1B18
    if name == "index":
        html = re.sub(r'background: var\(--ink-1\)', 'background: #1E1B18', html)
        html = html.replace('background: #1A1814', 'background: #1E1B18')

    path.write_text(html)
    print(f"✓ {name}.html")

# Project pages
for name in ["lyft", "hci", "berkeley", "cartabio", "sensetime"]:
    fix(name)

# index.html: just strip radius
path = BASE / "index.html"
html = path.read_text()
html = re.sub(r'<style>.*?</style>',
              lambda m: strip_radius(m.group(0)), html, flags=re.DOTALL)
path.write_text(html)
print("✓ index.html")

print("\nAll done.")
