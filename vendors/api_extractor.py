import requests
import time
from db_connector import RevisionDB

class RevisionExtractor(object):

    def __init__(self, payload={}, url='https://en.wikipedia.org/w/api.php', wait_time=2):
        self.payload = {
                'action': 'query',
                'format': 'json',
                'prop': 'revisions',
                'rvlimit': '50',
                'rvprop': 'ids|flags|timestamp|user|flags|user|userid|size|sha1|contentmodel|comment|parsedcomment|content|tags',
            }
        self.payload.update(payload)

        self.url = url
        self.wait_time = wait_time

    def get_all(self):
        # Get the last revision extracted allocated in the DB
        revendid=self.find_last_revid()
        if revendid != 0:
            self.payload.update({'rvendid': revendid})
        batch = self.get_one()

        while ("continue" in batch):
            time.sleep(self.wait_time)
            self.payload.update({'rvcontinue': batch["continue"]["rvcontinue"]})
            batch = self.get_one()

    def get_one(self):
        if self.url != None:
            r = requests.get(self.url, params=self.payload)
            if r.status_code == requests.codes.ok:
                response = r.json()
                # Next Key its the id of the wiki.
                # Get json key an use it to access the revisions
                ks = list(response["query"]["pages"])
                ks[0]
                #save data to db
                self.save(response["query"]["pages"][ks[0]]["revisions"])
                return r.json()
            else:
                return r.raise_for_status()

    def save(self, revision):
        RevisionDB.insert(revision)

    def remove_all(self):
        RevisionDB.remove()
    
    def find_last_revid(self):
        revision=RevisionDB.find_last()
        if revision != None:
            revid=0
            for rev in revision:
                revid=rev['revid']
        else:
            revid=0
        return revid
        

#extractor = RevisionExtractor(payload={'titles': "Malazan Book of the Fallen"})
#content = extractor.get_all()
