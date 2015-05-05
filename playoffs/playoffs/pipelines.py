from sqlalchemy.orm import sessionmaker

from models import *

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class PlayerPipeline(object):
    """pipeline for storing skater summary items in the database"""
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates game table if necessary.
        """
        engine = db_connect()
        create_game_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """
        Save games in the database.
        This method is called for every item in the pipeline component.
        """
        session = self.Session()

        game = GameModel(**item)

        try:
            session.add(game)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
    
        return item