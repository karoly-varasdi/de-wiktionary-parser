#!python3
# -*- coding: utf-8 -*-

from .common_defs import *
import webbrowser
import ujson


def bigcap(sets_list:list) -> set:
    return sets_list[0].intersection(*sets_list[1:])


#################################################
# Functions for exploring the dictionary        #
#################################################


def twigs_list_by_key(dic:dict, key) -> list:
    ''' Returns a list containing the twigs (lists of leaves) that are under the occurrences of key in dic '''
    twigs = []
    if not isinstance(dic, dict):
        return twigs
    for k in dic:
        if k == key:
            twigs.extend(twig_collector(dic[k]))
        else:
            twigs.extend(twigs_list_by_key(dic[k], key))
    return sorted(twigs)


def leaves_by_key(worddic:dict, key:str) -> list:
    '''Collects all the leaves under an arbitrary keyword in a dictionary, for example,
    leaves_by_key(word_entries, 'genus') collects every possible value that occurs under the genus keyword in word_entries.'''
    return sorted({leaf for leaves in twigs_list_by_key(worddic, key) for leaf in leaves})


def leaves_by_path_fragment(dic:dict, key_list:list, per_usage=False) -> list:
    '''Accepts a dictionary and an arbitrary list of keywords (not necessarily existing in the dictionary). Returns the set of all the leaves in the dictionary that are under all the keys in the keylist (the empty set if a non-existent key has been used). For example, leaves_by_path_fragment(word_entries['Tee'], ['u2', 'akkusativ']) returns the akkusativ forms under usage 2 of the word Tee; and leaves_by_path_fragment(word_entries, ['nominativ', 'plural']) returns every nominativ plural form in word_entries.'''
    twigs_list = [br[-1] for w in dic for br in branches(dic[w]) if all(k in br for k in key_list)]
    if per_usage:
        return twigs_list
    else:
        return sorted(set(e for li in twigs_list for e in li))


def forms(word:str, feats:str, dic:dict, per_usage = False) -> list:
    '''Returns a list of leaves (separated by usage if per_usage = True). For example, forms('Hahn', 'singular genitiv', commons) returns all the inflected singular genitive forms of the word Hahn in the dictionary named commons.'''
    return leaves_by_path_fragment(dic[word], feats.split(), per_usage)


def genders(word:str, dic:dict, per_usage = False) -> list:
    return forms(word, 'genus' ,dic, per_usage)


def english_trs(word:str, dic:dict, per_usage = False) -> list:
    return forms(word, 'translations en', dic, per_usage)


def no_of_usages(word:str, dic:dict) -> int:
    return len(dic[word])


def headwords_by_key_value_pairs(worddic:dict, *key_value:tuple, by_usage=True) -> list:
    '''Returns a list of entry keys (headwords) in worddic with a given key k and its value v specified
    a) if the entry has a usage that has at least one occurrence of the value v in the twigs under the key k for all k,v pairs specified (when by_usage=True, default case), or
    b) the entry has at least one occurrence of the value v in the twigs under the key k (when by_usage=False).
    For example, headwords_by_key_value_pair(word_entries, ('genus', 'n'), ('genus', 'm')) lists all headwords in worddic that have at least one usage that can be both a neuter and a masculine.
    By contrast, headwords_by_key_value_pair(word_entries, ('genus', 'n'), ('genus', 'm'), by_usage=False) lists all headwords in worddic that have both a neuter and a masculine use.'''
    headwords = set()
    for kv_pair in key_value:
        try:
            assert len(kv_pair) == 2
        except AssertionError:
            print("No result generated, due to incorrect argument '{}'.\nIt should be a list or tuple of length 2 of the form (key, value).".format(kv_pair))
            return False
    for w in worddic:
        if by_usage:
            for u in worddic[w]:
                if all(val in leaves_by_key(worddic[w][u], key) for key, val in key_value):
                    headwords.add(w)
        else:
            if all(val in leaves_by_key(worddic[w], key) for key, val in key_value):
                    headwords.add(w)
    return sorted(headwords)

def filter_entry_usages_by_keylists(source_dict: WordEntriesDict, include_list:list, exclude_list:list) -> WordEntriesDict:
    '''Returns a WordEntriesDict that contains entries of source_dict that only include the usages that have all the keys in include_list but none in exclude_list, e.g., filter_entry_usages_by_keylists(word_entries, ['plural'], ['singular', 'tantum']) returns a dictionary in the entries of which all the usages have a plural feature but no singular or tantum. '''
    target_dict = WordEntriesDict()
    for k in source_dict:
        target_dict[k] = WordEntriesDict()
        for u in source_dict[k]:
            if all(twigs_list_by_key(source_dict[k][u], incl) for incl in include_list) and not any(twigs_list_by_key(source_dict[k][u], excl) for excl in exclude_list):
                target_dict[k][u] = ujson.loads(ujson.dumps(source_dict[k][u]))
            else:
                continue
        if target_dict[k]:
            continue
        else:
            del target_dict[k]
    return target_dict


def subdic_by_headwords(dic:WordEntriesDict, headwords:list) -> WordEntriesDict:
    '''Given a list of headwords from dic, it returns the corresponding subdictionary of dic.'''
    subdic = WordEntriesDict()
    for hw in headwords:
        try:
            subdic[hw] = ujson.loads(ujson.dumps(dic[hw]))
        except KeyError:
            continue
    return subdic



def wiki(word:str):
    '''Accepts a word form and opens the respective wiktionary page.'''
    if not type(word) is str:
        print('The argument must be a string!')
        return
    else:
        webbrowser.open('https://de.wiktionary.org/wiki/' + word)



def charting_dictionary_space(dic:dict):
    entries = list(iter(dic.values()))
    chart = {}
    for new_key in sorted(keyrange(entries, [])):
        chart[new_key] = '[...]'
    gen_the_rest(entries, chart)
    return chart

def gen_the_rest(dic, chart):
    old_chart = ujson.loads(ujson.dumps(chart))
    for br in branches(chart):
        telescope = {}
        for new_key in sorted(keyrange(dic, br[:-1])):
            telescope.update({new_key:'[...]'})
            set_by_keypath(chart, br[:-1], telescope)
    if old_chart == chart:
        return
    else:
        return gen_the_rest(dic, chart)

def keyrange(dic_list, keypath):
    occurring_keys = set()
    for dic in dic_list:
        try:
            occurring_keys.update(list(get_by_keypath(dic, keypath).keys()))
        except(KeyError, AttributeError):
            continue
    return occurring_keys

