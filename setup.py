from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="hllama",
    version="0.0.3",
    description="hllama provides some useful utility functions for LLM.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="chansung park",
    author_email="deep.diver.csp@gmail.com",
    url="https://github.com/deep-diver/hllama",
    install_requires=[],
    packages=["hllama"],
    package_dir={"": "src"},
    keywords=["LLM", "Large Language Model", "Verification", "Utility"],
    python_requires=">=3.8",
    package_data={},
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
