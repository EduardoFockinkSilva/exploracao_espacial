from setuptools import setup, find_packages

setup(
    name='simulacao_sistema_solar',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pygame',
        'PyOpenGL',
    ],
    author='Eduardo Fockink Silva',
    author_email='eduardo.epublic@gmail.com',
    description='Simulação do Sistema Solar com foguetes e controle de câmera',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/EduardoFockinkSilva/simulacao_sistema_solar',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'simulacao=simulacao.main:main',
        ],
    },
    python_requires='>=3.6',
)
