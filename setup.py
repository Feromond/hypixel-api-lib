from setuptools import setup, find_packages

setup(
    name='hypixel_api_lib',  
    version='0.1.0',
    author='Desmond O, Jacob M',
    author_email='JacobPMish@gmail.com, desmond.obrien@ucalgary.ca',
    description='A python library to interact with the hypixel api, specifically focused on skyblock',
    # long_description=open('README.md').read(),
    # long_description_content_type='text/markdown',
    url='https://github.com/feromond/hypixel-api-lib',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'numpy==2.1.2',  
        'pandas==2.2.3',
        'requests==2.32.3',
    ],
)
