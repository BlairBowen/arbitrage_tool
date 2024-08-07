# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags
from common.helpers import read_yaml
from fuzzywuzzy import fuzz

def find_best_match(sport, input_name):
    best_match = None
    highest_similarity = 0

    if sport in read_yaml('sports')['two']:
        if '.' not in input_name.split(' ')[0]:
            split_name = input_name.split(' ')
            input_name = ' '.join([f'{split_name[0][0]}.', split_name[1]])
        return input_name.lower()
    else:
        config = read_yaml('leagues')[sport]
        # Compare the input name with each name in the list
        for team in config['teams']:
            similarity = fuzz.ratio(input_name, team)
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = team

        return best_match.lower()
    
def even_check(value):
    if value.lower() == 'even':
        return '+100'
    else:
        return value

class SportsbookScraperItem(scrapy.Item):
    # define the fields for your item here like:
    sideA = scrapy.Field(
        input_processor = MapCompose(remove_tags, lambda x: find_best_match('baseball-mlb', x)),
        output_processor = TakeFirst()
    )
    sideB = scrapy.Field(
        input_processor = MapCompose(remove_tags,  lambda x: find_best_match('baseball-mlb', x)), 
        output_processor = TakeFirst()
    )
    spread = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    spreadA = scrapy.Field(input_processor = MapCompose(remove_tags, even_check), output_processor = TakeFirst())
    spreadB = scrapy.Field(input_processor = MapCompose(remove_tags, even_check), output_processor = TakeFirst())
    total = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    over = scrapy.Field(input_processor = MapCompose(remove_tags, even_check), output_processor = TakeFirst())
    under = scrapy.Field(input_processor = MapCompose(remove_tags, even_check), output_processor = TakeFirst())
    moneyA = scrapy.Field(input_processor = MapCompose(remove_tags, even_check), output_processor = TakeFirst())
    moneyB = scrapy.Field(input_processor = MapCompose(remove_tags, even_check), output_processor = TakeFirst())
    moneyC = scrapy.Field(input_processor = MapCompose(remove_tags, even_check), output_processor = TakeFirst())
    date = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    gameCode = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())