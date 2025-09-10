# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/meditation_generator.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('samples', 'samples'),
        ('background_music', 'background_music'),
        ('output', 'output'),
    ],
    hiddenimports=[
        'pyttsx3',
        'pygame',
        'pydub',
        'gtts',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.scrolledtext',
        'wave',
        'tempfile',
        'subprocess',
        'threading',
        'datetime',
        'pathlib',
        're',
        'os',
        'time',
        'struct',
    ],
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
    name='MeditationGenerator',
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
    icon=None,
)
