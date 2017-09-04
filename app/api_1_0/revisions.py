from flask import Flask, request, jsonify, Response, url_for
import urlparse
from bson import json_util
from . import api,auto
from vendors.db_connector import RevisionDB

@api.route('/revisions', methods=['GET'])
@auto.doc()
def revisions():
    '''The function returns the content of the revisions.'''
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1

    db = RevisionDB(config={'host': config['default'].MONGO_HOST, 'port': config['default'].MONGO_PORT, 'username': config['default'].MONGO_USERNAME, 'password': config['default'].MONGO_PASSWORD})

    revisions = db.paginate(page)
    
    return Response(
        json_util.dumps(revisions),
        mimetype='application/json'
    )

