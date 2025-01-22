## Export from Excel

This is still work in progress. The idea is to have an Excel template and export
questions as Moodle XML from Excel. Basically the same as in the
[`libreoffice`](../libreoffice/) folder.

First approach: follow this guide: https://blog.udemy.com/excel-to-xml/

The problem is that custom exports in Excel are way more complicated than LibreOffice.

### One XSD for the Moodle XML

My first approach was to write an XSD file. Unfortunately, the `<question>`
element is ambiguous. I did not find a way to write one XSD that would match both
question types (in this project I am focusing on multichoice and kprime questions
only) in one file. Any hints on how to write a single XSD that would match all question
types are welcome.

On the other hand it is not so important to have all question types in one XSD because
in a table calculation you would have one type of questions per sheet only.
Therefore, having one XSD per question type is fine.

The validation of a XML against a stylesheet can be done like this:

```
xmllint --schema kprime.xsd question-kprime.xml --noout
```

### The XSD for the Excel export

The two XSD files cannot be used for the Excel export. Excel needs a 1:1
mapping of the elements from the stylesheet. When configuring the fields
for the XML export, the elements of the XSD file are dragged and dropped
onto the cells of the Excel sheet. Having e.g. in a Multichoice
question a list of responses, makes this impossible. In my XSD I defined
that a multichoice question must have at least 2 answer options with no
upper bound. When defining the mapping, it seems impossible to define
which answer option maps to which column or cell.

These two XSD need to be rewritten with an exact defined number of elements.
So the MC question might work with exactly 4 answers.

The Kprime questions lack the fact, that an X (or otherwise filled cell)
indicates whether an option is true or false to be correct. I haven't
figured out that I can set this.

Therefore, even though for multichoice question this might work, I currently
stop here and will not got any further.

### Next steps

The next steps would be: write a python script and bundle it in a way that
it is fool proof to use by an inexperienced user.

Also there might be the option to have some Visual Basic programming in order
to have an in-Excel solution without any other software dependency.

### Python script

The `xls2xml.py` can read an Excel file and outputs it to a xml file. The
`questions.xls` is an example where questions can be added in rows. The
Python script relies on the column order provided in that Excel file.

Before the script can be used, the depencencies must be installed. This is
mainly [Spire.Xls](https://pypi.org/project/Spire.Xls/) which is done via:

```
pip install spire.xls
```


