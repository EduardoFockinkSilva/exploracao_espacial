# setup.py

from setuptools import setup, find_packages

setup(
    name='simulador_sistema_solar',
    version='1.0.0',
    description='Simulador de sistema solar em 3D com foguete controlável e algoritmo A* para rotas otimizadas.',
    author='Eduardo Fockink Silva',
    author_email='seuemail@exemplo.com',
    url='https://github.com/seuusuario/simulador_sistema_solar',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
        'pygame',
        'PyOpenGL',
        'pytest',
        'networkx',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'simulador_sistema_solar=main:main',
        ],
    },
)
