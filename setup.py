from distutils.core import setup

with open("README", "r") as fh:
    long_description = fh.read()

setup(
    name = 'dattr',
    packages = ['dattr'],
    version = '1.5.0',
    license='MIT',
    description = 'Use the package to use python dictionary keys as attributes using dot(.) notation.',
    author = 'Saumalya Sarkar',
    author_email = 'saumalya75@gmail.com',
    url = 'https://github.com/mjolnir-repo/dattr',
    download_url = 'https://github.com/mjolnir-repo/dattr/archive/v1.5.0.tar.gz',
    keywords = ['python'],
    install_requires=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    long_description = long_description,
    long_description_content_type = "text/markdown"
)