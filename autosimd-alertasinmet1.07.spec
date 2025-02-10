# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['autosimd-alertasinmet1.07.py'],
    pathex=[],
    binaries=[],
    datas=[('D:\\07_GEOPROCESSAMENTO\\AUTOMATIZAÇÃO\\Executavel\\V1.07\\icones\\*', 'icones'), ('chromedriver.exe', '.')],
    hiddenimports=[],
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
    a.binaries,
    a.datas,
    [],
    name='autosimd-alertasinmet1.07',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['D:\\07_GEOPROCESSAMENTO\\AUTOMATIZAÇÃO\\Executavel\\V1.07\\icones\\Log_Sala_BM.ico'],
)
