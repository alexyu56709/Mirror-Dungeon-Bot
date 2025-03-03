# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Bot.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('ObjectDetection\\UI\\*.png', 'ObjectDetection\\UI'),
        ('ObjectDetection\\UI\\battle\\*.png', 'ObjectDetection\\UI\\battle'),
        ('ObjectDetection\\UI\\battle\\sins\\*.png', 'ObjectDetection\\UI\\battle\\sins'),
        ('ObjectDetection\\UI\\end\\*.png', 'ObjectDetection\\UI\\end'),
        ('ObjectDetection\\UI\\event\\*.png', 'ObjectDetection\\UI\\event'),
        ('ObjectDetection\\UI\\event\\sinprob\\*.png', 'ObjectDetection\\UI\\event\\sinprob'),
        ('ObjectDetection\\UI\\grab\\*.png', 'ObjectDetection\\UI\\grab'),
        ('ObjectDetection\\UI\\grab\\card\\*.png', 'ObjectDetection\\UI\\grab\\card'),
        ('ObjectDetection\\UI\\grab\\levels\\*.png', 'ObjectDetection\\UI\\grab\\levels'),
        ('ObjectDetection\\UI\\pack\\*.png', 'ObjectDetection\\UI\\pack'),
        ('ObjectDetection\\UI\\path\\*.png', 'ObjectDetection\\UI\\path'),
        ('ObjectDetection\\UI\\shop\\*.png', 'ObjectDetection\\UI\\shop'),
        ('ObjectDetection\\UI\\start\\*.png', 'ObjectDetection\\UI\\start'),
        ('ObjectDetection\\UI\\teams\\Burn\\*.png', 'ObjectDetection\\UI\\teams\\Burn'),
        ('ObjectDetection\\UI\\teams\\Burn\\buy\\*.png', 'ObjectDetection\\UI\\teams\\Burn\\buy'),
        ('ObjectDetection\\UI\\teams\\Burn\\gifts\\*.png', 'ObjectDetection\\UI\\teams\\Burn\\gifts')
    ],
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
    name='CGrinder',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['app_icon.ico'],
)
