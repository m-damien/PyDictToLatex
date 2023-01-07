from setuptools import setup

setup(
    name='pydict2latex',
    version='0.0.1',    
    description='Acces python dictionaries from latex',
    url='',
    author='Damien Masson',
    license='BSD 2-clause',
    packages=['pydict2latex'],
    install_requires=['numpy'],

    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: OS Independent',     
        "Topic :: Text Processing :: Markup :: LaTeX"   
    ],
)