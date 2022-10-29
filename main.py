from xml_base import Xml
from xml_diff import XmlDiff
import argparse

if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("--xml1", type=str, help="original xml file")
	parser.add_argument("--xml2", type=str, help="xml file to be compared")
	args = parser.parse_args()

	xml1 = Xml.get(args.xml1)
	xml2 = Xml.get(args.xml2)

	identical = XmlDiff.process(xml1, xml2)
	if identical:
		print("Files are identical!")
	else:
		print("Files are different")




