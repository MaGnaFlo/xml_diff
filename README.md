# xml_diff

This project is aimed at easily comparing two xml files. Most common xml comparators provided online do not take into account some possible differences between XMLs which
turn out not to be real differences but variations in the order of some parameters. The methods provided ensure a good reading and comparing without taking into account
such parasite differences.

Caveat: the program does not display differences. It only returns if files are identical or not.

## Examples of possible differences which do not impact the comparison
```xml
<somecontent>
  <data  expr="{'ParameterType':'Float','param:7.9'}" id="hello"/>
  <data  expr="{'ParameterType':'int','param:5'}" id="hola"/>
</somecontent>
```
and
```xml
<somecontent>
  <data  expr="{'param:5','ParameterType':'int'}" id="hola"/>
  <data  expr="{'ParameterType':'Float','param:7.9'}" id="hello"/>
</somecontent>
```
will be found identical.

## Requirements
- Tested on Windows, not on Linux or MacOs.
- Python 3

## Usage
Simply download the files and run the following command to test the example
```bash
python example.py --xml1 "data/same1.xml" --xml2 "data/same2.xml"
```
The example file shows the basics of how to use the XmlDiff class.
It is also possible to use directly the Xml class to perform a simple generation of an Xml object.

## What's next?
Future work may investigate the possibility of passing conditions to the comparison.
It is also possible to add more useful methods to Xml and improve some of them, including the printing of an Xml object.
