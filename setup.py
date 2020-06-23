from setuptools import setup

setup(
    name="jottingspool",
    author="Ewan Nicolson",
    description=("Tools to take and organise notes"),
    url="https://github.com/dataewan/jottingspool",
    packages=["jottingspool"],
    entry_points={
        "console_scripts": ["jottings-pool=jottingspool.interface:command_line"]
    },
    install_requires=["mistletoe", "rich"],
)
