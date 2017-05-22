from __future__ import absolute_import, unicode_literals
from .. import celery
from config import config, Config
from vendors.db_connector import RevisionDB
from vendors.query_handler import QueryHandler
from vendors.api_extractor import RevisionExtractor
import time


@celery.task(bind=True)
def hello(self):

    for x in xrange(1, 11):
        print "Hello World! %d" % x
        self.update_state(state='PROGRESS',
                          meta={'status': "Hello World Step %d / 10!" % x})
        time.sleep(2)

    return {'status': 'Task completed!',
            'result': "Hello World Step %d / 10" % x}


@celery.task(bind=True)
def extract_article(self, title):

    db = RevisionDB(config={'host': Config.MONGO_HOST, 'port': Config.MONGO_PORT, 'username': Config.MONGO_USERNAME, 'password': Config.MONGO_PASSWORD})

    extractor = RevisionExtractor(payload={'titles': title},title=title, db=db)
    total = extractor.get_all(self)

    return {'status': 'Task completed!',
            'result': "%d revisions extracted" % total}

@celery.task(bind=True)
def clean_revisions(self, title):

    db = RevisionDB(config={'host': Config.MONGO_HOST, 'port': Config.MONGO_PORT, 'username': Config.MONGO_USERNAME, 'password': Config.MONGO_PASSWORD})

    db.find_query({formatted: False})

    self.update_state(state='IN PROGRESS', meta={'status': "%d revisions extracted" % (2)})
    return {'status': 'Task completed!',
            'result': "%d revisions extracted" % total}
            
@celery.task(bind=True)
def count_task(self,code,values):

    db = RevisionDB(config={'host': Config.MONGO_HOST, 'port': Config.MONGO_PORT, 'username': Config.MONGO_USERNAME, 'password': Config.MONGO_PASSWORD})
    #instantiate a new QueryHandler to get execute the corresponding function
    handler = QueryHandler(db=db)
    number = handler.get_count(code,values)

    return {'status': 'Task completed!', 
            'count': "%d" % number}

@celery.task(bind=True)
def avg_task(self,code,values):

    db = RevisionDB(config={'host': Config.MONGO_HOST, 'port': Config.MONGO_PORT, 'username': Config.MONGO_USERNAME, 'password': Config.MONGO_PASSWORD})
    #instantiate a new QueryHandler to get execute the corresponding function
    handler = QueryHandler(db=db)
    number = handler.get_avg(code,values)

    return {'status': 'Task completed!', 
            'avg': "%f" % number}

@celery.task(bind=True)
def mode_task(self,attribute,code,values):

    db = RevisionDB(config={'host': Config.MONGO_HOST, 'port': Config.MONGO_PORT, 'username': Config.MONGO_USERNAME, 'password': Config.MONGO_PASSWORD})
    #instantiate a new QueryHandler to get execute the corresponding function
    handler = QueryHandler(db=db)
    number = handler.get_mode(attribute,code,values)

    return {'status': 'Task completed!', 
    'result': "%s" % number}

