import sys, os
from setuptools import setup , find_packages

packages = find_packages()
setup(name = 'dMilo',
	version='0.2',
	description='3D Asset Management Application',
	packages = packages,
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
	author='Peter Tiegs',
	author_email='peter@nascentia.com',
	url='www.nascentia.com',
	)
