from setuptools import setup

setup(
    name='pelapost',
    version='0.1',
    py_modules=['pelapost'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        pelapost=pelapost:_main
    ''',
)
