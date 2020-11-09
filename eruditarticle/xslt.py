# -*- coding: utf-8 -*-

import os
import io

import lxml.etree as et

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "xsl/marquage_to_html.xslt")
marquage_to_html = ""

with open(filename) as marquage_to_html_file:
    marquage_to_html = et.XSLT(et.parse(io.StringIO(marquage_to_html_file.read())))
