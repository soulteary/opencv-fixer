from setuptools import setup, find_packages

setup(
    name='opencv-fixer',
    version='0.1',
    license='Apache 2.0',
    author="soulteary",
    author_email="soulteary@gmail.com",
    packages=find_packages(),
    description='Fix OpenCV Issue for numpy, diffusers, etc.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/soulteary/opencv-fixer',
    install_requires=[],
)