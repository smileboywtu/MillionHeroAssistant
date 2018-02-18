# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['/Users/icarus/workspace/bake/MillionHeroAssistant'],
             binaries=[
                ("C:\\python36\\Lib\\site-packages\\scipy\\extra-dll\\", ".")
             ],
             datas=[
		        ("drivers", "drivers"),
		        ("adb", "adb"),
		        ("resources/dict.txt", "jieba"),
                ("resources", "resources"),
                ("screenshots", "screenshots"),
                ("config.yaml", ".")
	         ],
             hiddenimports=[
                "scipy._lib.messagestream",
                "pywt._extensions._cwt"
             ],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='AssistantExecutor',
          debug=False,
          strip=True,
          upx=True,
          console=True,
          window=True)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='main')
