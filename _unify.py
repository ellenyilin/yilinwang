#!/usr/bin/env python3
"""
Unify the shared design tokens across all portfolio project pages.
Changes:
  - background → #F5F2ED (warm stone)
  - bg-2      → #EDE8E1
  - border    → #C8C0B4
  - ink-1     → #1A1814
  - ink-2     → #48403A
  - ink-3     → #8A8278
  - conclusion → dark ink-1 band (text white)
  - nav style → clean flat
"""
import re, sys
from pathlib import Path

BASE = Path("/Users/wangyilin22/Downloads/portfolio_html")

# ── per-project accent colors (keep signature, only unify bg/border/ink)
ACCENTS = {
    "lyft":     "#C4156A",
    "hci":      "#D4621A",
    "berkeley": "#2B6CB0",
    "cartabio": "#3B5EA6",
    "sensetime":"#1B4D3E",
}

ACCENT_EM = {          # conclusion h2 em color (lighter/tinted of accent)
    "lyft":     "#F9A8D4",
    "hci":      "#FDBA74",
    "berkeley": "#93C5FD",
    "cartabio": "#93B4E0",
    "sensetime":"#A8D5B5",
}

def token_block(name):
    acc = ACCENTS[name]
    return f"""      --bg:      #F5F2ED;
      --bg-2:    #EDE8E1;
      --border:  #C8C0B4;
      --ink-1:   #1A1814;
      --ink-2:   #48403A;
      --ink-3:   #8A8278;
      --accent:  {acc};"""

def fix_project(name):
    path = BASE / f"{name}.html"
    html = path.read_text()

    # ── 1. Replace token block (find :root { ... }) surgically
    def replace_root_tokens(m):
        block = m.group(0)
        # replace bg / bg-2 / border / ink-1 / ink-2 / ink-3
        block = re.sub(r'--bg:\s*#[0-9A-Fa-f]{3,8}[^;]*;', '--bg:      #F5F2ED;', block)
        block = re.sub(r'--bg-2:\s*#[0-9A-Fa-f]{3,8}[^;]*;', '--bg-2:    #EDE8E1;', block)
        block = re.sub(r'--border:\s*#[0-9A-Fa-f]{3,8}[^;]*;', '--border:  #C8C0B4;', block)
        block = re.sub(r'--ink-1:\s*#[0-9A-Fa-f]{3,8}[^;]*;', '--ink-1:   #1A1814;', block)
        block = re.sub(r'--ink-2:\s*#[0-9A-Fa-f]{3,8}[^;]*;', '--ink-2:   #48403A;', block)
        block = re.sub(r'--ink-3:\s*#[0-9A-Fa-f]{3,8}[^;]*;', '--ink-3:   #8A8278;', block)
        # replace --blue / --blue-bg / --end-bg (conclusion band) with ink-1
        block = re.sub(r'--blue(?:-bg)?:\s*#[0-9A-Fa-f]{3,8}[^;]*;', '', block)
        block = re.sub(r'--end-bg:\s*#[0-9A-Fa-f]{3,8}[^;]*;', '', block)
        return block

    html = re.sub(r':root\s*\{[^}]+\}', replace_root_tokens, html, flags=re.DOTALL)

    # ── 2. Make conclusion background always var(--ink-1) dark
    html = re.sub(
        r'\.conclusion\s*\{[^}]*background:[^;]+;',
        lambda m: m.group(0).replace(
            re.search(r'background:[^;]+;', m.group(0)).group(0),
            'background: var(--ink-1);'
        ),
        html
    )
    # Fix any remaining blue-bg / end-bg references in CSS rules
    html = re.sub(r'var\(--blue-bg\)', 'var(--ink-1)', html)
    html = re.sub(r'var\(--blue\)', 'var(--ink-1)', html)
    html = re.sub(r'var\(--end-bg\)', 'var(--ink-1)', html)

    # ── 3. Fix conclusion text colors for dark background
    # h2 color → #fff, em color → accent-light
    em_color = ACCENT_EM[name]
    html = re.sub(
        r'(\.conclusion h2 em\s*\{[^}]*color:)[^;]+;',
        f'\\1 {em_color};',
        html
    )
    # make sure h2 is white on dark bg
    html = re.sub(
        r'(\.conclusion h2\s*\{[^}]*color:)\s*var\(--ink-1\)',
        '\\1 #fff',
        html
    )
    # make sure conclusion p text is readable on dark
    html = re.sub(
        r'(\.conclusion p\s*\{[^}]*color:)\s*var\(--ink-2\)',
        '\\1 rgba(255,255,255,.65)',
        html
    )
    html = re.sub(
        r'(\.conclusion p strong\s*\{[^}]*color:)\s*var\(--ink-1\)',
        '\\1 rgba(255,255,255,.9)',
        html
    )

    # ── 4. Fix outcome list items for dark bg
    html = re.sub(
        r'(\.oi \.ot\s*\{[^}]*color:)\s*var\(--ink-1\)',
        '\\1 rgba(255,255,255,.9)',
        html
    )
    html = re.sub(
        r'(\.oi \.od\s*\{[^}]*color:)\s*var\(--ink-2\)',
        '\\1 rgba(255,255,255,.5)',
        html
    )
    # outcome list borders
    html = re.sub(r'border-top:\s*1px solid rgba\(28,25,22,\.15\)',
                  'border-top: 1px solid rgba(255,255,255,.15)', html)
    html = re.sub(r'border-bottom:\s*1px solid rgba\(28,25,22,\.12\)',
                  'border-bottom: 1px solid rgba(255,255,255,.1)', html)

    # ── 5. proj-nav: use ink-1 background too, white text
    html = re.sub(r'background: var\(--blue-bg\)', 'background: var(--ink-1)', html)
    html = re.sub(r'background: var\(--end-bg\)', 'background: var(--ink-1)', html)
    # proj-nav text colors  
    html = re.sub(
        r'(\.pn-dir\s*\{[^}]*color:)\s*rgba\(28,25,22,\.[0-9]+\)',
        '\\1 rgba(255,255,255,.35)',
        html
    )
    html = re.sub(
        r'(\.pn-title\s*\{[^}]*color:)\s*var\(--ink-1\)',
        '\\1 rgba(255,255,255,.85)',
        html
    )
    html = re.sub(
        r'(\.nav-icon\s*\{[^}]*color:)\s*rgba\(28,25,22,\.[0-9]+\)',
        '\\1 rgba(255,255,255,.3)',
        html
    )
    # proj-nav border-top
    html = re.sub(
        r'border-top:\s*1px solid rgba\(168,194,224,\.[0-9]+\)',
        'border-top: 1px solid rgba(255,255,255,.1)',
        html
    )

    # ── 6. nav background (top pill nav)  
    html = re.sub(
        r'background:\s*rgba\([0-9, ]+\.(9[0-9]|8[0-9])\)',
        'background: rgba(245,242,237,.95)',
        html
    )

    path.write_text(html)
    print(f"✓ {name}.html updated")

for name in ["lyft", "hci", "berkeley", "cartabio", "sensetime"]:
    fix_project(name)

print("\nAll project pages unified.")
