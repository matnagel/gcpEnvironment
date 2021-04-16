import apache_beam as beam
from apache_beam.io import fileio
from apache_beam.options.pipeline_options import PipelineOptions

from datetime import datetime
import time

from bs4 import BeautifulSoup
from zipfile import ZipFile, ZIP_DEFLATED
from gcp.SqlSources import Price, StdSource

import argparse
from sys import argv

import re
from functools import reduce

import logging

class Webpage:
    def __init__(self, isin, scrapeDate, content):
        self.isin = isin
        self.scrapeDate = scrapeDate
        self.content = content
    def __str__(self):
        return f"Webpage({self.isin}, {self.scrapeDate})"
    @staticmethod
    def recoverFromFile(filename, content):
        filename = filename.replace('_', '.')
        parts = filename.split('.')
        isin = parts[1]
        dateString = parts[0]
        scrapeDate = datetime.strptime(dateString, "%y%m%d")
        return Webpage(isin, scrapeDate, content)

def filesToProcess(bucketName):
    return fileio.MatchFiles(f"{bucketName}/*") | fileio.ReadMatches()

def laterThanCutOff(cutOffDate, f):
    m = re.search('([0-9]{6})Scrapes', f.metadata.path)
    if m:
        cur = datetime.strptime(m[1], "%y%m%d")
        return cur > cutOffDate
    return False

def unzipFiles(zipHandle):
    with zipHandle.open() as zipMemory, ZipFile(zipMemory, 'r', ZIP_DEFLATED) as zipFile:
        for name in zipFile.namelist():
            cont = zipFile.read(name)
            yield (name, cont)

def convertToWebpage(t):
    return Webpage.recoverFromFile(t[0], t[1])

class saveToDB(beam.DoFn):
    def __init__(self, sqlConf):
        self.sqlConf = sqlConf
    def setup(self):
        self.source = StdSource(self.sqlConf)
    def teardown(self):
        self.source.tearDown()
    def process(self, element):
        self.source.addRow(element)
        self.source.commit()
        yield element


def extractId(soup, css):
    #setlocale(LC_NUMERIC, 'de_DE.UTF-8')
    html = soup.select(css)[0]
    txt = html.text.replace(' ', '')
    txt = txt.replace(',', '.')
    return float(txt)
    #return atof(txt)

def toPrice(webpage):
    rawPage = webpage.content
    soupPage = BeautifulSoup(rawPage, 'html.parser')
    try:
        last = extractId(soupPage, '#last')
        high = extractId(soupPage, '#high')
        low = extractId(soupPage, '#low')
    except ValueError:
        print(f"Malformed page returned for {isin}")
    return Price(isin=webpage.isin, date=webpage.scrapeDate, last=last, high=high, low=low)

# def verifyPreconditions(source):
#     stocks = source.query(Stock)
#     if len(list(stocks)) >= 25:
#         raise ValueError('There are more than 25 stocks to update')
#     lastUpdate = source.query(Price.date).order_by(Price.date.desc()).first()
#     today = date.today()
#     if lastUpdate.date >= today:
#         raise RuntimeError(f'Already have entries with date {lastUpdate.date}, which is today {today} or later. Only updates once a day.')

def combinePrices(iterator):
    return reduce(lambda x,y: x + "\n" + y, iterator, "")


def loadTradegatePipeline(bucketName, cutOffDate, sqlConf):
    return 'Load Files' >> filesToProcess(bucketName) \
              | beam.Filter(lambda f: laterThanCutOff(cutOffDate, f)) \
              | 'Unzip Files' >> beam.FlatMap(unzipFiles) \
              | 'Extract Prices' >> beam.Map(convertToWebpage) \
              | beam.Map(toPrice) \
              | 'Save result in DB' >> beam.ParDo(saveToDB(sqlConf)) \
              | 'Compute Result' >> beam.Map(lambda x: x.__str__()) \
              | beam.CombineGlobally(combinePrices) \
              | 'Log output' >> beam.Map(logging.info)
              #| beam.ParDo(saveToDB())

def runBeam():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cutOffDate', required=True)
    parser.add_argument('--bucketName', required=True)
    parser.add_argument('--dbuser', required=True)
    parser.add_argument('--dbpass', required=True)
    parser.add_argument('--dbname', required=True)
    parser.add_argument('--dbhost', required=True)
    parser.add_argument('--dbport', required=True)

    args, beam_args = parser.parse_known_args(argv)
    vargs = vars(args)

    bucketName = vargs['bucketName']
    cutOffDate = datetime.strptime(vargs['cutOffDate'], "%Y-%m-%d")

    sqlConf = dict()
    sqlConf['DB_USER'] = vargs['dbuser']
    sqlConf['DB_PASS'] = vargs['dbpass']
    sqlConf['DB_NAME'] = vargs['dbname']
    sqlConf['HOST'] = vargs['dbhost']
    sqlConf['PORT'] = vargs['dbport']

    pipeline_options = PipelineOptions(beam_args[1:])
    pipeline_options.view_as(SetupOptions).save_main_session = True
    with beam.Pipeline(options=pipeline_options) as p:
            p | loadTradegatePipeline(bucketName, cutOffDate, sqlConf)

if __name__ == '__main__':
    runBeam()
