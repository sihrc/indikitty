from setuptools import setup, find_packages
import os

if __name__ == "__main__":
    setup(
        name = "indikitty",
        packages = find_packages(),
        install_requires = open(os.path.join(
            os.path.dirname(__file__),
            "req.txt"), 'rb')
        .readlines(),
        version = "0.1.0"
    )
