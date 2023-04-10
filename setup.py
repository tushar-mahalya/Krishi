from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required_packages = f.read().splitlines()

setup(
    name='Krishi',
    version='1.0.0',
    description='An advanced AI powered web application for Plant Disease detection',
    author='Tushar Sharma',
    author_email='tusharmahalya@gmail.com',
    packages=find_packages(),
    install_requires=required_packages,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10'
    ],
)
