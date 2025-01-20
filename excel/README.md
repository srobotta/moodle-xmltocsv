## Export from Excel

This is still work in progress. The idea is to have an Excel template and export
questions as Moodle XML from Excel. Basically the same as in the
[`libreoffice`](../libreoffice/) folder.

I am trying to follow this guide: https://blog.udemy.com/excel-to-xml/

The problem is that Excel does it way more complicate than LibreOffice.

### One XSD for the Moodle XML

My first approach was to write an XSD file. Unfortunately, the `<question>`
element is ambiguous, so I was not able to have an XSD that would match both
question types (in this project I am focusing on mc and kprime only) in
one file. Any hints on how to write one XSD that would match all questions
are welcome.

It is also not so important to have all question types in one XSD because
in an table calculation you would have one type of questions per sheet only.
Therfore, the two XSD are separated by question type.

The validation of an XML agains a stylesheet can be done like this:

```
xmllint --schema kprime.xsd question-kprime.xml --noout
```

### The XSD for the Excel export

The two XSD files cannot be used for the Excel export. Excel needs a 1:1
mapping of the elements from the stylesheet. Having e.g. in a Multichoice
question a list of responses that I set to at least 2 but with an unbound
list, doesn't allow you in Excel to drag and drop XML elements onto a
column or cell.

These two XSD need to be rewritten with an exact defined number of elements.
So the MC question might work with exactly 4 answers.

The Kprime questions lack the fact, that an X to indicate which of the true
false field of an answer option is correct, seems to be complicated as well.
I didn't get so far to check whether this is possible or not.

### Next steps

The next steps would be: write a python script and bundle it in a way that
it is fool proofe usable by an inexperienced user.

Also there might be the option to have some Visual Basic programming to
have an in-Excel solution.


