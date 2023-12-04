# moodle-xmltocsv

This project is work in progress and was created to provide a fast solution
for a teacher that wanted a CSV export of his questions.

The `mc2csv.php` script is a fast and dirty solution that works for this
specific case. From the Moodle XML file only the multiple choice questions
are extracted and written as a line into a CSV file.

If you are interested in other question types or encounter errors in the
transformation process, please open an issue.

The script itself contains a brief documentation on how to use it by
typing: `php mc2csv.php --help`

## Libreoffice export templates

The folder `libreoffice` contains Libreoffice Calc templates for multichoice
and [kprime questions](https://moodle.org/plugins/qtype_kprime) as well as
templates that can be used as an export filter for libreoffice to export a
Moodle XML ready so that the questions can be created and edited in Libreoffice
and then transfered back to Moodle. This is the contrary workflow to the
`mc2csv` scripts.

The export templates are a proof of concept. They work but may not be as foolproof
as expected and do not support all question features.