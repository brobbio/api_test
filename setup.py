from setuptools import setup, find_packages

setup(
    name="items-api",
    version="0.1.0",
    description="Webapp to store items",
    package_dir={"": "src"},
    author="",
    packages=find_packages(where=".", exclude=["tests", "test*"]),
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "sqlalchemy",
        "psycopg[binary]",
        "fastapi>=0.124.4",
        "uvicorn>=0.33.0",
        "pytest",
        "httpx",
    ],
    entry_points={
        "console_scripts": [
            "items-api=app:main",
        ],
    },
)