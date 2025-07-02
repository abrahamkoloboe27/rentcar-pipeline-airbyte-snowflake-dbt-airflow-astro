from setuptools import find_packages, setup

setup(
    name="rentcar",
    version="0.0.1",
    packages=find_packages(),
    package_data={
        "rentcar": [
            "dbt-project/**/*",
        ],
    },
    install_requires=[
        "dagster",
        "dagster-cloud",
        "dagster-dbt",
        "dbt-snowflake<1.10",
    ],
    extras_require={
        "dev": [
            "dagster-webserver",
        ]
    },
)