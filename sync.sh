#!/usr/bin/env bash
# Copies built fonts from dist/ into the sibling projects that consume them.
# Run after build.sh whenever the fonts change.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
PARENT="$(dirname "$ROOT")"

cp -f "$ROOT"/dist/ttf/*.ttf    "$PARENT/SteppeKings/Assets/UI/Fonts/"
cp -f "$ROOT"/dist/web/*.woff*  "$PARENT/SteppeKingsWeb/public/fonts/"

echo "Synced:"
echo "  dist/ttf/*.ttf   -> SteppeKings/Assets/UI/Fonts/"
echo "  dist/web/*.woff* -> SteppeKingsWeb/public/fonts/"
