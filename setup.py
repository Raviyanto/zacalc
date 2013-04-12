#!/usr/bin/env python
 
from distutils.core import setup
from distutils.core import setup
from distutils import cmd
from distutils.command.install_data import install_data as _install_data
from distutils.command.build import build as _build

import msgfmt
import os

class build_trans(cmd.Command):
    description = 'Compile .po files into .mo files'
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        po_dir = os.path.join(os.path.dirname(os.curdir), 'po')
        for path, names, filenames in os.walk(po_dir):
            for f in filenames:
                if f.endswith('.po'):
                    lang = f[:len(f) - 3]
                    src = os.path.join(path, f)
                    dest_path = os.path.join('build', 'locale', lang, 'LC_MESSAGES')
                    dest = os.path.join(dest_path, 'zacalc.mo')
                    if not os.path.exists(dest_path):
                        os.makedirs(dest_path)
                    if not os.path.exists(dest):
                        print 'Compiling %s' % src
                        msgfmt.make(src, dest)
                    else:
                        src_mtime = os.stat(src)[8]
                        dest_mtime = os.stat(dest)[8]
                        if src_mtime > dest_mtime:
                            print 'Compiling %s' % src
                            msgfmt.make(src, dest)

class build(_build):
    sub_commands = _build.sub_commands + [('build_trans', None)]
    def run(self):
        _build.run(self)

class install_data(_install_data):

    def run(self):
        for lang in os.listdir('build/locale/'):
            lang_dir = os.path.join('share', 'locale', lang, 'LC_MESSAGES')
            lang_file = os.path.join('build', 'locale', lang, 'LC_MESSAGES', 'zacalc.mo')
            self.data_files.append( (lang_dir, [lang_file]) )
        _install_data.run(self)

cmdclass = {
    'build': build,
    'build_trans': build_trans,
    'install_data': install_data,
}

SCRIPTS=  ['data/zacalc']

DATA = [('share/applications', ['data/zacalc.desktop']),
        ('share/icons', ['data/zacalc.png']),
        ('share/zacalc', ['data/logo.png']),
        ('lib/zacalc', ['src/zacalc.py', 'src/i18n.py'])]
 
setup(name         = 'zacalc',
      version      = '1.3',
      description  = 'zakat calculator',
      author       = 'Fitra Aditya',
      author_email = '<fitra@idmail.or.id>',
      url          = 'http://dev.blankonlinux.or.id/bzr/rote/zacalc',
      license      = 'GPL v3',
      data_files   = DATA,
      scripts      = SCRIPTS,
      cmdclass     = cmdclass
      )
