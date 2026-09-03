#!/usr/bin/env bash
set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "🚀 Building Bengutas fonts directly from bengutas.pen..."

fontforge -lang=py -script "$PROJECT_DIR/src/build.py"

echo "📦 Packaging distribution archive..."
cd "$PROJECT_DIR"
zip -q -r docs/bengutas-fonts.zip dist/
cp docs/bengutas-fonts.zip ~/Desktop/SteppeKingsSans_Fonts.zip 2>/dev/null || true

echo "🔄 Updating system fonts (~/.local/share/fonts/Bengutas/)..."
mkdir -p ~/.local/share/fonts/Bengutas
cp "$PROJECT_DIR"/dist/ttf/* ~/.local/share/fonts/Bengutas/
fc-cache -f ~/.local/share/fonts/Bengutas/ >/dev/null 2>&1 || true

if [ -d "$PROJECT_DIR/../SteppeKings/Assets/UI/Fonts" ]; then
  echo "🎮 Updating Unity project fonts..."
  cp "$PROJECT_DIR"/dist/ttf/* "$PROJECT_DIR/../SteppeKings/Assets/UI/Fonts/"
fi

echo "✨ All fonts successfully compiled, packaged, and installed!"
