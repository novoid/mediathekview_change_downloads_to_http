#!/usr/bin/env python3
# -*- coding: utf-8 -*-
PROG_VERSION = u"Time-stamp: <2018-06-16 11:13:13 vk>"


# TODO:
# * fix parts marked with «FIXXME»


# ===================================================================== ##
#  You might not want to modify anything below this line if you do not  ##
#  know, what you are doing :-)                                         ##
# ===================================================================== ##

import re
import sys
import os
import os.path
import time
import logging
from optparse import OptionParser
import tempfile
from shutil import move  # for save copy/move/overwriting files
import codecs

PROG_VERSION_DATE = PROG_VERSION[13:23]
INVOCATION_TIME = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())

# the location of the XML file of MediathekView containing the pendings downloads on GNU/Linux:
DEFAULT_XMLFILE_NAME = os.path.join(os.path.expanduser("~"), ".mediathek3", "mediathek.xml")

DOWNLOAD_SECTION_MARKER = '<!--Downloads-->'
STRING_TO_SEARCH_FOR = '<URL>https://apasfpd.apa.at'
REPLACEMENT_STRING = '<URL>http://apasfpd.apa.at'

USAGE = "\n\
    mediathekview_change_downloads_to_http.py\n\
\n\
    This little Python script tries to locate the MediathekView XML\n\
    file containing pending downloads, change their protocol from\n\
    https to http and re-writes the XML file accordingly.\n\
\n\
    Read\n\
    https://github.com/novoid/mediathekview_change_downloads_to_http\n\
    for further information.\n\
\n\
:copyright: (c) by Karl Voit\n\
:license: GPL v3 or any later version\n\
:URL: https://github.com/novoid/mediathekview_change_downloads_to_http\n\
:bugreports: via github or <tools@Karl-Voit.at>\n\
:version: " + PROG_VERSION_DATE + "\n"

parser = OptionParser(usage=USAGE)

parser.add_option("-d", "--dryrun", dest="dryrun", action="store_true",
                  help="write result to temporary file, not modifying original one")

parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
                  help="talk to me more!")

parser.add_option("-q", "--quiet", dest="quiet", action="store_true",
                  help="don't bother me with the nasty details")

parser.add_option("--version", dest="version", action="store_true",
                  help="display version and exit - how boring.")

(options, args) = parser.parse_args()


def handle_logging():
    """Log handling and configuration"""

    if options.verbose:
        FORMAT = "%(levelname)-8s %(asctime)-15s %(message)s"
        logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    elif options.quiet:
        FORMAT = "%(levelname)-8s %(message)s"
        logging.basicConfig(level=logging.ERROR, format=FORMAT)
    else:
        FORMAT = "%(levelname)-8s %(message)s"
        logging.basicConfig(level=logging.INFO, format=FORMAT)


def error_exit(errorcode, text):
    """exits with return value of errorcode and prints to stderr"""

    sys.stdout.flush()
    logging.error(text)

    sys.exit(errorcode)


def replaceFileWithOther(filetooverwrite, replacement):

    assert(os.path.isfile(filetooverwrite))
    assert(os.path.isfile(replacement))

    os.remove(filetooverwrite)
    logging.debug('removed filetooverwrite [%s]\nrenaming replacement [%s] to filetooverwrite ...\n' % (filetooverwrite, replacement))
    try:
        dst_basename = os.path.basename(filetooverwrite)
        src_dirname = os.path.dirname(replacement)
        dst_dirname = os.path.dirname(filetooverwrite)
        os.rename(replacement, os.path.join(src_dirname, dst_basename))
        move(os.path.join(src_dirname, dst_basename), dst_dirname)
    except:
        logging.error("Rename failed\n")
        raise
    logging.debug('renamed replacement to filetooverwrite\n')

    assert(os.path.isfile(filetooverwrite))  # FIXXME: there is an issue when filetooverwrite has no path
    assert(os.path.isfile(replacement) is False)


def main():
    """Main function"""

    if options.version:
        print(os.path.basename(sys.argv[0]) + " version " + PROG_VERSION_DATE)
        sys.exit(0)

    handle_logging()

    logging.debug("Guess what: this awesomeness of a program was started and logging is working now :-)\n" +
                  "What can possibly go wrong now?")  # yes, this is called sarcasm. Big time.

    if options.verbose and options.quiet:
        error_exit(1, "IQ test result: Options \"--verbose\" and \"--quiet\" found. " +
                   "This does not make any sense, you silly fool :-)")

    if options.dryrun:
        logging.debug("Now you are a officially a big sissy: DRYRUN active, not changing any files")

    logging.debug("I just wanted to let you know that I am listening to The Who \"Life at Leeds\" at full volume at this very moment. Boy this album rocks, baby!")
    logging.debug("This wass totally irelevant to to, sorry for that.")
    logging.debug("I'm going to behave now.\n\n\n\n\n")
    logging.debug("Oh, what the hell: maybe not ;-)")

    if not os.path.isfile(DEFAULT_XMLFILE_NAME):
        logging.warn('MediathekView XML file not found on the default location which is "' + DEFAULT_XMLFILE_NAME + '"')
        xmlfilename = read('Please enter the full path to mediathek.xml on your system: ')
        if not os.path.isfile(xmlfilename):
            logging.error('You chose wrong. There is no file at "' + xmlfilename + '". You get punished now. Bad boy.')
            error_exit(2, "Try again with a file name that exists and I might try again.")
    else:
        xmlfilename = DEFAULT_XMLFILE_NAME

    temp_xml_file = tempfile.mkstemp()[1]
    num_modified_lines = 0
    logging.debug('Good news: I have come up with a strange file name to use as a TEMPORARY RESULT FILENAME: ' + temp_xml_file)
    with codecs.open(temp_xml_file, 'w', encoding='utf-8') as newxml:
        within_downloads = False
        for line in codecs.open(xmlfilename, 'r', encoding='utf-8'):

            if len(line.strip()) < 1:
                logging.debug('Oh boy, I found an empty line which tells me that a section ended. To be sure, set within_downloads to False (again).')
                within_downloads = False

            if within_downloads:
                modified_line = line.replace(STRING_TO_SEARCH_FOR, REPLACEMENT_STRING)
                logging.debug('I\'m going to write line…\n•  ' + line + '\n… as a modified version which looks like …\n•  ' + modified_line)
                newxml.write(modified_line)
                num_modified_lines += 1
            else:
                # writing to output without modification - copy that!
                newxml.write(line)

            if line.strip().startswith(DOWNLOAD_SECTION_MARKER):
                logging.debug('Hey, I found the magic marker that tells me that the pending downloads are starting here ...')
                within_downloads = True

    logging.info('I have modified ' + str(num_modified_lines) + ' lines.')
    if options.dryrun:
        logging.info('See the result in TEMPORARY RESULT FILENAME: ' + temp_xml_file)
        logging.info('Compare both with, e.g., "meld ' + xmlfilename + ' ' + temp_xml_file + '" (or use diff if you\'re a real hardcore fan)')
    else:
        replaceFileWithOther(xmlfilename, temp_xml_file)

    logging.debug("This script has finished. You can now be relieved and hug a tree … but with no tongue.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:

        logging.info("Received KeyboardInterrupt")

# END OF FILE #################################################################
