#! python3
# Author: John Berlin <jberlin@cs.odu.edu>.
import argparse
from glob import glob
import os
from zipfile import ZipFile
import json
import csv


class JoinAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, " ".join(values))


def rowMaper(fields, jrow):
    aRow = {}
    for field in fields:
        aRow[field] = jrow[field]
    return aRow


fields = ['WorkAngle', 'TravelAngle', 'CTWD', 'TravelSpeed', 'Aim', 'Technique', 'VerticalDirection', 'ElapsedTime',
          'DistanceAlongWeld']


def extra_all_in_dir(dir):
    print('in directory %s' % dir)
    zipCount = 0
    for aZip in glob(os.path.join(dir, '*.zip')):
        with ZipFile(aZip, 'r') as zin:
            zin.extractall(path=dir)
            zipCount += 1
    print('done extracting %d zip files' % zipCount)
    print('converting the extracted .txt files into .csv')
    csvCount = 0
    for aTextFile in glob(os.path.join(dir, '*.txt')):
        csvCount += 1
        csvName = '%s.csv' % os.path.splitext(aTextFile)[0]
        print(csvName)
        rowsOut = []
        with open(aTextFile, 'r') as textIn:
            for csvRow in map(lambda jrow: rowMaper(fields, jrow), json.load(textIn)):
                rowsOut.append(csvRow)
        with open(csvName, 'w+') as csvOut:
            csvWriter = csv.DictWriter(csvOut, fieldnames=fields)
            csvWriter.writeheader()
            csvWriter.writerows(rowsOut)
        os.remove(aTextFile)
    print('converted %d .txt files into .csv'%csvCount)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Batch .txt converter')
    parser.add_argument('-dir', nargs="+", action=JoinAction)
    args = parser.parse_args()
    for dir in filter(lambda maybeDir: os.path.isdir(os.path.join(args.dir, maybeDir)), os.listdir(args.dir)):
        dirPath = os.path.join(args.dir, dir)
        print('extracting all zips and converting .txt files to .csv for directory %s' % dirPath)
        extra_all_in_dir(dirPath)
