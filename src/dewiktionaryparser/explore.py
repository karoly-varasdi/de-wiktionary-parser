#!python3
# -*- coding: utf-8 -*-

from .common_defs import *


def bigcap(lis:list) -> set:
    return lis[0].intersection(*lis[1:])


#################################################
# Functions for exploring the dictionary        #
#################################################


def leaves_under_keyword(worddic:dict, keyword:str) -> set:
    '''Collects all the leaves under an arbitrary keyword in a dictionary, for example,
    leaves_under_keyword(word_entries, 'genus') collects every possible value that occurs under the genus keyword in word_entries.'''
    return {leaf for leaves in get_leaves_by_key(worddic, keyword) for leaf in leaves}


def get_leaves_by_key(dic:dict, key) -> list:
    ''' Returns a list containing the list of leaves that are under the occurrences of key in dic '''
    leaves = []
    if not isinstance(dic, dict):
        return leaves
    for k in dic:
        if k == key:
            leaves.extend(leaf_collector(dic[k]))
        else:
            leaves.extend(get_leaves_by_key(dic[k], key))
    return leaves

def find_by_path_fragment(dic:dict, keys:list) -> set:
    '''Accepts a dictionary and an arbitrary list of keywords (not necessarily existing in the dictionary). Returns the set of all the leaves in the dictionary that are under all the keys in the keylist (the empty set if a non-existent key has been used). For example, find_by_path_fragment(word_entries['Tee'], ['u2', 'akkusativ']) returns the akkusativ forms under usage 2 of the word Tee; and find_by_path_fragment(word_entries, ['nominativ', 'plural']) returns every nominativ plural form in word_entries.'''
    return bigcap([leaves_under_keyword(dic, k) for k in keys])

def find_entries_by_keyword_value(worddic:dict, **aspect) -> set:
    '''Returns the set of entry keys in worddic with a given keyword (aspect) and its value specified if the entry has at least one occurence of the value in the leaves under the keyword. For example, find_entries_by_keyword_value(word_entries, spec_word_type='Toponym') collects all toponym entries in word_entries.'''
    entry_sets_list = []
    for keyword, kwvalue in aspect.items():
        entry_sets_list.append({word for word in worddic for leaf_list in get_leaves_by_key(worddic[word], keyword) for leaf in leaf_list if kwvalue in leaf})
    return bigcap(entry_sets_list)


def filter_usages_by_keywords(source_dict: WordEntriesDict, include_list:list, exclude_list:list) -> WordEntriesDict:
    '''Returns a WordEntriesDict that contains entries of source_dict that only include the usages that have all the keys in include_list but none in exclude_list, e.g., filter_usages_by_keywords(word_entries, ['plural'], ['singular', 'tantum']) returns a dictionary in the entries of which all the usages have a plural feature but no singular or tantum. '''
    target_dict = WordEntriesDict()
    for k in source_dict:
        target_dict[k] = WordEntriesDict()
        for u in source_dict[k]:
            if all(get_leaves_by_key(source_dict[k][u], incl) for incl in include_list) and not any(get_leaves_by_key(source_dict[k][u], excl) for excl in exclude_list):
                target_dict[k][u] = source_dict[k][u]
            else:
                continue
        if target_dict[k]:
            continue
        else:
            del target_dict[k]
    return target_dict


def collect_values(dic:dict, keypath:list) -> (dict, dict):
    '''Collects the values in a dictionary under keypath (vals); collects the errors thrown when the keypath is not defined (exceps). For example, tword_entries, ['u1']) returns the words that have a 'u1' key as well as those that do not, separated in the output as vals, exceps.'''
    vals, exceps = {}, {}
    for w in dic:
        try:
            vals.update({w:get_by_keypath(dic[w], keypath)})
        except Exception as ex:
            exceps.update({w: (type(ex).__name__, ex.args)})
            continue
    return vals, exceps
