from setuptools import setup, find_packages


setup(
    name='finite-topology',
    version='0.1.11',
    author='nand0san',
    author_email='hancaidolosdos@hotmail.com',
    description='A Python library for defining and manipulating topologies on finite sets.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/nand0san/Topology',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
    python_requires='>=3.7',
    install_requires=[
        # Add any dependencies here, if needed
    ],
    include_package_data=True,
    keywords='topology, mathematics, finite sets, discrete topology',
    project_urls={
        'Source': 'https://github.com/nand0san/Topology',
        'Tracker': 'https://github.com/nand0san/Topology/issues',
    },
)
