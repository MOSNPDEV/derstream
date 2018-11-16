import json

from confluent_kafka import Producer
from tweepy.streaming import StreamListener

from utilities import Tweet


class TweetKafkaProducer(StreamListener):
    '''
    Initializes a Kafka producer. The producer sends the messages which are collected from the twitter stream.
    ...

    Attibutes
    ---------
    configuration_dict : dict
        The configuration of the producer specified as 'property.type': 'property-value'.

    topic_name : str
        The name of the topic the messages are sent to.

    Methods
    ---------
    producer_setup
        Initializes the producer with the given configuration. Can be used to reinitialize the producer.

    on_data:
        Inherited method from the stream listener. Defines how each received tweet is processed.

    on_error:
        Inherited method which terminates the subscription and prints the error.

    '''
    def __init__(self, configuration_dict, topic_name="tweets"):
        self._topic_name = topic_name
        self._producer = Producer(**configuration_dict)

    def producer_setup(self, configuration_dict):
        self._producer = Producer(**configuration_dict)

    def on_data(self, data):
        tweet_json = json.loads(data)
        if "text" in tweet_json:
            tweet_text = tweet_json["text"]
            tweet = Tweet(tweet_text)
            tweet.sanitise()
            self._producer.produce(self._topic_name, tweet.get_tweet().encode('utf-8'), callback=delivery_report)
            self._producer.poll(0)

        return True

    def on_error(self, status):
        print(status)
        self._producer.flush()


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
    Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))