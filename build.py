import PyInstaller.__main__


PyInstaller.__main__.run(['--noconsole',
                          '--icon', 'application/img/b_logo.ico',
                          '--onefile',
                          'run.py'])
