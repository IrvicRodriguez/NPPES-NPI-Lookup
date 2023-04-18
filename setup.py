from setuptools import setup, find_packages

setup(
    name="npi-lookup",
    version="0.1",
    py_modules=["npi_lookup"],
    install_requires=[
        'requests',
        'sqlalchemy',
        'alembic'
    ],
    entry_points={
        'console_scripts': [
            'npi-lookup = npi_lookup:main',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
