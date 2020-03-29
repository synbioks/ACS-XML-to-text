## acs-xml-parser
A tool for extracting text from ACS xml files.

### Setup

Update the following parameters in the second cell

```
input_path = directory to articles
output_path = directory to the output of this script
suppl_path = directory to the supplementary files of the articles
```

The script will recursively collect all xml files under the `input_path`, and will put the processed output under the `output_path`. The output files will have the same name as their corresponding input files but different extension (.pkl instead of .xml). The structure of the input directory will not be persisted in the output directory.

## Example

Original:

```
<working-directory>
+-- input-folder
|   |-- a.xml
|   |-- d.txt
|   +-- folder1
|       |-- b.xml
|       +-- folder2
|           +-- c.xml
+-- output-folder
    +-- <empty>
```

Running the script will give:

```
<working-directory>
|-- input-folder
|   |-- a.xml
|   |-- d.txt
|   +-- folder1
|       |-- b.xml
|       +-- folder2
|           +-- c.xml
+-- output-folder
    |-- a.pkl
    |-- b.pkl
    +-- c.pkl
```

## Input Format

ACS z39-96 standard xml files

## Output Format

Pickle files adhering to the following format:

```
{
    "abstract": "...",
    "keywords": [
        "keyword1",
        "keyword2",
        ...
    ],
    "body": [
        {
            "section": [introduction|method|materials|result|discussion|summary],
            "text": "..."
        }, ...
    ],
    issue_pub_date: "month/day/year",
    electron_pub_date: "month/day/year",
    suppl_files: [
        {
            "suppl_filename": "...",
            "rpath": "path/to/suppl_file",
            "is_sequence": [True|False]
        }, ...
    ]
}
```

`abstract` contains the abstract of the article\
`keywords` contains a list of keywords found in the metadata of the article\
`body` is a list of dictionary where each contains the text and the sections the text is from.\
`issue_pub_date` is the date the article is published in an issue.\
`electron_pub_date` is the date the article is published electronically.\
`suppl_files` contains a list of supplementary materials and where to find them.
