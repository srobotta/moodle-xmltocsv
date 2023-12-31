<?php
// This software is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// You should have received a copy of the GNU General Public License
// along with Moodle.  If not, see <http://www.gnu.org/licenses/>.

/**
 * Takes a Moodle XML export file of questions and exports all the
 * multiple choice questions into a csv file.
 * 
 * Usage php mc2csv.php --in questions.xml
 *
 * Optional arguments:
 * --delimiter char    Delimiter character for the csv file, default is ";"
 * --keephtml          Do not strip html tags at all.
 * --keeptags 'a,b,c'  List of tags that should not be eliminated when
 *                     stripping html from the questions. The default
 *                     tags that are not purged: i,img,s,strong,sub,sub,u
 * --out filename.csv  if not provided the base name of the xml file is
 *                     used, trailed by a .csv suffix.
 *         
 **/

// Predefined variables.
$infile = $outfile = null;
$delimiter = ';';
$keeptags = ['i', 'img', 's', 'strong', 'sub', 'sub', 'u'];
$striptags = true;

$args = $_SERVER['argv'];
array_shift($args);

// Start handling the command line arguments.
$carg = null;
while ($arg = array_shift($args)) {
    if ($arg === '--in' || $arg === '--out' || $arg === '--keeptags' || $arg === '--delimiter') {
        $carg = $arg;
        continue;
    }
    if ($arg === '--keephtml') {
        $striptags = false;
        continue;
    }
    if ($arg === '--help') {
        $echo = false;
        $fp = fopen($_SERVER['argv'][0], 'r');
        while ($line = fgets($fp)) {
            if ($echo) {
                if (trim($line) === '**/') {
                    fclose($fp);
                    dieNice();
                }
                $line = substr($line, 3);
                if (!empty($line)) {
                    echo $line;
                } else {
                    echo "\n";
                }
                continue;
            }
            if (substr($line, 0, 3) === '/**') {
                $echo = true;
            }
        }
        dieNice();
    }
    if ($carg === '--in') {
        $infile = $arg;
        $carg = null;
        continue;
    }
    if ($carg === '--out') {
        $outfile = $arg;
        $carg = null;
        continue;
    }
    if ($carg === '--keeptags') {
        $keeptags = array_map(fn($t) => trim($t), explode(',', $arg));
        $carg = null;
        continue;
    }
    if ($carg === '--delimiter') {
        if (strlen($delimiter) > 1) {
            dieNice(5, 'Delimiter must be a single character only.');
        }
        $delimiter = $arg;
        $carg = null;
        continue;
    }
    dieNice(1, 'invalid argument ' . $arg);
}
// End of handling the command line arguments.

// Start working here...
if (!$infile) {
    dieNice(1, 'No Moodle XML File provided.');
}
if (!file_exists($infile)) {
    dieNice(2, 'File ' . $infile . ' does not exist.');
}
if (!$data = file_get_contents($infile)) {
    dieNice(2, 'Could not read file ' . $infile);
}
if (!$xml = simplexml_load_string($data)) {
    dieNice(3, 'Could not parse XML from file ' . $infile);
}
if (!$outfile) {
    $p = strrpos($infile, '.');
    if ($p === false) {
        $p = strlen($infile);
    }
    $outfile = substr($infile, 0, $p) . '.csv';
}
$fout = fopen($outfile, 'wb');
if (!$fout) {
    dieNice(4, 'Could not open ' . $outfile . ' for writing');
}

$cols = [];
$csvdata = [];

foreach ($xml->xpath('//question') as $question) {
    handler($question);
}

fputcsv($fout, $cols, $delimiter);
foreach ($csvdata as $line) {
    while (count($line) < count($cols)) {
        $line[] = '';
    }
    fputcsv($fout, $line, $delimiter);
}
fclose($fout);
// Finshed working here.

/**
 * Get column number for a column name.
 * @param string $name
 * @return int
 */
function getColIdx(string $name): int {
    global $cols;
    foreach ($cols as $i => $col) {
        if ($col === $name) {
            return $i;
        }
    }
    $cols[] = $name;
    return count($cols) - 1;
}

/**
 * Format/strip html tags from a value.
 * @param string $value
 * @return string
 */
function formatHtml(string $value): string {
    global $striptags, $keeptags;
    if ($striptags) {
        return strip_tags($value, $keeptags);
    }
    return $value;
}

/**
 * Handler function that (in this case) handles the mc questions.
 * @param $question
 * @return void
 */
function handler($question) {
    global $csvdata;
    if ((string)$question['type'] === 'multichoice') {
       $row = [];
       $row[getColIdx('name')] = trim($question->name->text ?? '');
       $row[getColIdx('questiontext')] = formatHtml((string)$question->questiontext->text ?? '');
       $row[getColIdx('generalfeedback')] = formatHtml((string)$question->generalfeedback->text ?? '');
       $row[getColIdx('defaultgrade')] = (float)$question->defaultgrade ?? 0.0;
       $row[getColIdx('penalty')] = (float)$question->penalty ?? 0.0;
       $row[getColIdx('hidden')] = (int)$question->hidden ?? 0;
       $row[getColIdx('idnumber')] = (string)$question->idnumber ?? '';
       $row[getColIdx('single')] = ((string)$question->single ?? 'true') === 'true' ? 1 : 0;
       $row[getColIdx('shuffleanswers')] = ((string)$question->shuffleanswers ?? 'true') === 'true' ? 1 : 0;
       $row[getColIdx('answernumbering')] = (string)$question->answernumbering ?? '';
       $row[getColIdx('showstandardinstruction')] = (int)$question->showstandardinstruction ?? 0;
       $row[getColIdx('correctfeedback')] = formatHtml((string)$question->correctfeedback->text ?? '');
       $row[getColIdx('partiallycorrectfeedback')] = formatHtml((string)$question->partiallycorrectfeedback->text ?? '');
       $row[getColIdx('incorrectfeedback')] = formatHtml((string)$question->incorrectfeedback->text ?? '');
       $i = 1;
       foreach($question->answer as $answer) {
           $row[getColIdx('answer_' . $i)] = formatHtml((string)$answer->text ?? '');
           $row[getColIdx('answer_' . $i . '_fraction')] = (float)$answer['fraction'] ?? 0.0;
           $row[getColIdx('answer_' . $i . '_feedback')] = formatHtml((string)$answer->feedback->text ?? '');
           $i++;
       }
       $csvdata[] = $row;
    }
}

/**
 * Terminate the script with an exit code.
 * @param int $code
 * @param string|null $msg
 * @return void
 */
function dieNice(int $code = 0, ?string $msg = null) {
    if ($code > 0) {
        echo $msg . PHP_EOL;
        echo 'See --help for more details' . PHP_EOL;
    }
    exit($code);
}
