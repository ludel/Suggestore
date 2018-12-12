import setuptools

setuptools.setup(
    name='suggestore',
    version='0.0.1',
    author='Ludovic Delsol',
    install_requires=['pandas', 'sklearn', 'requests'],
    python_requires='>=3.7',
    include_package_data=True,
    packages=setuptools.find_packages(),
)