import re
import regex
import time


class Tweet:
    '''
    Initializes a Tweet object which can then be used to process the tweet.
    This includes removal of links, tweets in non-latin alphabets and special characters.
    It also splits the string into keywords and removes words which are too short.
    ...

    Attibutes
    ---------
    tweet_text : str
        The text-message of a tweet.

    Methods
    ---------
    get_tweet
        Returns the text of the tweet as a string.

    get_keywords
        Returns the keywords of a tweet.

    remove_clutter
        Removes words which are shorter than some specified length.

    sanitise
        Removes non-latin characters.

    '''

    def __init__(self, tweet_text):
        '''
        Parameters
        ----------
        tweet_text : str
            The text-message of a tweet.
        '''
        self._tweet_text = tweet_text
        self._tweet_keywords = []

    def get_tweet(self):
        return self._tweet_text

    def get_keywords(self):
        return self._tweet_keywords

    def remove_clutter(self, length=2):
        words = self._tweet_text.split(" ")
        keywords = []
        for word in words:
            if len(word) > length:
                keywords.append(word)

        self._tweet_keywords = keywords

    def sanitise(self):
        text_wo_links = re.sub(r"http\S+", "", self._tweet_text)
        text_wo_links = re.sub('@[^\s]+', '', text_wo_links)
        self._tweet_text = regex.sub(u'\p{^Latin}+', u' ', text_wo_links)

    def process_tweet(self):
        self.sanitise()
        self.remove_clutter()


class Keywords:
    '''
    Keywords is the object which is used to count the frequency of specific words in the tweets.
    The words are in this case the 100 most frequently used english adjectives. However, other
    words may be used as well.
    ...

     Attibutes
    ---------
    adj_dict : dict
        A dictionary where keys are words and the values are the counts.

    Methods
    ---------
    get_dict
        Returns the current word count as a dict.

    reset_dict
        Resets the current word count.

    update_keyword_count
        Given a sequence (e.g. list) of keywords, the word count is updated.

    adjectives_setup
        Initiates a dict with words (in this case the 100 most frequently used english adjectives).
    '''
    def __init__(self, adj_dict=None):
        if adj_dict:
            self._adj_dict = adj_dict
        else:
            self._adj_dict = self.adjectives_setup()

    def get_dict(self):
        return self._adj_dict

    def reset_dict(self):
        self._adj_dict = self.adjectives_setup()

    def update_keyword_count(self, keywords):
        #for keyword in keywords:
        #    if keyword in self._adj_dict:
        #        self._adj_dict[keyword] += 1
        # A bit faster; does not count multiple occurrences.
        for key in set(keywords) & set(self._adj_dict.keys()):
            self._adj_dict[key] += 1


    @staticmethod
    def adjectives_setup():
        with open('adjectives.txt') as file:
            adjectives = file.readlines()
        return {line.split()[1]: 0 for line in adjectives}




class Keeper:
    '''
    A small class which keeps the starting time and the number of processed tweets in an globally accessible object.
    ...

    Attibutes
    ---------

    Methods
    ---------
    reset_time
        Resets the time to the current time.

    get_time
        Returns the starting time.

    reset_counter
        Resets the processed tweet count to 0.

    increment_counter
        Increments the processed tweet count by 1.

    get_counter
        Returns the number of processed tweets.
    '''
    def __init__(self):
        self._start_time = time.time()
        self._counter = 0

    def reset_time(self):
        self._start_time = time.time()

    def get_time(self):
        return self._start_time

    def reset_counter(self):
        self._counter = 0

    def get_counter(self):
        return self._counter

    def increment_counter(self):
        self._counter += 1