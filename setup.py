from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
    name='osc_ne',
    packages=['osc_ne'],
    ext_modules=[Extension("osc_ne.coremidi",
        ["osc_ne/coremidi.pyx"],
        extra_link_args = [
            '-framework', 'CoreFoundation',
            '-framework', 'CoreMIDI'
    ]),],
    cmdclass = {'build_ext': build_ext}
)
