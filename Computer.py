import Message

class PaxosComputer:
    def __init__(self, network, acceptors=None):
        self.network = network
        self.acceptors = acceptors
        self.failed = False
        self.changed = False
        self.prior = False
        self.consensus = False
        self.promise_count = 0
        self.accepted_proposals = 0
        self.rejected_proposals = 0
        self.maxID = 0
        self.value = None
        self.initial_value = None
        self.proposal = 0



    def deliver_message(self, message, proposal):
        '''Delivers messages between paxos computers'''
        self.proposal = proposal

        def process_message(type, src, dst, value):
            '''Process a message given a type, src, dst and value'''
            m = Message.Message()
            m.type = type
            m.src = src
            m.dst = dst
            m.value = value
            m.proposalID = proposal
            self.network.add_message_to_queue(m)
        match message.type:
            case 'PROPOSE':
                self.proposal += 1
                self.initial_value = message.value
                self.value = message.value
                for acceptor in self.acceptors:
                    process_message('PREPARE', message.dst, acceptor, message.value)

            case 'PREPARE':
                prepare_value = self.value if self.prior else message.value
                process_message('PROMISE', message.dst, message.src, prepare_value)

            case 'PROMISE':
                self.promise_count += 1
                if self.value != message.value and not self.changed:
                    self.value = message.value
                    self.changed = True
                if self.promise_count == len(self.acceptors):
                    for acceptor in self.acceptors:
                        process_message('ACCEPT', message.dst, acceptor, self.value)

            case 'ACCEPT':
                if self.prior:
                    if message.proposalID < self.maxID:
                        process_message('REJECTED', message.dst, message.src, message.value)
                    else:
                        self.maxID = message.proposalID
                        self.value = message.value
                        process_message('ACCEPTED', message.dst, message.src, message.value)
                else:
                    self.prior = True
                    self.maxID = message.proposalID
                    self.value = message.value
                    process_message('ACCEPTED', message.dst, message.src, message.value)

            case ('ACCEPTED' | 'REJECTED'):
                if message.type == 'ACCEPTED':
                    self.accepted_proposals += 1
                if message.type == 'REJECTED':
                    self.rejected_proposals += 1

                if self.accepted_proposals + self.rejected_proposals == len(self.acceptors):
                    if self.accepted_proposals > self.rejected_proposals: #als er meer geaccepteerde voorstellen zijn
                        self.changed = False
                        self.consensus = True  # dan is er consensus en resetten de values
                        self.accepted_proposals = 0
                        self.rejected_proposals = 0
                        self.promise_count = 0

                    else: #anders, prepare nieuwe messages
                        self.changed = False
                        self.accepted_proposals = 0
                        self.rejected_proposals = 0
                        self.promise_count = 0
                        self.value = message.value
                        self.proposal+=1
                        #prepare
                        for acceptor in self.acceptors:
                            process_message('PREPARE', message.dst, acceptor, message.value)

