## acs-xml-parser.py
A tool for extracting text from ACS xml files.

### Usage

```
acs-xml-parser.py --input=<input-path> --output=<output-path>
```

The script will recursively collect all xml files under the directory given to the `--input` option, and will put the processed output under the direcotry given to the `--output` option. The output files will have the same name as their corresponding input files but different extension (.pkl instead of .xml). The structure of the input directory will not be persisted in the output directory.

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

Running the following commad:

```
acs-xml-parser.py --input=input-folder --output=output-folder
```

Result:

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
            "section": [...],
            "text": "..."
        }
    ]
}
```

`abstract` contains the abstract of the article\
`keywords` contains a list of keywords found in the metadata of the article\
`body` is a list of dictionary where each contains the text and the sections the text is from.