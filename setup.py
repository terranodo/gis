from distutils.core import setup

setup(
    name='asyncgeo',
    version='0.1',
    url='http://github.com/terranodo/asyncgeo',
    license='MIT',
    author='Ariel Nunez',
    author_email='ingenieroariel@gmail.com',
    description='async + http2 + postgis + openapi + geo+json-seq',
    long_description=open('README.md').read(),
    py_modules=['asyncgeo'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System ::: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
