from setuptools import setup, find_packages

setup(
    name="taurus",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "psycopg2",
        "numpy",
        "pandas",
        "pandas_ta",
        "datetime",
        "time",
        "warnings",
        "MetaTrader5",
        "scipy",
        "tqdm",
        "itertools",
        "TA-Lib",
        "joblib"
    ],
    extras_require={
        "yfinance": ["yfinance>=0.0.0"],
    },
)