# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import lxml.html as lhtml
from lxml.html import builder as E
from lxml import etree

class TableAdderPipeline(object):
    def __init__(self):
        self.file_path = '../../NewsView/index.html'

        # Can not be opened in append or write mode for etree parsing
        self.index = open(self.file_path, 'r')
        self.html = lhtml.parse(self.index)
        self.table_section = self.html.xpath('//section')[0]
        self.table_section.clear()
        self.table_section.set('class', 'news')
    
    def process_item(self, item, spider):
        self.build_item_container(item)
        return item

    def build_item_container(self, item):
        try:
            content = item['content'][0]
            table = lhtml.fromstring(content)
            table.set('class', 'table')
            for subelement in table.findall('.//img'):
                subelement.getparent().remove(subelement)
            
            panel = E.DIV(
                        E.CLASS('panel panel-default'),
                        E.DIV(
                            E.CLASS('panel-heading'),
                            item['name']
                        ),
                        lhtml.fromstring( lhtml.tostring(table) )
                    )
        except IndexError:
            panel = E.DIV(
                        E.CLASS('panel panel-default'),
                        E.DIV(
                            E.CLASS('panel-heading'),
                            item['name']
                        ),
                        E.DIV(
                            E.CLASS('panel-body'),
                            E.P("No hay discusiones")
                        )
                    )
        self.table_section.append(panel)
        self.index.close()
        self.index = open(self.file_path, 'w')
        self.index.write( lhtml.tostring(self.html) )
        self.index.close()