"""
Poser types is a representation of the poser files in python.   

    @Author: Peter Tiegs
    Nascentia Corporation 2007 (Some Rights Reserved).
"""
    
import os
import re
import time
import hashlib
import ZestyParser as ZP 

## Dictionary map between extention and text for type
POSERTYPES = {u".cr2": u"Poser Character",
          u".pp2":u"Poser Prop",
          u".pz2":u"Poser Pose",
          u".hr2":u"Poser Hair",
          u".hd2":u"Poser Hands",
          u".lt2":u"Poser LightSet"}
class TagParser(object):
    def __init__(self, ignoreWords = [], dropSingletons=False):
        dTagset = ZP.Defer(lambda: self.Tagset)
        tag = ZP.RE(r'[a-zA-Z\d]+', group=0, callback=self.cbTag)
        self.Tagset= (tag | ZP.Omit(ZP.RE(r'[\s!_-]+')))+dTagset
        self.tags=set()
        self.ignoreWords = ignoreWords
        self.dropSingletons = dropSingletons

    def cbTag(self, data):
        if self.dropSingletons and (len(data) < 2):
            pass
        elif data.lower() in [x.lower() for x in self.ignoreWords]:
            pass
        else:
            self.tags.add(data)

    def getTags(self, inputString):
        parser=ZP.ZestyParser(inputString)
        parser.scan(self.Tagset)
        return self.tags

class RuntimePathParser(object):
    """Parses the path for poser files for data about the model."""
    def __init__(self):
        """Contstructor sets up the parse tokens."""
        self.runtimefound = False
        tDir = ZP.Defer(lambda: self.Dir)
        pathsep = ZP.RE(r'[\\|\/]')
        dirname = ZP.RE(r'[\w\s!-]+', group=0,callback=self.cbDirname)
        rtdirname = ZP.RE(r'[\w\s!-]+', group=0)
        filename =ZP.RE(r'[\w\s!-]+\.[\w]+',group=0)
        #rtDir = ZP.TokenSequence( (rtdirname,ZP.Omit(pathsep), ZP.Omit(ZP.RE(r'[Rr]untime')+pathsep+ZP.RE(r'[Ll]ibraries')+pathsep+dirname)), callback=self.cbRuntimeFound)
        rtDir = ZP.TokenSequence( (rtdirname,ZP.Omit(pathsep), ZP.Omit(ZP.RE(r'[Rr]untime')+pathsep+ZP.RE(r'[Ll]ibraries'))), callback=self.cbRuntimeFound)
        self.Dir = ZP.Omit(pathsep)+(rtDir|dirname) + (tDir|ZP.Omit(pathsep)+filename)

    def cbRuntimeFound(self,data):
        """Callback when the runtime is found.
            @data: the matching string
        """
        if not self.runtimefound:
            self.pathmeta['runtime'] = data[0]
            self.runtimefound = True

    def cbDirname(self,data):
        """Callback when a directory is found.
            @data: the matching string (directory name)
        """
        if self.runtimefound:
            self.pathmeta['libs'].append(data)

    def getTags(self, liblist):
        """Given a list of strings parses out tags from only alpha-numeric characters
        to use as meta data tags for the Poser object.
            @liblist: a list of strings (directory names)
        """
        thisTagParser = TagParser(ignoreWords=['the'], dropSingletons=True)
        retval = set()
        for lib in liblist:
            retval = retval.union(thisTagParser.getTags(lib.lower()))
        return sorted(retval)

    def parsePath(self,pathstring):
        """Parses a directory string with the tokens setup in the constructor.
            @pathstring: full path of a directory containing a poser file type."""
        
        self.pathmeta = {'runtime':'','libs':[]}
        parser = ZP.ZestyParser(pathstring)
    #   parser = ZP.DebuggingParser(pathstring)
        out = parser.scan(self.Dir)
        liblist = self.pathmeta['libs']
        if len(liblist) >=1:
            self.pathmeta['tags']=self.getTags(self.pathmeta['libs'])
        return self.pathmeta

class posertype(object):
    """ This is the base class for all the poser types """
    
    def read(self, filename):
        """Open and read the Poser file.
            @filename: full path to poser file."""
        self.filename= filename
        base, ext = os.path.splitext(self.filename)
        self.thumb = base+(".png")
        self.type = POSERTYPES[ext]
        input = open(self.filename, "r")
        self.raw = input.read()
        self.chksum = hashlib.md5( self.raw ).hexdigest()
        input.close()
    
    def getPathMeta(self):
        """Parse the directory containing the poser file for additional meta data."""
        (drive, pathstring)=  os.path.splitdrive(os.path.dirname(self.filename))

        return RuntimePathParser().parsePath(pathstring)

    def parse(self):
        """Parse the Actual structure of the Poser file."""
        pass
        
def parsePath( pathstring ):
        return RuntimePathParser().parsePath(pathstring)

