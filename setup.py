from setuptools import setup, find_packages

setup(
    name="xprpy",  # The name of your package
    version="1.0.1",  # The initial version of your package
    author="paulgnz",
    author_email="protonnz4@gmail.com",
    description="A Python library for XPR Network blockchain transactions.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/paulgnz/xprpy",  # Replace with your repository URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        # List your dependencies here
        "requests",  # Example dependency
        "python-dotenv",
        # Add others as needed
    ],
)
