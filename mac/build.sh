#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [ ! -f credentials.json ]; then
    echo "ERROR: credentials.json not found in project root."
    echo "Download from Google Cloud Console and save it here before building."
    exit 1
fi

if [ -d .venv ]; then
    # shellcheck disable=SC1091
    source .venv/bin/activate
fi

pip install pyinstaller

if [ ! -f assets/icon.icns ]; then
    echo "Generating assets/icon.icns from assets/icon.png..."
    ICONSET="assets/icon.iconset"
    rm -rf "$ICONSET"
    mkdir -p "$ICONSET"
    sips -z 16 16 assets/icon.png --out "$ICONSET/icon_16x16.png" >/dev/null
    sips -z 32 32 assets/icon.png --out "$ICONSET/icon_16x16@2x.png" >/dev/null
    sips -z 32 32 assets/icon.png --out "$ICONSET/icon_32x32.png" >/dev/null
    sips -z 64 64 assets/icon.png --out "$ICONSET/icon_32x32@2x.png" >/dev/null
    sips -z 128 128 assets/icon.png --out "$ICONSET/icon_128x128.png" >/dev/null
    sips -z 256 256 assets/icon.png --out "$ICONSET/icon_128x128@2x.png" >/dev/null
    sips -z 256 256 assets/icon.png --out "$ICONSET/icon_256x256.png" >/dev/null
    sips -z 512 512 assets/icon.png --out "$ICONSET/icon_256x256@2x.png" >/dev/null
    sips -z 512 512 assets/icon.png --out "$ICONSET/icon_512x512.png" >/dev/null
    sips -z 1024 1024 assets/icon.png --out "$ICONSET/icon_512x512@2x.png" >/dev/null
    iconutil -c icns "$ICONSET" -o assets/icon.icns
    rm -rf "$ICONSET"
fi

pyinstaller mac/AutoMeet-mac.spec

echo ""
echo "Built dist/AutoMeet.app"
echo "Zip and upload to GitHub Releases as AutoMeet-mac.zip"
