
######################### XML_BASE #########################
############################################################
################ AUTHOR: FLORIAN LARDEUX ###################
############################################################
######################## 10/21/2022 ########################
############################################################

import re

""" Node class =============================================
	Provides methods for building an XML node
	name: name of the node
	content: self-contained information (text, single tags)
	children: children nodes
"""
class Node:
	def __init__(self, name):
		self.content = []
		self.children = {}
		self.name = name

	""" add some content to the node
		content: list of strings
	"""
	def add_content(self, content):
		self.content.append(content)

	""" add a child to the node
		child: child node
		returns the list of children
	"""
	def add_child(self, child):
		self.children[child] = Node(child)
		return self.children[child]

	""" [recursive]
		generate a string for printing the node
		value: string
	"""
	def get_repr(self, value):
		value += "Node '" + self.name + "': "
		for content in self.content:
			value += content + " "

		if len(self.children) == 0:
			return value

		else:
			for child in self.children.values():
				value += '\n' + child.get_repr("")

		return value

	""" printing of the node """
	def __repr__(self):
		return self.get_repr("")

	""" length of the node's children list """
	def __len__(self):
		return len(self.children)


""" Xml class =============================================
	Provides methods for building an general Xml object,
	which in itself is basically a node.
	filename: full path to the xml file
	xml: xml root node
"""
class Xml:
	def __init__(self, filename=""):
		self.filename = filename
		self.xml = None
		if filename != "":
			self.parse_file()

	def __repr__(self):
		return self.xml.get_repr("")

	""" General class getter
		returns an Xml object based on its path
	"""
	@classmethod
	def get(cls, filename):
		xml_obj = cls(filename)
		return xml_obj

	""" Sets the full path to the xml file 
		filename: full path string
	"""
	def set_file(self, filename):
		self.filename = filename

	""" [recursive]
		General parsing of a single node based on a list of lines of the xml file.
		node: current node
		lines: list of lines of the xml file
		index: current line index
	"""
	def parse_node(self, node, lines, index):
		while index < len(lines):
			line = lines[index]

			# kick first spaces
			s = re.search("( *\t*)*", line)
			if s is not None:
				span = s.span()
				line = line[span[1]:]

			# empty line
			if line == "" or line == "\n":
				index += 1
				continue

			# comment
			elif re.search("^<!--.*-->$", line):
				index += 1
				continue

			# tag
			elif re.search("^<.*>$", line):
				node_name = line.split('<')[1].split('>')[0]

				# content tag
				if re.search("^<.*/>$", line):
					content = line.split('<')[1].split('/>')[0].split("\n")[0]
					node.add_content(content)
					index += 1

				# inline node tag
				elif re.search("(<.*?>)(.*)(<.*?>)", line):
					content = line.split('>')[1].split('</')[0].split("\n")[0]
					subnode = node.add_child(node_name)
					subnode.add_content(content)
					index += 1
						
				# end node
				elif re.search("^</.*>$", line):
					index += 1
					break

				# node tag
				else:
					content = line.split('>')[1].split('</')[0].split("\n")[0]
					subnode = node.add_child(node_name)
					subnode.add_content(content)
					index = self.parse_node(subnode, lines, index+1)

				continue

			else:
				# non specific tag
				content = line.split("\n")[0]
				node.add_content(content)
				index += 1
				continue

		return index

	""" General parsing of the file """
	def parse_file(self):
		# read file
		lines = []
		with open(self.filename, 'r') as f:
			for line in f:
				lines.append(line)

		if len(line) == 0:
			return "No data"

		# store data
		self.xml = Node("root")
		self.parse_node(self.xml, lines, 0)

