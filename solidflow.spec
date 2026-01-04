# -*- mode: python ; coding: utf-8 -*-
#
# PyInstaller spec for SolidFlow Desktop.
# Note: packaging VTK/PyVista can be environment-specific. This spec provides a baseline.

from PyInstaller.utils.hooks import collect_submodules


block_cipher = None

hiddenimports = []
for mod in ("pyvista", "vtk", "pyvistaqt", "trimesh"):
    try:
        hiddenimports += collect_submodules(mod)
    except Exception:
        # If module is not installed in the build env, PyInstaller will fail earlier anyway.
        pass


a = Analysis(
    ["src/solidflow/__main__.py"],
    pathex=["src"],
    binaries=[],
    datas=[],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="SolidFlow",
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

app = BUNDLE(
    exe,
    name="SolidFlow.app",
    icon=None,
    bundle_identifier="com.shuldeshoff.solidflow",
)


