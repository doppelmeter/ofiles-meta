from setuptools import setup

setup(
    name='ofiles_meta',
    version='0.1.1',
    packages=['build.lib.ofiles_meta', 'build.lib.ofiles_meta.ocad', 'build.lib.ofiles_meta.mapper', 'ofiles_meta'],
    url='https://github.com/huema-ch/ofiles-meta',
    license='MIT',
    author='Marius Hürzeler',
    author_email='huerzeler.marius@gmail.com',
    description='provide functions to analyze files related to orienteering'
)
