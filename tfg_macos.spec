# -*- mode: python -*-
block_cipher = None
a = Analysis(['src/main.py'],
             pathex=['src'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Test Files Generator',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='Test Files Generator')
app = BUNDLE(coll,
             name='Test Files Generator.app',
             icon='icon/icon.icns',
             info_plist={
                'LSUIElement': '1',
                'NSHighResolutionCapable': 'True',
                'CFBundleDisplayName': 'Test Files Generator',
                'CFBundleDisplayName': 'Test Files Generator',
                'CFBundleShortVersionString': '1.0.0',
                'NSHumanReadableCopyright': '2019, Mat Muller'
             },
             )