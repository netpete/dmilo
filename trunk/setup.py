import sys, os
from setuptools import setup , find_packages

mainscript = 'dmilo.py'
if os.name == 'nt':
	homedir = os.environ['HOMEPATH']
else:
	homedir = os.environ['HOME']

packages = find_packages()
setup(name = 'dMilo',
	version='0.2',
	description='3D Asset Management Application',
	packages = packages,
	#include_package_data = True,
	entry_points = {'console_scripts': ['zipinstall = dmilo.zipinstall:main', 'dmilo = dmilo.dmilo:main' ]},
	package_data = {
		'dmilo':['templates/*','*.xrc','resource/*'],
		},
	zip_safe=False,
	
	author='Peter Tiegs',
	author_email='peter@nascentia.com',
	url='www.nascentia.com',
	)
