#!/usr/bin/env python

"""
vote_extractor.py: A script to extract votes from the canon.nrc.nl website and make a list of top ranked images.

Requires BeautifulSoup.

Use and modify as you see fit to apply to other results. Not guaranteed to work.

Roderik Koenders
"""

import os

from bs4 import BeautifulSoup

def create_addresses_file(pages, addresses_filename, base_url):
    """pages: int with number of pages."""
    outfile = file(addresses_filename, "w")
    for i in range(pages):
        outfile.write(base_url.format(i+1))
    outfile.close()

def wget_all_pages(addresses_filename):
    os.system("wget -i {0}".format(addresses_filename))


## A function to extract the information
def link_and_vote(item):
    #Feed a 'div' and get the link and number of votes
    s = item
    link = s.find("a", attrs={"class": "yf-link"}).get("href")
    votes = s.find("span", attrs={"class": "yf-count"}).text
    return (link, int(votes))

def get_results(pages):
    ##Read in all the files and append them to content list.
    content = []
    for i in range(pages):
        inf = file("index.html?page={0}".format(i+1), "r")
        content.append(inf.read())
        inf.close()

    ##And now extract the votes for each page
    all_votes = []
    for page in content:
        # Create a soup
        soup = BeautifulSoup(page)
        # Loop over all items in the page and run link extractor fn.
        for item in soup.find_all('div', attrs = {"class": "item yf-item"}):
            all_votes.append(link_and_vote(item))

    ## Sort the votes
    all_votes_sorted = sorted(all_votes, key=lambda x: x[1])

    return all_votes_sorted

if __name__ == "__main__":

    num_pages = 225
    addresses_filename = "addresses.txt"
    base_url = "http://canon.nrc.nl/?page={0}"
    create_addresses_file(num_pages, addresses_filename, base_url)

    wget_all_pages(addresses_filename)

    all_votes_sorted = get_results(num_pages)
    ## Get top 10 images:
    all_votes_sorted[-10:]

    ##Example results.
    # http://canon.nrc.nl/Picture/view/9379 with 2595 votes.
    # http://canon.nrc.nl/Picture/view/9804 with 2607 votes.
    # http://canon.nrc.nl/Picture/view/1279 with 2684 votes.
    # http://canon.nrc.nl/Picture/view/3046 with 2755 votes.
    # http://canon.nrc.nl/Picture/view/8006 with 2775 votes.
    # http://canon.nrc.nl/Picture/view/7877 with 2801 votes.
    # http://canon.nrc.nl/Picture/view/8779 with 2842 votes.
    # http://canon.nrc.nl/Picture/view/2771 with 2874 votes.
    # http://canon.nrc.nl/Picture/view/207 with 2932 votes.
    # http://canon.nrc.nl/Picture/view/10501 with 3201 votes.

