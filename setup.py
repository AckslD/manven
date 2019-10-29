import setuptools

with open("README.md", 'r') as f:
    long_description = f.read()

with open("requirements.txt", 'r') as f:
    install_requires = [line.strip() for line in f.readlines()]

setuptools.setup(
    name="manven",
    version="0.1.1",
    author="Axel Dahlberg",
    author_email="axel.dahlberg12@gmail.com",
    description="Small CLI for managing virtual python environments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AckslD/manven",
    include_package_data=True,
    scripts=["bin/manven", "bin/manven.fish"],
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: MacOS"
    ],
)
