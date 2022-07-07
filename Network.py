class Network:
    def __init__(self):
        self.queue = []
        self.computers = None

    def add_message_to_queue(self, message):
        self.queue.append(message)

    def extract_message(self):
        for message in self.queue:
            if self.computers[message.src].failed is False and self.computers[message.dst].failed is False:
                self.queue.remove(message)
                return message
        return None
