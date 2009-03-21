#!python
import sys
import os
import shutil
import datetime
from zipfile import ZipFile, is_zipfile
#Settings

installdir = os.path.join(os.environ['HOME'], 'Models', 'dMilo')
archivedir = os.path.join(os.environ['HOME'], 'Models', 'Archive')

def install(zfile, outdir):
	print zfile
	print outdir
	if not os.path.exists(outdir):
		print "Install dir does not exist"
		return False
	if is_zipfile(zfile):
		zip = ZipFile(zfile, 'r')
		runtimeindex = -1
		for each in zip.namelist():
			index = each.lower().rfind('runtime')
			if index > runtimeindex: runtimeindex = index
		if runtimeindex == -1:
			print "Unable to determine install"
			return False
		for each in zip.namelist():
			try:
				newdir, filename= [unicode(x , 'iso-8859-1') for x in  os.path.split(each)]
			except UnicodeDecodeError, e:
				print e
			if -1 != newdir.lower().rfind('runtime'):
				newdir = newdir[newdir.lower().rfind('runtime'):]	
			if not os.path.exists(os.path.join(outdir,newdir)):
				os.makedirs(os.path.join(outdir,newdir))
			if 0 == zip.getinfo(each).file_size: #Probably a dir
				if not os.path.exists(os.path.join(outdir, newdir, filename)):
					os.makedirs(os.path.join(outdir, newdir, filename))
			else:
				try:
					outfile = open(os.path.join(outdir,newdir,filename), 'wb')
					outfile.write(zip.read(each))
					outfile.close()
				except:
					print "zip error"
					zip.close()
					return False
		zip.close()
	else:
		print "Not a zipfile"
		return False
	return True	

def main():
	args = sys.argv[1:]
	if len(args) > 1:
		dir = args[1]	
	else:
		dir = installdir
	if os.path.isdir(args[0]):
		filelist = os.listdir(args[0])
		filelist.sort()
		for filename in filelist:
			if install(filename, dir):
				print "Installed %s\n"%filename
				targetDir = os.path.join(archivedir, str(datetime.date.today()))
				if not os.path.exists( targetDir ):
					os.makedirs( targetDir )
				try:
					shutil.move(filename, targetDir)
				except:
					print "Unable to move %s"%(filename)
		

		
			
	else:

		install(args[0], dir)

if __name__=="__main__":
	main()
