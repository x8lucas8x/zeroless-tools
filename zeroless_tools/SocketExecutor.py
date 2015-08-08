import sys
import warnings

def read_and_print(receiver, num_parts=1):
    for i in range(num_parts):
        data = next(receiver)

        if isinstance(data, bytes):
            print(data.decode("utf-8"))
        else:
            for part in data:
                print(part.decode('utf-8'))

def wait_and_write(sender, num_parts):
    for i in range(num_parts):
        data = input().encode('utf-8')
        sender(data)

class PubExecutor:
    def __init__(self, socket, num_parts, topic, embed_topic):
        self._sender = socket.pub(topic=topic.encode('utf-8'), embed_topic=embed_topic)
        self._num_parts = num_parts

    def execute(self):
        try:
            wait_and_write(self._sender, self._num_parts)
        except ValueError:
            print("ERROR: The message was not sent, since the topic was not in"
                  " the beginning of the first frame of the message. If you want"
                  " the topic to be automatically sent, set the --embedTopic flag."
                  , file=sys.stderr)

class SubExecutor:
    def __init__(self, socket, num_parts, topics):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self._receiver = socket.sub(topics=[topic.encode('utf-8') for topic in topics])
        self._num_parts = num_parts

    def execute(self):
        read_and_print(self._receiver, self._num_parts)

class PushExecutor:
    def __init__(self, socket, num_parts):
        self._sender = socket.push()
        self._num_parts = num_parts

    def execute(self):
        wait_and_write(self._sender, self._num_parts)

class PullExecutor:
    def __init__(self, socket, num_parts):
        self._receiver = socket.pull()
        self._num_parts = num_parts

    def execute(self):
        read_and_print(self._receiver, self._num_parts)

class ReqExecutor:
    def __init__(self, socket, num_parts):
        self._sender, self._receiver = socket.request()
        self._num_parts = num_parts

    def execute(self):
        wait_and_write(self._sender, self._num_parts)
        read_and_print(self._receiver, self._num_parts)

class RepExecutor:
    def __init__(self, socket, num_parts):
        self._sender, self._receiver = socket.reply()
        self._num_parts = num_parts

    def execute(self):
        read_and_print(self._receiver, self._num_parts)
        wait_and_write(self._sender, self._num_parts)

class ReadOnlyPairExecutor:
    def __init__(self, socket, num_parts):
        _, self._receiver = socket.pair()
        self._num_parts = num_parts

    def execute(self):
        read_and_print(self._receiver, self._num_parts)

class WriteOnlyPairExecutor:
    def __init__(self, socket, num_parts):
        self._sender, _ = socket.pair()
        self._num_parts = num_parts

    def execute(self):
        wait_and_write(self._sender, self._num_parts)