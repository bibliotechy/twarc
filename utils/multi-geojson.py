#!/usr/bin/env python

import json
import fileinput
from multiprocessing import Pool



def tweet2geojson(line):
    ret = None
    tweet = json.loads(line)
    if tweet["geo"]:
        ret = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    tweet["geo"]["coordinates"][1],
                    tweet["geo"]["coordinates"][0]
                ],
            },
            "properties": {
                "name": tweet["user"]["name"],
                "screen_name": tweet["user"]["screen_name"],
                "created_at": tweet["created_at"],
                "text": tweet["text"],
                "profile_image_url": tweet["user"]["profile_image_url"],
                "url": "http://twitter.com/%s/status/%s" % (
                    tweet["user"]["screen_name"], 
                    tweet["id_str"],
                )
            }
        }
        return ret

if __name__ == '__main__':

    features = []
    pool = Pool(4)
    results = pool.map(tweet2geojson, [line for line in fileinput.input()])
    pool.close()
    pool.join()
    geojson = {"type" : "FeatureCollection", "features": [result for result in results if result is not None]}
    print json.dumps(geojson, indent=2)


