import sys
import time
import unittest

import settings

from greenamqp.client_0_8 import Connection, Message

class TestEventlet(unittest.TestCase):

    def test_eventlet_per_channel(self):        
        from eventlet import spawn, sleep
        from eventlet.event import Event
        
        conn = Connection(**settings.connect_args)
        
        start_engines = Event()
        messages_to_send = 75

        def make_message(routing_key, i):
            return Message(u'%s message #%d' % (routing_key, i))
        
        def writer(channel_id, routing_key, read_ready):
            start_engines.wait()    

            chan = conn.channel(channel_id)
            read_ready.wait()
        
            for i in range(messages_to_send):
                msg = make_message(routing_key, i)
                chan.basic_publish(msg, 'amq.direct', routing_key=routing_key)
                sleep(0)
            
        def reader(channel_id, routing_key, read_ready):
            messages = []
            def got_message(m):
                messages.append(m)
                sleep(0)
    
            start_engines.wait()
            
            chan = conn.channel(channel_id)
            chan.queue_declare(queue=routing_key, exclusive=True)
            chan.queue_bind(routing_key, exchange='amq.direct', routing_key=routing_key)
            chan.basic_consume(queue=routing_key, callback=got_message)

            read_ready.send(True)            
            while(True):
                chan.wait()
                if len(messages) == messages_to_send:
                    break


        # set up a bunch of pairs of readers
        # and writers that are all sending 
        # and recieving on the same connection 
        # via separate channels.
        pairs = 25
        procs = []
        ch = conn.channel(pairs*2 + 2)
        for i in range(1, pairs + 1):
            key = 'q_%d' % i
            
            read_ready = Event()
            procs.append(spawn(writer, i, key, read_ready))
            procs.append(spawn(reader, i + pairs, key, read_ready))

        # tell them to begin...
        start_engines.send(True)

        for proc in procs:
            proc.wait()

        conn.close()
        

        
        
def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEventlet)
    unittest.TextTestRunner(**settings.test_args).run(suite)


if __name__ == '__main__':
    main()
