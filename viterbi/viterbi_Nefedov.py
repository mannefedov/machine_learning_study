"""пока нет оценки качества"""
from collections import Counter


class HMM():
    def states(self):
        states = set()
        for i in self.corpus:
            for s in i:
                states.add(s[2])
        self.states = states
    

    def get_probs(self):
        transitions = Counter()
        emissions = Counter()
        initial = Counter(['__BOS__'])
        tag = '__BOS__'
        s = ['__BOS__'] + list(self.states) + ['__EOS__']
        pairs = []
        for x in s:
            for y in s:
                pairs.append((x, y))
        pairs = {x: 0 for x in pairs}
        for sent in self.corpus:
            for word in sent:
                token, pos = word[0].lower(), word[2]
                initial.update([pos])
                emissions.update([(pos, token)])
                transitions.update([(tag, pos)])
                tag = pos
            transitions.update([(tag, '__EOS__')])
            tag = '__BOS__'
            initial.update([tag])
        # transitions_p = {}
        emissions_p = {}
        for c in transitions:
            try:
                pairs[c] = transitions[c]/initial[c[0]]
            except Exception as e:
                print(c, e)  
        for c in emissions:
            try:
                emissions_p[c] = emissions[c]/initial[c[0]] 
            except Exception as e:
                print(c, e)


        self.trans = pairs
        self.emission = emissions_p

    def read_corpus(self):
        sent = []
        stack = []
        with open('ruscorpora.parsed.txt', encoding='utf-8') as corpus:
            corpus = [line.strip('\n') for line in corpus if not line.startswith('#')]
            corpus = [line.split('\t')[0] for line in corpus]
            for line in corpus:
                if not line:
                    sent.append(stack)
                    stack = []
                    continue
                line = line.split('=')[0]
                line = line.split('/')
                if len(line) == 3:
                    word, lemma, pos = line
                else:
                    word = ''.join(line[:2])
                    lemma = line[2]
                    pos = line[3]
                stack.append((word, lemma, pos.split(',')[0]))
        self.corpus = sent

def viterbi(obs, states, transition, emission):
    V = [{}]
    for i in states:
        V[0][i] = transition[('__BOS__', i)]*emission.get((i,obs[0]),0)
    for t in range(1, len(obs)):
        V.append({})
        for y in states:
            prob = max(V[t-1][ys]*transition[(ys, y)]*emission.get((y, obs[t]), 0) for ys in states)
            V[t][y] = prob
    opt = []
    for j in V:
        for x,y in j.items():
            if j[x] == max(j.values()):
                opt.append(x)
    h = max(V[-1].values())
    return ' '.join(opt), h

if __name__ == '__main__':
    h = HMM()
    h.read_corpus()
    h.states()
    h.get_probs()
    print(viterbi('сегодня в москве был дождь'.split(' '), h.states, h.trans, h.emission))
    