"""The setup file for the library."""

from setuptools import setup
from setuptools import find_namespace_packages

# load the README file.
with open(file="README.md", mode="r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(

    # this will be my Library name.
    name='finance-brain',

    # Want to make sure people know who made it.
    author='Alex Reed',

    # also an email they can use to reach out.
    author_email='alexreed1192@gmail.com',

    # I'm in alpha development still, so a compliant version number is a1.
    # read this as MAJOR VERSION 0, MINOR VERSION 1, MAINTENANCE VERSION 0
    version='0.1.0',

    # here is a simple description of the library, this will appear when
    # someone searches for the library on https://pypi.org/search
    description='A document parser that uses ChatGPT to parse different financial documents.',

    # I have a long description but that will just be my README file, note the
    # variable up above where I read the file.
    long_description=long_description,

    # want to make sure that I specify the long description as MARKDOWN.
    long_description_content_type="text/markdown",

    # here is the URL you can find the code, this is just the GitHub URL.
    url='',

    # there are some dependencies to use the library, so let's list them out.
    install_requires=[
        'requests',
        'openai',
        'python-docx',
        'PyPDF2',
        'docx2pdf',
        'markdown'
    ],

    # some keywords for my library.
    keywords='api, chatgpt, parser',

    # here are the packages I want "build", in this case the finbrain package.
    packages=find_namespace_packages(
        include=['finbrain', 'finbrain.*']
    ),

    # I also have some package data, like photos and JSON files, so I want to
    # include those too.
    include_package_data=True,

    # you will need python 3.11 to use this libary.
    python_requires='>=3.11'

)
