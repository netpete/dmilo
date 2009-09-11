import sys, os
from setuptools import setup , find_packages

packages = find_packages()
setup(name = 'dMilo',
	version='0.3',
	description='3D Asset Management Application',
	author='Peter Tiegs',
	author_email='peter@nascentia.com',
	url='www.nascentia.com',
	test_suite = 'dmilo.dmilo_test.test_suite',
	packages = packages,
	app=['bin/macstart.py'],

	entry_points = {
		'console_scripts': [
			'zipinstall = dmilo.zipinstall:main',
			'dmilo = dmilo.dmilo:main' 
			]
		},
	package_data = {
		'dmilo':['templates/*','*.xrc','resource/*'],
		},
	zip_safe=False,
	install_requires = [
		#'wxPython',
		#'twisted',
		'mako',
		'sqlobject',
		'ZestyParser',
	],
	setup_requires=['py2app'],

	)
