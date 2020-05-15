# PS 5: RSS Feed Filter
#
# Name: Peter Bekins
# Date: 4/29/20
#

import feedparser
import string
import time
from project_util import translate_html
from news_gui import Popup

#-----------------------------------------------------------------------
#
# Problem Set 5

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        print entry
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        try:
            summary = translate_html(entry.summary)
        except AttributeError:
            summary = ""
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

#======================
# Part 1
# Data structure design
#======================

# Problem 1

class NewsStory(object):

    nextIDNum = 0

    def __init__(self, guid, title, subject, summary, link):
        self.guid = guid
        if self.guid == '':
            self.guid = NewsStory.nextIDNum
            NewsStory.nextIDNum += 1
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_subject(self):
        return self.subject

    def get_summary(self):
        return self.summary

    def get_link(self):
        return self.link

#======================
# Part 2
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5

# TODO: WordTrigger
class WordTrigger(Trigger):
    def __init__(self, word):
        self.word = word

    def is_word_in(self, text):
        test_word = self.word.lower()
        text_words = ''.join(i if i not in string.punctuation else ' ' for i in text).lower().split()
        #print test_word
        #print text_words
        if test_word in text_words:
            return True
        else:
            return False

# TODO: TitleTrigger
class TitleTrigger(WordTrigger):
    def evaluate(self, story):
        if self.is_word_in(story.title):
            return True
        else:
            return False
# TODO: SubjectTrigger
class SubjectTrigger(WordTrigger):
    def evaluate(self, story):
        if self.is_word_in(story.subject):
            return True
        else:
            return False
# TODO: SummaryTrigger
class SummaryTrigger(WordTrigger):
    def evaluate(self, story):
        if self.is_word_in(story.summary):
            return True
        else:
            return False


# Composite Triggers
# Problems 6-8

# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger

    def evaluate(self, story):
        return not(self.trigger.evaluate(story))


# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        if self.trigger1.evaluate(story) and self.trigger2.evaluate(story):
            return True
        else:
            return False

# TODO: OrTrigger

class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        if self.trigger1.evaluate(story) or self.trigger2.evaluate(story):
            return True
        else:
            return False

# Phrase Trigger
# Question 9

# TODO: PhraseTrigger

class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase

    def evaluate(self, story):
        phrase = self.phrase
        subject = story.subject
        title = story.title
        summary = story.summary

        if (phrase in subject) or (phrase in title) or (phrase in summary):
            return True
        else:
            return False


#======================
# Part 3
# Filtering
#======================

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory-s.
    Returns only those stories for whom
    a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    print "In filter module"
    print stories
    filtered_stories = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                filtered_stories.append(story)

    print filtered_stories

    return filtered_stories

#======================
# Part 4
# User-Specified Triggers
#======================

def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """
    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)

    # TODO: Problem 11
    # 'lines' has a list of lines you need to parse
    # Build a set of triggers from it and
    # return the appropriate ones
    triggers = []
    out_triggers = []
    for line in lines:
        if line.split()[0] != 'ADD':
            name = line.split()[0]
            type = line.split()[1]
            arg = line.split()[2:]
            if type == 'PHRASE':
                pt = PhraseTrigger(' '.join(arg))
                triggers.append((name, pt))
            elif type == 'SUBJECT':
                st = SubjectTrigger(arg[0])
                triggers.append((name, st))
            elif type == 'TITLE':
                tt = TitleTrigger(arg[0])
                triggers.append((name, tt))
            elif type == 'SUMMARY':
                st = SummaryTrigger(arg[0])
                triggers.append((name, st))
            elif type == 'NOT':
                for trigger in triggers:
                    if trigger[0] == arg[0]:
                        t1 = trigger[1]
                nt = NotTrigger(t1)
                triggers.append((name, nt))
            elif type == 'AND':
                for trigger in triggers:
                    if trigger[0] == arg[0]:
                        t1 = trigger[1]
                    elif trigger[0] == arg[1]:
                        t2 = trigger[1]
                at = AndTrigger(t1, t2)
                triggers.append((name, at))
            elif type == 'OR':
                for trigger in triggers:
                    if trigger[0] == arg[0]:
                        t1 = trigger[1]
                    elif trigger[0] == arg[1]:
                        t2 = trigger[1]
                ot = OrTrigger(t1, t2)
                triggers.append((name, ot))
        elif line.split()[0] == 'ADD':
            for t in line.split()[1:]:
                for trigger in triggers:
                    if trigger[0] == t:
                        out_triggers.append(trigger[1])

    return out_triggers

import thread

def main_thread(p):
    # A sample trigger list - you'll replace
    # this with something more configurable in Problem 11
    # t1 = SubjectTrigger("Obama")
    # t2 = SummaryTrigger("MIT")
    # t3 = PhraseTrigger("Supreme Court")
    # t4 = OrTrigger(t2, t3)
    # triggerlist = [t1, t4]
    
    # TODO: Problem 11
    # After implementing readTriggerConfig, uncomment this line 
    triggerlist = readTriggerConfig("triggers.txt")

    guidShown = []
    
    while True:
        print "Polling..."

        # Get stories from Google's Top Stories RSS news feed
        stories = process("http://news.google.com/?output=rss")
        # Get stories from Yahoo's Top Stories RSS news feed
        stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

        # Only select stories we're interested in
        stories = filter_stories(stories, triggerlist)
    
        # Don't print a story if we have already printed it before
        newstories = []
        for story in stories:
            if story.get_guid() not in guidShown:
                newstories.append(story)
        
        for story in newstories:
            guidShown.append(story.get_guid())
            p.newWindow(story)

        print "Sleeping..."
        time.sleep(SLEEPTIME)

SLEEPTIME = 60 #seconds -- how often we poll
if __name__ == '__main__':
    p = Popup()
    thread.start_new_thread(main_thread, (p,))
    p.start()

