from setuptools import setup

setup(
    name='userassistmon',
    version="0.1.0",
    description='Monitor UserAssist in Real-time.',
    author='Matthew Seyer',
    url='https://github.com/forensicmatt/MonitorUserAssist',
    license='Apache License (2.0)',
    packages=[
        'userassist'
    ],
    python_requires='>=3',
    install_requires=[
        'ujson',
        'pywin32',
        'python-box'
    ],
    scripts=[
        'scripts/usrasst_mon.py'
    ]
)
