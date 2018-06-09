#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 13:28:03 2018

@author: codemaker
"""

import urllib2
import collections

def get_page(url):
    #return page html from url
    try:
        return [url,urllib2.urlopen(url).read()]
    except:
        return [url,""]         

def get_next_url(page):
    #goes through page html from a starting position and finds the next url
    start_link = page[1].find('<a href="http')
    if start_link == -1:
        return None, 0
    end_link = page[1].find('"', start_link + len('<a href="'))
    url = page[1][start_link + len('<a href="'): end_link]
    return url, end_link           

def get_all_links(page):
    #returns all urls from a page
    links = []
    while True:
        url,end_link = get_next_url(page)
        if url:
            links.append(url)           
            page[1] = page[1][end_link:]
        else:
            return links

def crawl_web(seed, to_crawl, crawled):
    #calls get_all_links to crawl webpage, updates crawled and to_crawl.
    to_crawl.remove(seed)
    if seed not in crawled:
        new_links = set(link for link in get_all_links(get_page(seed)))
        to_crawl = to_crawl.union(new_links)
        crawled.add(seed)

    return crawled, to_crawl, new_links

def track_depth(url, maxdepth):
    #sets depth of webcrawl, feeds seed url to webcrawler
    depth = 0
    tier = [[url]]
    to_crawl = set([url])
    crawled = set()
    while depth < maxdepth:   
        next_tier = []
        for next_url in tier[depth]:
            crawled, to_crawl, new_links = crawl_web(next_url, to_crawl,
                                                     crawled)
            next_tier += list(new_links)
        tier.append(next_tier)
        depth += 1
    return tier, crawled, to_crawl


def get_next_string(page):
    #finds string in html of page using paragraph markers
    start_string = page[1].find('<p>')
    if start_string == -1:
        return None, 0
    end_string = page[1].find('</p>', start_string + len('<p>'))
    string = page[1][start_string + len('<p>'): end_string]
    return string, end_string

def get_page_words(page):
    #gets all strings on page and converts to word list
    page_string = ''
    to_remove = '#$%^&*._,1234567890+=<>/\()":;!?'
    while True:
        string, end_string = get_next_string(page)
        if string:
            page_string += " " + string           
            page[1] = page[1][end_string:]
        else:
            for i in to_remove:        
                page_string = page_string.replace(i, '').lower()
                page_words = page_string.split()
            return page_words

def word_bank(crawled):
    #creates word index mapping url values to word keys    
    crawled = list(crawled)
    word_count = {}  
    for url in crawled:
        for word in get_page_words(get_page(url)):
            if word in word_count:
                if url in word_count[word]:
                    word_count[word][url] += 1
                else:
                    word_count[word][url] = 1
            elif len(word) < 15:
                word_count[word] = {url: 1}
    return word_count

def search_engine(target_string, word_count):
    #searches word_bank for words in string, returns urls words are found at
    targets = list(set(target_string.split()))
    result =[]
    for word in targets:
        if word in word_count:
            result += word_count[word].keys()
    ans = collections.Counter(result).most_common()
    return ans[0][0]

crawled = track_depth("http://xkcd.com/1427/", 2)[1]
print "crawling done"
word_count = word_bank(crawled)
print "word_count done"
#print word_count
print search_engine('starting blogs about', word_count)