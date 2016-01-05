from setuptools import setup

setup(
    name='plot_joblog',
    version='1.0.0',
    description='Produce a time chart of the jobs ran by GNU parallel',
    author='Maurizio Tomasi',
    author_email='ziotom78@gmail.com',
    py_modules=['plot_joblog'],
    install_requires=[
        'Click',
    ],
    url='https://github.com/ziotom78/plot_joblog',
    license='MIT',
    keywords='plot cli gnuparallel',
    entry_points='''
        [console_scripts]
        plot_joblog=plot_joblog:main
    ''',
)
