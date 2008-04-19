import os, sys
from PythonMagick import Image 

def rsr2pct(rsrfile):
	header = open(os.path.join('resource',"pict.header"), 'rb')
	file = open(os.path.normpath(rsrfile), 'rb')
	pictfile = os.path.splitext(rsrfile)[0] + ".pct"
	rsrhead= file.readline()
	data = file.read()
	outfile = open(pictfile, 'wb')

	outfile.write(header.read()+data)
	outfile.close()

def rsr2png(rsrfile):
	rsr2pct(rsrfile)
	pictfile = os.path.splitext(rsrfile)[0]+".pct"
	try:
		thumb = Image(str(pictfile))
	except:
		print pictfile
		raise
	thumb.opacity(100)
	thumb.scale(91,91)
	thumb.write(str(os.path.splitext(rsrfile)[0]+".png"))
if __name__ == '__main__':
	#rsr2pct(sys.argv[1])
	rsr2png(sys.argv[1])
