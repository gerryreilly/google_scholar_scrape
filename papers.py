#! python
# Scrape google scholar to extract list of papers by authors listed in csv file
# CSV files as input, columns Name and Institution (optional).  These must match profiles
# in google scholarly
#
# usage
#    papers.py -i inputfile -o outputfile
#
# Gerry Reilly, 24th January 2019

import scholarly
import csv
import sys
import getopt

authors = []
inputfile = ' '
outputfile = ' '

def parse_args(argv):
  global inputfile
  global outputfile
  try:
    opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
  except getopt.GetoptError:
    print('papers.py -i inputfile -o outputfile')
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print('papers.py -i <inputfile> -o <outputfile>')
      sys.exit()
    elif opt in ("-i", "--ifile"):
      inputfile = arg
    elif opt in ("-o", "--ofile"):
      outputfile = arg
  if inputfile is '' or outputfile is '':
    print('input and / or output file not specified')
    sys.exit(2)

def build_author_list():
  global authors
  with open(inputfile, newline='') as infile:
    authors_names = csv.DictReader(infile, delimiter=',', quotechar='|')
    authors = list(authors_names)

def extract_store_papers():
  with open(outputfile, 'w', newline='') as outfile:
    fieldnames = ['author', 'title']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for author in authors:
      print(author)
      if author['Name'] is not None:
        if author['Institution'] is not None:
          search_query = scholarly.search_author(author['Name'] + ', ' + author['Institution'])
        else:
          search_query = scholarly.search_author(author['Name'])
        author_details = next(search_query).fill()
        for pub in author_details.publications:
          writer.writerow({'author': author['Name'].encode('utf8'), 'title': pub.bib['title'].encode('utf8')})

def main(argv):
  parse_args(argv)
  build_author_list()
  extract_store_papers()

if __name__ == "__main__":
    main(sys.argv[1:])
