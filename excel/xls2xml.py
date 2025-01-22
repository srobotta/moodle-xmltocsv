#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Takes a Excel file and reads all questions from one sheet and
exports these as Moodle XML.

Usage php xls2xml.py --in questions.xls

Optional arguments:
--col letter        The column letter of the question text. Default is F.
                    The answer option must follow in the next columns, e.g.
                    the first answer option text is in G and the indicator
                    if that option is correct is in H.
--in filename.xls   The filename of the Excel file to read.
--out filename.xml  If not provided the xml is written to stdout.
--row number        The number of the row to start reading. Default is 3.
                    Row 1 and 2 can be used for headlines and column labels.
--sheet number      The number of the sheet to read. Default is 1.
--type string       The type of question to export. Default is multichoise.
                    Possible values are: multichoice, kprime.
"""

from spire.xls import *
import os, sys

def dieNice(errMsg = ""):
    print("Error: {0}\nUsage: {1} --in questions.xls\nType --help for more details."
        .format(errMsg, os.path.basename(sys.argv[0])))
    sys.exit(1)

class QuestionExcel:
    wb = None
    sheet = None
    file = None
    cols = []
    row = 3

    def process(self):
        # Create a Workbook object.
        self.wb = Workbook()
        # Load an Excel file.
        self.wb.LoadFromFile(self.file)
        # Get the worksheet with the questions.
        sheet = self.wb.Worksheets[self.sheet]

        # Get a specific cell range and put that into an array.
        result = []
        cellRange = sheet.Range[self.row, self.colToNum(self.cols[0]), self.row, self.colToNum(self.cols[1])]
        isEmpty = True
        for cell in cellRange:
            val = cell.Value.strip()
            result.append(val)
            if val != '':
                isEmpty = False

        return [] if isEmpty == True else result

    def __del__(self):
        # Dispose resources.
        if self.wb != None:
            self.wb.Dispose()

    def colToNum(self, col):
        num = 0
        for i in range(len(col)):
            num = num * 26 + ord(col[i].upper()) - 64
        return num

class Question:

    def __init__(self, type, name = '', text = ''):
        self.type = type
        self.name = name
        self.text = text

    def getXml(self):
        return '''\
            <question type="{0}">
              <name>
                <text>{1}</text>
              </name>
              <questiontext format="html">
                <text><![CDATA[{2}]]></text>
              </questiontext>
              <generalfeedback format="html">
                <text></text>
              </generalfeedback>
              <defaultgrade>1</defaultgrade>
              <penalty>0.3333333</penalty>
              <hidden>0</hidden>
              <idnumber></idnumber>
              ~~__OPTIONS__~~
              ~~__ANSWERS__~~
            </question>
        '''.format(self.type, self.name, self.text)

    def escapeXml(self, text):
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&apos;')

class QuestionKprime(Question):

    def __init__(self, name, text):
        self.answers = []
        super().__init__('kprime', name, text)

    def addAnswer(self, answer, truefalse):
        self.answers.append({
            "text": answer,
            "truefalse": truefalse
        })

    def getXml(self):
        xml = super().getXml()
        xml = xml.replace('~~__ANSWERS__~~', self.getAnswersXml())
        xml = xml.replace('~~__OPTIONS__~~', self.getOptionsXml())
        return xml
    
    def getOptionsXml(self):
        return '''\
            <scoringmethod><text>kprime</text>
            </scoringmethod>
            <shuffleanswers>false</shuffleanswers>
            <numberofrows>4</numberofrows>
            <numberofcolumns>2</numberofcolumns>
        '''
    
    def getAnswersXml(self):
        xml = '''\
            ~~__ROW__~~
            ~~__COLUMN__~~
            ~~__WEIGHT__~~
        '''
        for i, answer in enumerate(self.answers):
            xml = xml.replace('~~__ROW__~~', '''\
                <row number="{1}">
                  <optiontext format="html">
                    <text><![CDATA[{0}]]></text>
                  </optiontext>
                  <feedbacktext format="html">
                    <text></text>
                  </feedbacktext>
                </row>
                ~~__ROW__~~          
            '''.format(answer['text'], str(i + 1)))

            val = True if (answer['truefalse'] == 'TRUE' or answer['truefalse'] == '1') else False
            fracTrue = '1.000' if val == True else '0.000'
            fracFalse = '1.000' if val == False else '0.000'
            xml = xml.replace('~~__WEIGHT__~~', '''\
                <weight rownumber="{0}" columnnumber="1">
                  <value>
                    {1}
                  </value>
                </weight>
                <weight rownumber="{0}" columnnumber="2">
                  <value>
                    {2}
                  </value>
                </weight>
                ~~__WEIGHT__~~
            '''.format(str(i + 1), fracTrue, fracFalse))

        xml = xml.replace('~~__COLUMN__~~', '''\
            <column number="1">
              <responsetext format="moodle_auto_format">
                <text>WAHR</text>
              </responsetext>
            </column>
            <column number="2">
              <responsetext format="moodle_auto_format">
                <text>FALSCH</text>
              </responsetext>
            </column>
        ''')

        return xml.replace('~~__ROW__~~', '').replace('~~__WEIGHT__~~', '').strip()
    
class QuestionMc(Question):
    def __init__(self, name, text):
        self.answers = []
        super().__init__('multichoice', name, text)

    def addAnswer(self, answer, fraction):
        self.answers.append({
            "text": answer,
            "fraction": fraction
        })

    def getXml(self):
        xml = super().getXml()
        xml = xml.replace('~~__ANSWERS__~~', self.getAnswersXml())
        xml = xml.replace('~~__OPTIONS__~~', self.getOptionsXml())
        return xml
    
    def getOptionsXml(self):
        return '''\
            <single>true</single>
            <shuffleanswers>false</shuffleanswers>
            <answernumbering>none</answernumbering>
            <showstandardinstruction>0</showstandardinstruction>
            <correctfeedback format="html">
            <text></text>
            </correctfeedback>
            <partiallycorrectfeedback format="html">
            <text></text>
            </partiallycorrectfeedback>
            <incorrectfeedback format="html">
            <text>></text>
            </incorrectfeedback>
            <shownumcorrect/>
        '''
    
    def getAnswersXml(self):
        xml = ''
        for answer in self.answers:
            fraction = '0' if answer['fraction'] == '' else '100'
            xml += '''\
                <answer fraction="{1}">
                  <text><![CDATA[{0}]]></text>
                  <feedback format="html">
                    <text></text>
                  </feedback>
                </answer>
            '''.format(answer['text'], fraction)
        return xml

# Depending on the type, read different cells.

def main():
    """Evaluate the cli arguments, get the file to read and write
    xml into file."""

    # available options that can be changed via the command line
    options = ['in', 'out', 'col', 'row', 'sheet', 'type', 'help']

    # the worker that does the parsing.
    worker = QuestionExcel()
    worker.sheet = 0
    worker.row = 3

    outfile = None
    qtype = 'mc'
    colStart = 'F'

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
        elif len(currentCmd) > 0:
            if currentCmd == 'in':
                worker.file = arg
            elif currentCmd == 'out':
                outfile = arg
            elif currentCmd == 'type':
                if not (arg in ['multichoice', 'kprime']):
                    dieNice('Unknown question type: ' + arg)
                qtype = arg
            elif currentCmd == 'row':
                try:
                    worker.row = int(arg)
                    if worker.row < 1:
                        raise ValueError()
                except ValueError:
                    dieNice('Invalid row number: ' + arg)
            elif currentCmd == 'col':
                if (len(arg) != 1 or ord(arg) < 65 or ord(arg) > 90):
                    dieNice('Invalid column letter: ' + arg)
                colStart = arg
            elif currentCmd == 'sheet':
                try:
                    worker.sheet = int(arg) - 1
                    if worker.sheet < 0:
                        raise ValueError()
                except ValueError:
                    dieNice('Invalid sheet number: ' + arg)
            currentCmd = ''
        else:
            dieNice('invalid argument: ' + arg)

    if worker.file == None:
        dieNice('No input file provided.')

    # process the data now
    
    #worker.cols = ['F', 'N'] if qtype == 'kprime' else ['F', 'N']
    colEnd = chr(ord(colStart) + 8)
    worker.cols = [colStart, colEnd]

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<quiz>\n'
    
    qnum = 1
    while True:
        row = worker.process()
        if len(row) == 0:
            del(worker)
            break
        worker.row += 1
        question = None
        qname = '#' + str(qnum).rjust(3, '0')
        qnum += 1
        if qtype == 'kprime':
            question = QuestionKprime(qname, row[0])
        else:
            question = QuestionMc(qname, row[0])
        for i in range(1, len(row), 2):
            question.addAnswer(row[i], row[i + 1])

        xml += question.getXml()
    xml += '</quiz>'
    if outfile == None:
        print(xml)
    else:
        with open(outfile, 'w') as f:
            f.write(xml)


if __name__ == "__main__":
    main()
