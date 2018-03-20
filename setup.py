from distutils.core import setup

setup(
    name='gis',
    version='0.2',
    url='http://github.com/terranodo/gis',
    license='MIT',
    author='Ariel Nunez',
    author_email='ingenieroariel@gmail.com',
    description='async + http2 + postgis + openapi + geo+json-seq',
    long_description=open('README').read(),
    py_modules=['gis'],
    install_requires=[
        'h2',
        'asyncio',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
