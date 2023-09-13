"""Knuth-Morris-Pratt finds the 1st occurrence of a pattern in a text string wo/backing-up."""
# pylint: disable=invalid-name

from collections import defaultdict


def search(pat, txt):
    """Knuth-Morris-Pratt finds the 1st occurrence of a pattern in a text string wo/backing-up."""
    kmp = KMP(pat)
    return kmp.search(txt)


class KMP: # O ~ txtlen + patlen * alphabet-size (wc)
    """finds the first occurrence of a pattern string in a text string."""

    def __init__(self, pat):
        """Preprocesses the pat string."""
        self._pat = list(pat)
        self._len_pat = len(self._pat)
        self._dfa = self._init_dfa()

    def _init_dfa(self):
        """Build DFA (Deterministic finite state automatom) from pat"""
        dfa = defaultdict(lambda: [0 for i in range(self._len_pat)])
        dfa[self._pat[0]][0] = 1
        state_id = 0
        for pat_j, letter in enumerate(self._pat[1:], 1):
            for key in dfa.keys():
                dfa[key][pat_j] = dfa[key][state_id]  # Copy mismatch cases.
            dfa[letter][pat_j] = pat_j+1  # Set match case.
            state_id = dfa[letter][state_id]  # Update restart state.
        return dfa

    def search(self, txt):
        """Returns the idx of the 1st occurrrence of the pattern string in the text string."""
        # simulate operation of DFA on text
        dfa = self._dfa
        len_pat = self._len_pat
        pat_j = 0

        # Using a for-loop in Python is faster and emphasizes that there is no backup
        for txt_i, txt_chr in enumerate(txt):
            pat_j = dfa[txt_chr][pat_j] if txt_chr in dfa else 0 # <----- no backup
            # Found the pattern: leave text loop
            if pat_j == len_pat:
                break
        if pat_j == len_pat:
            return txt_i - len_pat + 1 # found substring

        return -1                   # not found, originally return text size(len_txt)

    def prt_dfa(self, prt):
        """Print DFA (Deterministic finite state automatom) from pat."""
        prt.write("     {}\n".format(' '.join(self._pat)))
        # pylint: disable=line-too-long
        prt.write("     {} <- Current State\n".format(' '.join(str(i) for i in range(self._len_pat))))
        for pat_letter, state_nxt in sorted(self._dfa.items()):
            prt.write("{} -> {}\n".format(pat_letter, ' '.join(str(s) for s in state_nxt)))


# Copyright 2002-2016, Robert Sedgewick and Kevin Wayne.
# Copyright 2015-present, DV Klopfenstein, PhD, Python implementation.
