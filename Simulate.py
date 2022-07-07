from Network import Network
from Computer import PaxosComputer
from Message import Message

def Simulate(n_p, n_a, tmax, E):
    N = Network()
    A = {f'A{i+1}':PaxosComputer(N) for i in range(n_a)}
    P = {f'P{i+1}':PaxosComputer(N, A.keys()) for i in range(n_p)}
    C = {**P, **A}
    N.computers = C
    proposal = 0

    for t in range(0, tmax):
        tfill = str(t).zfill(3) #represent the ticks in string format so it matches required output

        if len(N.queue) == 0 and len(E) == 0:
            #Since there are no message or events, the simulation will end here.
            for key in P.keys():
                if P[key].consensus:
                    print(f'{key} heeft wel consensus (voorgesteld: {P[key].initial_value}, geaccepteerd: {P[key].value})')
                else:
                    print(f'{key} heeft geen consensus.')
            return

        #Verweerk event e (als dat tenminste bestaat)
        e = [i for i in E if i[0] == t]
        e = None if e == [] else e[0]
        if e is not None:
            E.remove(e)
            (t, F, R, pi_c, pi_v) = e

            for c in F:
                print(f'{tfill}: ** {c} kapot **')
                C[c].failed = True

            for c in R:
                print(f'{tfill}: ** {c} gerepareerd **')
                C[c].failed = False

            if pi_v is not None and pi_c is not None:
                m = Message()
                m.type = 'PROPOSE'
                m.src = None
                m.dst = pi_c
                m.value = pi_v
                print(f'{tfill}:    -> {m.dst}  PROPOSE v={m.value}')
                proposal += 1
                C[pi_c].deliver_message(m, proposal)

        else:
            m = N.extract_message()
            if m is not None:
                match m.type:
                    case 'PREPARE':
                        print(f'{tfill}: {m.src} -> {m.dst}  PREPARE n={m.proposalID}')
                        C[m.dst].deliver_message(m, proposal)

                    case 'PROMISE':
                        if C[m.src].prior:
                            print(f'{tfill}: {m.src} -> {m.dst}  PROMISE n={m.proposalID} (Prior: n={C[m.src].maxID}, v={C[m.src].value})')
                        else:
                            print(f'{tfill}: {m.src} -> {m.dst}  PROMISE n={m.proposalID} (Prior: None)')
                        C[m.dst].deliver_message(m, proposal)

                    case 'ACCEPT':
                        print(f'{tfill}: {m.src} -> {m.dst}   ACCEPT n={m.proposalID} v={m.value}')
                        C[m.dst].deliver_message(m, proposal)

                    case 'ACCEPTED':
                        print(f'{tfill}: {m.src} -> {m.dst}   ACCEPTED n={m.proposalID} v={m.value}')
                        C[m.dst].deliver_message(m, proposal)

                    case 'REJECTED':
                        print(f'{tfill}: {m.src} -> {m.dst}   REJECTED n={m.proposalID} v={m.value}')
                        C[m.dst].deliver_message(m, proposal)
                        proposal = C[m.dst].proposal
            else:
                print(f'{tfill}: ')
