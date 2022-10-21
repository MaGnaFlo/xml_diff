
######################### XML_DIFF #########################
############################################################
################ AUTHOR: FLORIAN LARDEUX ###################
############################################################
######################## 10/21/2022 ########################
############################################################

import re

""" XmlDiff class =============================================
	Provides general tools for the comparison of XMLs.
	identical: attribute False if XMLs are different, else True
"""
class XmlDiff:
	""" xml1, xml2: Xml objects"""
	def __init__(self, xml1, xml2):
		self.identical = self.diff_node(xml1.xml, xml2.xml)

	""" Principal result getter 
		xml1, xml2: Xml objects
		returns the identical attribute
	"""
	@classmethod
	def process(cls, xml1, xml2):
		diff_obj = cls(xml1, xml2)
		return diff_obj.identical

	""" [recursive]
		Processes the difference between 2 Nodes
		node1, node2: Noed objects
	"""
	def diff_node(self, node1, node2):
		if len(node1) != len(node2):
			return False

		identical, _, _ = self.diff_line(node1.name, node2.name)
		if not identical:
			return False
		
		for subnode_name in node1.children:
			found_child = self.corresponding_child(subnode_name, node2)

			if found_child is None:
				return False
			else:
				identical = identical and self.diff_content(node1.children[subnode_name], node2.children[found_child])
				if not identical:
					return False
				identical = identical and self.diff_node(node1.children[subnode_name], node2.children[found_child])
				
		return identical
	
	""" Process the difference between two node's list of contents
		node1, node2: Node objects
		returns boolean (True is identical)
				two strings (line1, line2) corresponding (if they exist) to the two corresponding contents in each node
	"""		
	def diff_content(self, node1, node2):
		identical = True
		for line1 in node1.content:
			for line2 in node2.content:
				found, _, _ = self.diff_line(line1, line2)
				if found:
					break
			identical = identical and found

		return identical

	""" [recursive]
		Processes the difference between two single contents
		line1, line2: strings of the content
	"""
	def diff_line(self, line1, line2, sep=" "):
		if sep == " ":
			s = re.search(sep, line1)
			if s is not None:
				span = s.span()
				start_keyword1 = line1[:span[1]]
				start_keyword2 = line2[:span[1]]

				if start_keyword1 != start_keyword2:
					return False, None, None
				else:
					line1_ = line1[span[1]:]
					line2_ = line2[span[1]:]
			else:
				line1_ = line1
				line2_ = line2
		else:
			line1_ = line1
			line2_ = line2

		blocks1 = line1_.split(sep)
		blocks2 = line2_.split(sep)

		if len(blocks1) != len(blocks2):
			return False, None, None

		else:
			for b1 in blocks1:
				found_in_blocks2 = False
				if b1 in blocks2:
					found_in_blocks2 = True

				else:
					for b2 in blocks2:
						s1, s2 = None, None
						if "expr=" in b1:
							s1 = re.search(r'{.*}"$', b1)
							s2 = re.search(r'{.*}"$', b2)

						if s1 is not None and s2 is not None:
							span1 = s1.span()
							span2 = s2.span()
							bb1 = b1[span1[0]+1:-2]
							bb2 = b2[span2[0]+1:-2]

							found_in_blocks2, _, _ = self.diff_line(bb1, bb2, ',')
							
							if found_in_blocks2:
								break

				if not found_in_blocks2:
					return False, None, None

			return True, line1, line2

	""" Returns the child in a Node corresponding to the name of a child of another node.
		subnode_name1: name of the query child
		node2: target node
	"""
	def corresponding_child(self, subnode_name1, node2):
		found_child = None
		for child in node2.children:
			found, name1, name2 = self.diff_line(subnode_name1, child)
			if found:
				found_child = name2
				break
		return found_child
