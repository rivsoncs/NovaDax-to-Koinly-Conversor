from setuptools import setup, find_packages

setup(
    name="novadax-koinly",
    version="2.0.0",
    description="Conversor de extratos da NovaDax para o formato Koinly",
    author="Rivson CS",
    author_email="email@example.com",  # Substitua pelo seu email
    url="https://github.com/rivsoncs/NovaDax-to-Koinly-Conversor",
    packages=find_packages(),
    install_requires=[
        "pdfplumber",
    ],
    entry_points={
        "console_scripts": [
            "novadax-koinly=novadax_koinly.cli:main",
            "nova2k=novadax_koinly.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 