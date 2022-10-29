from xml_base import Xml
from xml_diff import XmlDiff

if __name__ == "__main__":

	file1 = "data/same1.xml"
	file2 = "data/same2.xml"

	xml1 = Xml.get(file1)
	xml2 = Xml.get(file2)

	options = {"ignore_json_order":False}

	identical = XmlDiff.process(xml1, xml2, options)
	if identical:
		print("Files are identical!")
	else:
		print("Files are different")




