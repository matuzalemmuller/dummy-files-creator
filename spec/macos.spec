# -*- mode: python -*-
block_cipher = None
a = Analysis(['../src/dummy_files_creator.py'],
             pathex=['src'],
             binaries=[],
             datas=[
                    ('../icon/icon.png','icon')
                   ],
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
          name='dummy-files-creator-darwin',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='dummy-files-creator-darwin')
app = BUNDLE(coll,
             name='Dummy Files Creator.app',
             icon='../icon/icon.icns',
             info_plist={
                'LSBackgroundOnly': 'False',
                'NSHighResolutionCapable': 'True',
                'CFBundleDisplayName': 'Dummy Files Creator',
                'CFBundleShortVersionString': '1.2.0',
                'NSHumanReadableCopyright': '2019, Mat Muller'
             },
             )