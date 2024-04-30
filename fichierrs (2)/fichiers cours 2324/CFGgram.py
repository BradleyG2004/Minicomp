# -*- coding: utf-8 -*-


from collections import defaultdict
import random 

class CFG(object):
    def __init__(self):
        self.prod = defaultdict(list)

    def add_prod(self, lhs, rhs):
        """ Add production to the grammar. 'rhs' can
            be several productions separated by '|'.
            Each production is a sequence of symbols
            separated by whitespace.

            Usage:
                grammar.add_prod('NT', 'VP PP')
                grammar.add_prod('Digit', '1|2|3|4')
        """
        prods = rhs.split('|')
        for prod in prods:
            self.prod[lhs].append(tuple(prod.split()))

    def gen_random(self, symbol):
        """ Generate a random sentence from the
            grammar, starting with the given
            symbol.
        """
        sentence = ''

        # select one production of this symbol randomly
        rand_prod = random.choice(self.prod[symbol])

        for sym in rand_prod:
            # for non-terminals, recurse
            if sym in self.prod:
                sentence += self.gen_random(sym)
            else:
                sentence += sym + ' '

        return sentence
        

cfg1 = CFG()
cfg1.add_prod('S', 'GN GN GN ')
cfg1.add_prod('P', 'GN GV | GN GV CCM| CCT GN GV| GN GV PropSub')
cfg1.add_prod('CCM', 'doucement | comme s il n y avait pas de lendemain')
cfg1.add_prod('GN', 'Pronom | det N')
cfg1.add_prod('Pronom', 'Je|Il|Elle|Joe')
cfg1.add_prod('GV', 'V COD')
cfg1.add_prod('CCT', 'pendant 2 ans| ce matin | Ce n etait pas encore l aube quand|apres un mauvais hivers')
cfg1.add_prod('PropSub', 'qui déceda aussitot')
cfg1.add_prod('COD', 'det N')
cfg1.add_prod('det', 'un|le|mon|son')
cfg1.add_prod('N', 'mamouth | chat | citoyen | pantalon')
cfg1.add_prod('V', 'mangea | reconnu | acheta|chicota')

print(cfg1.gen_random('S'))