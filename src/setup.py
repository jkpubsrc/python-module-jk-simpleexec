from setuptools import setup


def readme():
	with open('README.rst') as f:
		return f.read()


setup(name='jk_simpleexec',
	version='0.2017.8.28',
	description='Module to run shell programs in a very simple way.',
	author='Jürgen Knauth',
	author_email='pubsrc@binary-overflow.de',
	license='Apache 2.0',
	url='https://github.com/jkpubsrc/python-module-jk-simpleexec',
	download_url='https://github.com/jkpubsrc/python-module-jk-simpleexec/tarball/0.2017.8.28',
	keywords=['exec', 'command'],
	packages=['jk_simpleexec'],
	install_requires=[
	],
	include_package_data=True,
	classifiers=[
		'Development Status :: 4 - Beta',
		'Programming Language :: Python :: 3.5',
		'License :: OSI Approved :: Apache Software License'
	],
	long_description=readme(),
	zip_safe=False)

