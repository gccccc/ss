# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class baseInfoPipeline(object):
    def process_item(self, item, spider):
    	dic = dict(item)
        '''
    	if 'area' in dic:
    		print dic
        	with open('./base_info.list','a+') as f:
        		output_info = json.dumps(dic, sort_keys=True, indent=3)
        		f.write('%s\n' % output_info)
        else:
        '''
        #with open('./new_allinfo.list','a+') as f:
        #	output_info = json.dumps(dic, sort_keys=True, indent=3)
        #	f.write('%s\n' % output_info)
        with open('./line.list','a+') as f:
        	area = '%s,%s,%s' % (dic['area']['province_name'], dic['area']['city_name'], dic['area']['area_name'])
        	#output_info = '%s %s %s %s %s %s %s %s %s\n' % (dic['name'].ljust(20), dic['projectname'].ljust(20), dic['projectkind'].ljust(20), dic['projectproperty'].ljust(20), dic['fundtype'].ljust(20), dic['phone'].ljust(20), dic['mobilephone'].ljust(20), dic['website'].ljust(20), area.ljust(20))
        	output_info = '%s || %s || %s || %s || %s || %s || %s' % (dic['name'], dic['projectname'], dic['year'], dic['phone'], dic['mobilephone'], area, dic['website'])
        	f.write('%s\n' % output_info)
        return item
