#!/usr/local/bin/python2.7
# encoding: utf-8
'''
akamai_stage_ip -- determine akamai stage IP

It defines classes_and_methods

@author:     Václav Rak

@copyright:  2014 vena.cz. All rights reserved.

@license:    MIT

@contact:    me@vena.cz
@deffield    updated: 2014-07-17
'''

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import dns.resolver
__all__ = []
__version__ = 0.1
__date__ = '2014-07-17'
__updated__ = '2014-07-17'

DEBUG = 0
TESTRUN = 0
PROFILE = 0

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by user_name on %s.
  Copyright 2014 organization_name. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-c", "--csv", dest="csv", help="CSV response",  default = False, action='store_true')
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument(dest="paths", help="paths to folder(s) with source file(s) [default: %(default)s]", metavar="path", nargs='+')

        # Process arguments
        args = parser.parse_args()

        paths = args.paths
        csv = args.csv
        if csv and len(paths) > 0:
            print "domain,akamaiStageIp" 
        for inpath in paths:
            ### do something with inpath ###
            a = dns.resolver.query(inpath, 'CNAME')
            b = str(a[0]).replace(".net.", "-staging.net.")
            c = dns.resolver.query(b,  'CNAME')
            d =  dns.resolver.query(str(c[0]), 'A')
            if csv:
                print "%s,%s" % (inpath, str(d[0]))
            else:
                print "Domain '%s' akamai staging IP is %s " % (inpath, str(d[0]))
            
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'akamai_stage_ip_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())