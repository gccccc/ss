# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field
'''
name means enterprise register name
registertime means enterprise register time
'''

class baseInfoItem(scrapy.Item):
    index 				= 	Field() 
    name 				= 	Field()
    area				= 	Field() 
    registertime		= 	Field() 
    enterpriseproject	= 	Field() 
    teamplayproject		= 	Field()
    enterprisecoach		= 	Field() 
    serviceoutsourcing	= 	Field()
    fundtype			= 	Field()
    phonenum 			= 	Field()

class playInfoItem(scrapy.Item):
	index 				= 	Field() 
	name 				= 	Field()
	projectname			= 	Field()  
	projectkind			= 	Field() 
	projectproperty		= 	Field() 
	fundtype			= 	Field()
	phone            	=   Field()
	mobilephone			=   Field()
	website				=	Field()
	area				=   Field()
	year				=	Field()

'''
class nameToPhoneItem(scrapy.Item):
    name                =   Field()
    phonenum            =   Field()  
'''