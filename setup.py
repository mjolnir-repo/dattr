from distutils.core import setup
setup(
  name = 'dattr',
  packages = ['dattr'],
  version = '1.0',
  license='MIT',
  description = 'This package was developed as support package to mjonir project. In mjolnir project, there are certain scope to read configuration json and traverse through then recursively. So I felt the need for a solution that will let us chain the dictionary keys with dot notation for ease-of-use. Hence I built one. I know there are already some libraries available which do similar stuff. But the purpose of this package was to support custom features like reading-writing to-fro json files, read strings and compile as dictionary directly etc.',   # Give a short description about your library
  author = 'Saumalya Sarkar',
  author_email = 'saumalya75@gmail.com',
  url = 'https://github.com/mjolnir-repo/dattr',
  download_url = 'https://github.com/mjolnir-repo/dattr/archive/v1.0.tar.gz',
  keywords = ['python'],
  install_requires=[],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development',
    'License :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)