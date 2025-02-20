# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import json
import time

import metapy

class RankedSearch:
    """
    Wraps the MeTA search engine and its rankers.
    """
    def __init__(self, cfg):
        """
        Create/load a MeTA inverted index based on the provided config file and
        set the default ranking algorithm to Okapi BM25.
        """
        self.idx = metapy.index.make_inverted_index(cfg)
        self.default_ranker = metapy.index.OkapiBM25()

    def search(self, request):
        """
        Accept a JSON request and run the provided query with the specified
        ranker.
        """
        start = time.time()
        query = metapy.index.Document()
        query.content(request['query'])
        ranker_id = request['ranker']
        try:
            ranker = getattr(metapy.index, ranker_id)()
        except:
            print("Couldn't make '{}' ranker, using default.".format(ranker_id))
            ranker = self.default_ranker
        response = {'query': request['query'], 'results': []}
        for result in ranker.score(self.idx, query):
            name = self.idx.metadata(result[0]).get('name')
            path = self.idx.metadata(result[0]).get('url')
            genre = self.idx.metadata(result[0]).get('genre')
            year = self.idx.metadata(result[0]).get('release year')

            response['results'].append({
                'score': float(result[1]),
                'name':name,
                'path': path,
                'genre': genre,
                'year': year
            })
        response['elapsed_time'] = time.time() - start
        return json.dumps(response, indent=2)