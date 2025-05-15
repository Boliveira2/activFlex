# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[],
    hiddenimports=[
        # Dependências internas
        'scripts.gui',
        'scripts.leitor',
        'scripts.processador_new',
        'scripts.relatorio_new',

        'pyexcel_io',
        'pyexcel_io.writers.csv_in_file',
        'pyexcel_io.plugins',
        'pyexcel_io.plugins.csvw',
        'pyexcel_io.plugins.csvw.writer',


        # Bibliotecas externas usadas diretamente
        'tkinter',
        'pandas',
        'pyexcel',
        'pyexcel_ods',
        'pyexcel_ods3',
        'odf',
        'odf.opendocument',
        'odf.style',
        'odf.table',
        'odf.text',
        'openpyxl',
        'xlrd',

        # Componentes adicionais do tkinter usados explicitamente
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.ttk',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ActivFlex',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # True se quiser consola visível
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ActivFlex',
)
