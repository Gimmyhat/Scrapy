# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pymongo import MongoClient

from db import CLIENT
import re


class JobparserPipeline:
    def __init__(self):
        client = MongoClient(CLIENT)  # Подключаемся к MongoDB Atlas
        self.mongobase = client.vacancies

    def process_item(self, item, spider):

        item['min'], item['max'], item['cur'] = self.process_salary(item['salary'], spider.name)
        del item['salary']

        collection = self.mongobase[spider.name]
        collection.insert_one(item)

        return item

    def process_salary(self, salary: list, collection_name):
        min_salary, max_salary, cur_salary = None, None, None
        if len(salary) == 5:
            item = [[1, salary[3]], [2, 'руб']][collection_name == 'sjru']
            min_salary = [None, int(salary[item[0]].replace('\xa0', '').replace('руб.', ''))]['от' in salary[0]]
            max_salary = [None, int(salary[item[0]].replace('\xa0', '').replace('руб.', ''))]['до' in salary[0]]
            cur_salary = item[1]
        elif len(salary) > 5:
            item = [[1, 3, -2], [0, 4, -3]][collection_name == 'sjru']
            min_salary = int(salary[item[0]].replace('\xa0', ''))
            max_salary = int(salary[item[1]].replace('\xa0', ''))
            cur_salary = salary[item[2]]
        print()
        return min_salary, max_salary, cur_salary
