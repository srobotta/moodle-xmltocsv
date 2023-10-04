#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Takes a Moodle XML export file of questions and exports all the
multiple choice questions into a csv file.

Usage php mc2csv.php --in questions.xml

Optional arguments:
--delimiter char    Delimiter character for the csv file, default is ";"
--keephtml          Do not strip html tags at all.
--keeptags 'a,b,c'  List of tags that should not be eliminated when
                    stripping html from the questions. The default
                    tags that are not purged: i,img,s,strong,sub,sub,u
--out filename.csv  if not provided the base name of the xml file is
                    used, trailed by a .csv suffix.
"""

import xml.etree.ElementTree as ET
from html.parser import HTMLParser
import os, sys, csv

def dieNice(errMsg = ""):
    print("Error: {0}\nUsage: {1} --in moodle_questions.xml\nType --help for more details."
        .format(errMsg, os.path.basename(sys.argv[0])))
    sys.exit(1)

class HTMLTagRemover(HTMLParser):
    def __init__(self, keeptags):
        super().__init__()
        self.result = []
        self.keeptags = keeptags

    def handle_data(self, data):
        self.result.append(data)

    def handle_starttag(self, tag, attrs):
        try:
            self.keeptags.index(tag)
            self.result.append('<' + tag + ', '.join(['{}="{}"'.format(k,v) for k,v in attrs.iteritems()]) + '>')
        except:
            pass

    def handle_endtag(self, tag):
        try:
            self.keeptags.index(tag)
            self.result.append('</' + tag + '>')
        except:
            pass

    def handle_startendtag(tag, attrs):
        try:
            self.keeptags.index(tag) > -1
            self.result.append('<' + tag + ', '.join(['{}="{}"'.format(k,v) for k,v in attrs.iteritems()]) + '/>')
        except:
            pass

    def get_text(self):
        return ''.join(self.result)


class McHandler:

    def __init__(self, cols, options):
        self.cols = cols
        self.keeptags = options['keeptags']
        self.keephtml = options['keephtml']

    def insertColInRow(self, row, name, value):
        try:
            i = self.cols.index(name)
            row[i] = value
        except ValueError:
            self.cols.append(name)
            row.append(value)

    def formatHtml(self, value):
        if value == None:
            return ''
        if self.keephtml == True:
            return value
        remover = HTMLTagRemover(self.keeptags)
        remover.feed(value)
        return remover.get_text()

    def handle(self, question):
        if 'type' not in question.attrib or question.attrib['type'] != 'multichoice':
            return []
        row = ['' for i in range(0, len(self.cols))]
        self.insertColInRow(row, 'name', question.find('name/text').text)
        self.insertColInRow(row, 'questiontext', self.formatHtml(question.find('questiontext/text').text))
        self.insertColInRow(row, 'generalfeedback', self.formatHtml(question.find('generalfeedback/text').text))
        self.insertColInRow(row, 'defaultgrade', question.find('defaultgrade').text)
        self.insertColInRow(row, 'penalty', question.find('penalty').text)
        self.insertColInRow(row, 'hidden', question.find('hidden').text)
        self.insertColInRow(row, 'idnumber', question.find('idnumber').text)
        self.insertColInRow(row, 'single', '1' if question.find('single').text.strip() == 'true' else '0')
        self.insertColInRow(row, 'shuffleanswers', '1' if question.find('shuffleanswers').text.strip() == 'true' else '0')
        self.insertColInRow(row, 'answernumbering', question.find('answernumbering').text)
        self.insertColInRow(row, 'showstandardinstruction', question.find('showstandardinstruction').text)
        self.insertColInRow(row, 'correctfeedback', self.formatHtml(question.find('correctfeedback/text').text))
        self.insertColInRow(row, 'partiallycorrectfeedback', self.formatHtml(question.find('partiallycorrectfeedback/text').text))
        self.insertColInRow(row, 'incorrectfeedback', self.formatHtml(question.find('incorrectfeedback/text').text))
        i = 1
        for answer in question.findall('answer'):
            self.insertColInRow(row, 'answer_' + str(i), self.formatHtml(answer.find('text').text))
            self.insertColInRow(row, 'answer_' + str(i) + '_fraction', answer.attrib['fraction'])
            self.insertColInRow(row, 'answer_' + str(i) + '_feedback', self.formatHtml(answer.find('feedback/text').text))
            i = i + 1

        return row

class QuestionXml:

    def __init__(self):
        self.infile = None
        self.outfile = None
        self.delimiter = ';'
        self.keeptags = ['i', 'img', 's', 'strong', 'sub', 'sub', 'u']
        self.keephtml = False
        self.cols = []
        self.rows = []


    def process(self):
        # Passing the path of the
        # xml document to enable the
        # parsing process
        if self.infile == None:
            dieNice('No Moodle XML file provided')

        try:
            tree = ET.parse(self.infile)
        except FileNotFoundError:
            dieNice('File {0} not found'.format(self.infile))
        except ET.ParseError:
            dieNice('Error parsing XML in file ' + self.infile)

        # getting the parent tag of
        # the xml document
        root = tree.getroot()

        handler = McHandler(self.cols, {'keephtml': self.keephtml, 'keeptags': self.keeptags})
        for question in root.findall('question'):
            row = handler.handle(question)
            if len(row) > 0:
                self.rows.append(row)


    def writeCsv(self):
        # Check, if we have a file name set.
        if self.outfile == None:
            p = self.infile.rfind('.')
            if p == -1:
                p = len(self.infile)
            self.outfile = self.infile[0, p] + '.csv'
        # Open the file.
        try:
            fp = open(self.outfile, "w")
        except:
            dieNice('Could not open file %s for writing result' % self.outfile)
        # Setup the writer and put the columns (as header) and then all rows into the file.
        writer = csv.writer(fp, delimiter = self.delimiter)
        writer.writerow(self.cols)
        for row in self.rows:
            writer.writerow(row)
        fp.close()


def main():
    """Evaluate the cli arguments, built up the work object
    with the parameters to process the xml file. Finally write
    the output into a csv file."""

    # available options that can be changed via the command line
    options = ['in', 'out', 'delimiter', 'keephtml', 'keeptags', 'help']

    # the worker that does the parsing.
    worker = QuestionXml()

    # try to fetch the command line args
    currentCmd = ''
    for i in range(len(sys.argv)):
        if i == 0:
            continue
        arg = sys.argv[i]
        if arg[0:2] == '--':
            currentCmd = arg[2:]
            if not(currentCmd in options):
                dieNice(f"Invalid argument {0}".format(currentCmd))
            if currentCmd == 'help':
                print(__doc__)
                sys.exit(0)
            elif currentCmd == 'keephtml':
                worker.keephtml = True
                currentCmd = ''
        elif len(currentCmd) > 0:
            if currentCmd == 'in':
                worker.infile = arg
            elif currentCmd == 'out':
                worker.outfile = arg
            elif currentCmd == 'delimiter':
                if len(arg) > 1:
                    dieNice('Delimiter must be one character only')
                worker.delimiter = arg
            elif currentCmd == 'keeptags':
                worker.keeptags = list(map(lambda x: x.strip(), arg.split(',')))
            currentCmd = ''
        else:
            dieNice('invalid argument: ' + arg)

    # process the data now
    worker.process()
    worker.writeCsv()

if __name__ == "__main__":
    main()
