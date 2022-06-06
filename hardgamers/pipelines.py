# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter

from scrapy.pipelines.images import ImagesPipeline

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class HardgamersPipeline:
    def process_item(self, item, spider):
        return item


class customImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        return request.url.split('/')[-1]

    def item_completed(self, results, item, info):
        file_paths = [x['path'] for ok, x in results if ok]
        if not file_paths:
            raise DropItem("Item contains no files")
        adapter = ItemAdapter(item)
        adapter['file_paths'] = file_paths
        return item