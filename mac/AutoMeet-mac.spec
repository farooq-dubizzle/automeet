# -*- mode: python ; coding: utf-8 -*-

import os

ROOT = os.path.abspath(os.path.join(SPECPATH, ".."))

a = Analysis(
    [os.path.join(SPECPATH, "main.py")],
    pathex=[ROOT],
    binaries=[],
    datas=[
        (os.path.join(ROOT, "assets"), "assets"),
        (os.path.join(ROOT, "credentials.json"), "."),
    ],
    hiddenimports=[
        "calendar_client",
        "mac",
        "mac.auth",
        "mac.config",
        "mac.platform",
        "mac.scheduler",
        "mac.tray_app",
        "google.auth",
        "google_auth_oauthlib",
        "googleapiclient",
        "googleapiclient.discovery",
        "pystray",
        "PIL",
        "PIL.Image",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="AutoMeet",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="AutoMeet",
)

app = BUNDLE(
    coll,
    name="AutoMeet.app",
    icon=os.path.join(ROOT, "assets", "icon.icns"),
    bundle_identifier="com.automeet.app",
    info_plist={
        "LSUIElement": True,
        "CFBundleName": "AutoMeet",
        "CFBundleDisplayName": "AutoMeet",
    },
)
