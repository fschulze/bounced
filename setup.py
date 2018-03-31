from setuptools import setup
import os


README = open(os.path.abspath('README.rst')).read()


setup(
    name='bounced',
    version='0.2.0',
    license='MIT',
    description='A library to determine info on bounced email messages',
    long_description="\n\n".join([README]),
    url='https://github.com/fschulze/bounced',
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6"],
    install_requires=[
        'attrs'],
    package_data={
        'bounced': [
            'tests/*.py',
            'tests/bounces/*.eml',
            'tests/flufl_bounce/*.eml',
            'tests/bounce_email/bounces/*.eml',
            'tests/bounce_email/non_bounces/*.eml']},
    packages=['bounced'],
    package_dir={'': 'src'})
