from setuptools import setup, find_packages
from setuptools.command.install import install
from opencv_fixer import AutoFix

class AutoFixCommand(install):
    def run(self):
        AutoFix()
        install.run(self)

setup(
    name='opencv_fixer',
    version='0.2.4',
    license='Apache 2.0',
    author="soulteary",
    author_email="soulteary@gmail.com",
    packages=find_packages(),
    description='Fix OpenCV Issue for numpy, diffusers, etc.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/soulteary/opencv-fixer',
    install_requires=[],
    cmdclass={
        'install': AutoFixCommand,
    },
)
