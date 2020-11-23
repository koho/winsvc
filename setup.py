from setuptools import setup, find_packages

setup(
    use_scm_version=True,
    packages=find_packages(),
    install_requires=['click', 'pywin32; sys_platform == "win32"']
)
