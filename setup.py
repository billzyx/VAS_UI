import sys
from setuptools import setup

main_script = 'main.py'
base_options = dict(
    app=[main_script],
    options={
        'py2app': {
            'resources': ['assets', 'vas_toolkit', 'style.qss'],
            'packages': ['webdriver_manager', 'selenium', 'seleniumwire', 'ssl', 'requests']
        }
    },
)

if sys.platform == 'darwin':
    extra_options = dict(
        setup_requires=['py2app'],
    )
elif sys.platform == 'win32':
    extra_options = dict(
        setup_requires=['py2exe'],
    )
else:
    extra_options = dict(

    )

setup(
    name="VASToolBox",
    **base_options,
    **extra_options,
)
