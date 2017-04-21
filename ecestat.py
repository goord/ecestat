#!/usr/bin/env python

import sys
import os.path
import json
import argparse
import collections

statusfile = os.path.join(os.path.dirname(os.path.realpath(__file__)),".ecestat.json")

def load_stats():
    if(not os.path.exists(statusfile)):
        return {"status" : [],"legs" : collections.OrderedDict}
    statustext = open(statusfile).read()
    return json.loads(statustext,object_pairs_hook = collections.OrderedDict)

def write(data):
    with open(statusfile,'w') as ofile:
        json.dump(data,ofile,indent = 4,separators = (',',':'))

def main(args):
    parser = argparse.ArgumentParser(description = "status retriever/updater")
    parser.add_argument("--upgrade", metavar = "leg",  dest = "row", type = str, default = None, help = "Upgrade the status of a leg")
    parser.add_argument("--addstat", metavar = "stat", dest = "col", type = str, default = None, help = "Add a new status to the stat file")
    args = parser.parse_args()
    newstat,leg = args.col,args.row
    data = load_stats()
    if(newstat):
        stattuple = newstat.split(':')
        stat = stattuple[0]
        if(len(stattuple) > 1):
            index = int(stattuple[1])
            data["status"].insert(index,stat)
        if(len(stattuple) > 2):
            print "Ignoring argument substrings",stattuple[2:]
        else:
            data["status"].append(stat)
        if(leg): print "Ignoring extra arguments --update",leg
        write(data)
    elif(leg):
        if(leg in data["legs"]):
            curstat = data["legs"][leg]
            index = data["status"].index(curstat)
            if(index < len(data["status"]) - 1):
                data["legs"][leg] = data["status"][index + 1]
                write(data)
            else:
                print "Ignored final status update"
        else:
            if(len(data["status"]) > 0):
                data["legs"][leg] = data["status"][0]
                write(data)
            else:
                print "No statuses were defined in the stat file"
    else:
        print "defined statuses:",' '.join(data["status"])
        for leg in data["legs"]:
            print leg,":",data["legs"][leg]

if __name__ == "__main__":
    main(sys.argv[1:])
