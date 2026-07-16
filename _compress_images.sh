#!/bin/bash
# Compress all images in assets/ for web
# - PNGs: resize to max 1600px on longest side, re-compress
# - JPGs: resize to max 1600px, quality 70

cd /Users/wangyilin22/Downloads/portfolio_html

echo "=== Before compression ==="
du -sh assets/
echo ""

echo "=== Compressing PNGs ==="
for f in assets/*.png; do
  [ -f "$f" ] || continue
  sips -Z 1600 "$f" --out "$f" > /dev/null 2>&1
  echo "  done: $(basename "$f")"
done

echo ""
echo "=== Compressing JPGs ==="
for f in assets/*.jpg; do
  [ -f "$f" ] || continue
  sips -Z 1600 -s formatOptions 70 "$f" --out "$f" > /dev/null 2>&1
  echo "  done: $(basename "$f")"
done

echo ""
echo "=== After compression ==="
du -sh assets/
echo ""
echo "=== Individual file sizes (sorted) ==="
ls -lhS assets/*.png assets/*.jpg 2>/dev/null | awk '{print $5, $9}'
