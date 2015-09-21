import urllib2
import sys
import getopt
from os.path import exists, normpath, sep
import re

DEFAULT_READ_BUF_SZ = 2048
DEFAULT_FILE_LOC    = '.'

class DownloadFile(object):
    def __init__(self, url, blocks=DEFAULT_READ_BUF_SZ, loc=DEFAULT_FILE_LOC):
        try:
            self.__url = url
            if exists(loc):
                self.__loc__ = loc
            else:
                raise IOError('output directory does not exist')
            self.read_size = blocks
        except IOError:
            raise

    def progress(self, ds, sz):
        msg = "{:0.2f} of {:,.2f} downloaded".format((ds*100.0/sz), sz)
        sys.stdout.write("\r%s" %msg)
        sys.stdout.flush()

    def perform(self):            
        try:            
            u = urllib2.urlopen(self.__url)
            ofname = normpath("{0}{1}{2}".format(self.__loc__, sep, self.__url.split(sep)[-1]))
            f = open(ofname, 'wb')
            sz = int(u.info().getheaders("Content-Length")[0])
            ds = 0
            print "saving file to: {0} ({1:,} bytes)".format(ofname, sz)
                
            while True:
                read_buffer = u.read(self.read_size)
                
                if not read_buffer:
                    break
                
                ds += len(read_buffer)
                f.write(read_buffer)
                
                self.progress(ds, sz)
                
            sys.stdout.write("\n")
                
        except (IOError, urllib2.URLError, urllib2.HTTPError):
            raise
        except KeyboardInterrupt:
            print >> sys.stderr, "\nDownload terminated"
        else:
            f.flush() 
            f.close()           
            
        return ofname

def process_args(args):
    url               = None
    download_size     = DEFAULT_READ_BUF_SZ
    download_location = DEFAULT_FILE_LOC
    
    try:
        opts, args = getopt.getopt(args, 'hu:b:o:')

        for opt, arg in opts:
            if opt == '-h':
                usage()
                sys.exit(2)
            elif opt == '-u':
                url = arg
            elif opt == '-b':
                if re.match("^[+-]?[0-9]*$", arg):
                    download_size = int(arg)
                else:
                    raise TypeError('download size must be an integer')
                if download_size < 1:
                    raise TypeError('download size must be > 0')
            elif opt == '-o':
                download_location = arg
    except TypeError:
        raise
    except getopt.GetoptError:
        raise('invalid argument')
    
    return (url, download_size, download_location)

def usage():
    print >> sys.stderr, """
{0} - large file download & monitor
usage: {0} -u url -b read_block_size -o download_location [-h]
""".format(sys.argv[0])

if __name__ == "__main__":
    try:
        (url, size, location) = process_args(sys.argv[1:])
        if url is None or location is None:
            raise TypeError('missing arguments')
        
        f = DownloadFile(url, size, location)
        fname = f.perform()
    except (TypeError, IOError, getopt.GetoptError, urllib2.URLError, urllib2.HTTPError), e:
        print >> sys.stderr, e
        usage()
        sys.exit(1)
    else:
        print "{0} download complete".format(fname)
        sys.exit(0)
