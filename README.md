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
