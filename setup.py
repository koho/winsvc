from setuptools import setup, find_packages

setup(
    use_scm_version=False,
    version="1.0",
    packages=find_packages(),
    install_requires=['click', 'pywin32; sys_platform == "win32"']
)
