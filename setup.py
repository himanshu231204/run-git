from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="run-git",
    version="1.0.9",
    author="Himanshu Kumar",
    author_email="",
    description="Git automation CLI — one command to add, commit, pull & push with smart commit messages, TUI, and GitHub repo creation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/himanshu231204/gitpush",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control :: Git",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "rich>=13.0.0",
        "GitPython>=3.1.0",
        "PyGithub>=1.59.0",
        "questionary>=1.10.0",
        "pyyaml>=6.0",
        "requests>=2.28.0",
    ],
    extras_require={
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "run-git=gitpush.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "gitpush": ["config/templates/*"],
    },
)