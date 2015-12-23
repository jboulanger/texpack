#!/usr/bin/env python
# Scan a tex file to find figures and bib
# tested on Ubuntu only
# Jerome Boulanger
import os, sys
import re

class TexPack(object):
    """
    Package a tex folder
    """

    def __init__(self, filename):
        """
        """
        filename = os.path.abspath(filename)
        self.filename = os.path.abspath(filename)
        self.src_folder = os.path.dirname(filename)
        self.logfile = os.path.splitext(os.path.basename(filename))[0] + '.log'
        self.blgfile = os.path.splitext(os.path.basename(filename))[0] + '.blg'
        self.texfile = os.path.splitext(os.path.basename(filename))[0] + '.tex'
        self.project = os.path.splitext(os.path.basename(self.src_folder))[0]
        self.directory = os.path.join(self.src_folder, self.project)
        if not os.path.exists(self.directory):
            os.mkdir(self.directory)
        self.store(self.texfile)
        self.parse(self.logfile, '<.*use (.*)>')
        self.parse(self.logfile, 'PGFPlots: reading {(.*)}')
        self.parse(self.blgfile,"INFO - Found BibTeX data source '(.*)'");

    def store(self, item):
        f = os.path.join(self.src_folder, item)
        if os.path.exists(f):
            g = os.path.join(self.directory, item)
            if not os.path.exists(os.path.dirname(g)):
                os.mkdir(os.path.dirname(g))
            os.system('cp '+ f + ' ' + g)
        else:
            print f + ' not found'

    def parse(self, filename, expression):
        p = re.compile(expression)
        with open(os.path.join(self.src_folder,filename)) as f:
            for line in f:
                m = p.search(line)
                if m != None:
                    self.store(m.group(1))

if __name__ == "__main__":
    tp = TexPack(sys.argv[1])
