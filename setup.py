from setuptools import setup, find_packages

setup(
    name="HadithIQ",
    version="1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "mysql-connector-python",
        "sentence-transformers",
        "numpy",
        "fastapi",
        "uvicorn",
    ],
)
