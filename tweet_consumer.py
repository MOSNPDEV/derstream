import time

import numpy as np

from confluent_kafka import Consumer, KafkaError

from utilities import Tweet, Keywords, Keeper

conf_local_consumer = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': '%s-consumer' % 'local',
    'auto.offset.reset': 'earliest',
    'session.timeout.ms': 6000,
    'default.topic.config': {'auto.offset.reset': 'smallest'},
    'queue.buffering.max.messages': 10000,
    'queue.buffering.max.ms': 10,
    'batch.num.messages': 10,

}


# TODO: Clean consume-listener, split it in logic parts.
class TweetKafkaConsumer:
    '''
    Initializes a Kafka consumer. The consumer receives the messages sent by the producer and processes them
    by cleaning up the tweet using the methods defined in Tweet() and.
    In this case, the tweet is analysed for the 100 most frequently used english adjectives. If such an adjective
    occurs, a dictionary is updated accordingly. In regular time intervals, the dict is saved as an .npy file.
    ...

    Attibutes
    ---------
    configuration_dict : dict
        The configuration of the consumer specified as 'property.type': 'property-value'.

    Methods
    ---------
    consumer_setup
        Initializes the consumer with the given configuration. Can be used to reinitialize the consumer.

    consumer_subscribe:
        Subscribes to the specified topic (str).

    consumer_close:
        Closes the currently active subscription.

    consumer_listen:
        Receives the messages sent by the producer and processes them. Saves a dict which counts word
        occurrences in a regular interval specified by time_interval.

    '''
    def __init__(self, configuration_dict=conf_local_consumer):
        self._consumer = Consumer(**configuration_dict)

    def consumer_setup(self, configuration_dict):
        self._consumer = Consumer(**configuration_dict)

    def consumer_subscribe(self, topic):
        self._consumer.subscribe(topic)

    def consumer_close(self):
        self._consumer.close()

    def consumer_listen(self, time_interval):
        adj_dict = Keywords()
        time_keeper = Keeper()
        while True:
            message = self._consumer.poll(0)
            if message is None:
                continue
            if message.error():
                if message.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(message.error())
                    break

            tweet = Tweet(message.value().decode('utf-8'))
            tweet.process_tweet()
            adj_dict.update_keyword_count(tweet.get_keywords())
            time_keeper.increment_counter()

            if time.time() - time_keeper.get_time() > time_interval:
                time_keeper.reset_time()
                print(sum(adj_dict.get_dict().values()), time_keeper.get_counter())
                np.save("tweet_dict" + str(int(time.time())) + "_" + str(time_keeper.get_counter()) + ".npy",
                        adj_dict.get_dict())
                time_keeper.reset_counter()
                adj_dict.reset_dict()

        self._consumer.close()

