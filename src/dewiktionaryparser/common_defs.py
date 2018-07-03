#!python3
# -*- coding: utf-8 -*-

import re
import json
import pprint
from collections import defaultdict
from prettytable import PrettyTable

###################################
#  Super-class for dictionaries   #
###################################

class WordEntriesDict(dict):
    """A generic dictionary entry"""

    def export_to_json(self, file_path, encoding='utf-8'):
        '''
        For exporting nouns_info dictionary into json file.
        :param file_path: the json file path to which the dictionary should be exported.
        :param encoding: optional string argument specifying the file encoding. Some possible encodings: 'utf-8' (default), 'ISO-8859-1'
        '''
        print('Exporting dictionary to {0} . . .'.format(file_path))
        with open(file_path, 'w', encoding=encoding) as file:
            json.dump(self, file)
        print('Dictionary exported.\n')


    def retrieve_from_json(self, file_path, encoding='utf-8', clear_dict=True):
        '''
        For retrieving previously generated json file contents to populate the dictionary.
        :param file_path: the json file path from which the info should be retrieved.
        :param encoding: optional string argument specifying the file encoding. Some possible encodings: 'utf-8' (default), 'ISO-8859-1'
        :param clear_dict: iff not false, existing entries in self will be deleted before populating self with json information (this is the default choice)
        '''
        if clear_dict:
            self.clear()
        print('Retrieving dictionary from {0} . . .'.format(file_path))
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                self.update(json.load(file))
            print('Retrieved {0} entries.\n'.format(len(self)))
        except FileNotFoundError:
            print('FILE NOT FOUND! {0}\n'.format(file_path))


    def make_inv_dict(self, exclude=list(), include=list()):
        '''Generates and returns an inverse dictionary (whose keys are elements of list-leaves of self, and whose values are word entries from self including that string as an element of its leaves) as a WordEntriesDict entity.
        :param exclude: All branches containing any of the features in the exclude list are disregarded.
        :param include: Only leaves of branches containing at least one feature in the include list (if specified) are collected.'''
        try:
            assert(isinstance(exclude, list))
            assert(isinstance(include, list))
        except AssertionError:
            print('Error: arguments of make_inv_dict must be lists!')
            return
        print('Generating entries for inverse dictionary . . .')
        inv_dict = defaultdict(set)
        for i, w in enumerate(self):
            if (i + 1) % 10000 == 0:
                print('read', i + 1, 'entries')
            for branch in branches(self[w]):
                if include:
                    if all(feat not in branch[:-1] for feat in include):
                        continue
                if all(feat not in branch[:-1] for feat in exclude):
                    if isinstance(branch[-1], list):
                        for leaf_element in branch[-1]:
                            inv_dict[leaf_element].add(w)
                    else:  # note: currently all leaves are lists, but else option kept for potential extensions
                        inv_dict[branch[-1]].add(w)
        print('Read {0} entries altogether.'.format(len(self)))
        for entry in inv_dict:
            inv_dict[entry] = list(inv_dict[entry])
        print('Generated {0} new entries for inverse search.\n'.format(len(inv_dict)))
        return WordEntriesDict(inv_dict)


    def enhance_usages(self, second_dic: dict):
        '''Adds information from second_dic under the relevant usages of self word entries, and returns the list of entry-usage pairs not in second_dic.
        '''
        # not_in_second_dic = []
        for n in self.keys():
            for u in self[n].keys():
                try:
                    self[n][u].update(second_dic[n][u])
                except KeyError:
                    # not_in_second_dic.append((n, u))
                    continue
                except Exception as ex:
                    print(str(ex), n, u)
                    continue
        # return not_in_second_dic


    def printsorted(self, m=0, n=10):
        '''Print information from the alphabetically sorted dictionary from between indexes m and n.'''
        sorted_entries = sorted(self)

        for word in sorted_entries[m:n]:
            print(word), pprint.pprint(self[word])


    def word_entry(self, entry: str):
        '''Pretty print information about word entry.'''
        if not entry in self:
            print("'{0}' is not in dictionary.".format(entry))
            return
        pprint.pprint(self[entry])


    def tabulate_entry(self, noun: str, verbose=False):
           ''' Displays a word entry in a tabulated form. Not to be used with inverse dictionaries. Requires the prettytable or the PTable package. The switch 'verbose' affects the details displayed (default: False). '''
           try:
               branchlist = branches(self[noun])
               if isinstance(self[noun], list):
                   print('\n {0} |--> {1}'.format(noun, ', '.join(sorted(self[noun]))))
                   return
               elif any(feat in br for br in branchlist for feat in ['deg_of_comp', 'spec_comp', 'decl_feat', 'attr_pred']):
                   self.word_entry(noun)
                   return
           except KeyError:
               print("'{0}' is not in dictionary.".format(noun))
               return
           table = PrettyTable()
           table.title = noun  # Works only if the package PTable is installed
           table.field_names = ["Usage", "SpecFeat", "Gen/Case/Lang", "Num/Lex", "Decl", "Value"]
           usage_flag = False
           specfeat_flag = False
           # table.align["Genus/Case"] = "l"
           # table.align["Num"] = "l"
           emptyrow = ["", "", "", "", "", ""]
           usages = partition_branches(branchlist)
           for usage in usages:
               table.add_row(emptyrow)
               for decl in usage:
                   for row in decl:
                       row[0] = row[0][1]
                       if row[0] != '1':
                           usage_flag = True
                       if row[1] == 'gen_case_num':
                           row[1] = ''
                       if row[1]:
                           specfeat_flag = True
                       if not row[-1]:
                           row[-1] = ['-']
                       row[-1] = ', '.join(row[-1])
                       table.add_row(row)
                   table.add_row(emptyrow)
           if verbose:
               print(table)
           elif usage_flag and specfeat_flag:
               print(table.get_string(fields=["Usage", "SpecFeat", "Gen/Case/Lang", "Num/Lex", "Value"]))
           elif usage_flag:
               print(table.get_string(fields=["Usage", "Gen/Case/Lang", "Num/Lex", "Value"]))
           elif specfeat_flag:
               print(table.get_string(fields=["SpecFeat", "Gen/Case/Lang", "Num/Lex", "Value"]))
           else:
               print(table.get_string(fields=["Gen/Case/Lang", "Num/Lex", "Value"]))



############################################
#  Dictionary manipulation functions       #
############################################

def get_by_keypath(dic:dict, keypath:list):
    for key in keypath:
        dic = dic[key]
    return dic


def set_by_keypath(dic:dict, keypath:list, val):
    for key in keypath[:-1]:
        dic = dic.setdefault(key, {})
    dic[keypath[-1]] = val


def twig_collector(dic:dict) -> list:
    ''' Collects the twigs in a dictionary. '''
    twigs = []
    if not isinstance(dic, dict):
        return [dic]
    else:
        for val in dic.values():
            twigs.extend(twig_collector(val))
    return twigs


def nextlevel_keys(dic:dict, keypath:list):
    try:
        return get_by_keypath(dic, keypath).keys()
    except AttributeError:
        return None


def branches(tree:dict, keypath=list()) -> list:
    '''Unpacks a dictionary into a flat list of its branches '''
    branches_list = []
    if nextlevel_keys(tree, keypath) == None:
        return [[get_by_keypath(tree,keypath)]]
    else:
        for k in nextlevel_keys(tree, keypath):
            kth_br_list = []
            for sub_tree_br_list in branches(tree, keypath + [k]):
                kth_br_list.append([k] + sub_tree_br_list)
            for br in kth_br_list:
                branches_list.append(br)
    return branches_list

def partition_branches(branchlist):
    branchlist = preproc(branchlist)
    usages = sorted([[li for li in branchlist if li[0] == u] for u in {li[0] for li in branchlist}], key=lambda x: ordering0.index(x[0][0]))
    partition = []
    for use in usages:
        same_decls = [[li for li in use if li[-2] == d] for d in {us[-2] for us in use}]
        same_decls_sorted = sorted(same_decls, key=lambda x: ordering4.index(x[0][-2]))
        partition.append(same_decls_sorted)
    return partition

def preproc(branchlist):
    new_brl = []
    for li in branchlist:
        new_li = li[:]
        for i, el in enumerate(li):
            if el == 'translations':
                new_li[i + 3:i + 3] = [' ']
            if el == 'genus':
               new_li[i+1:i+1] = ['']
            if el == 'spec_word_type':
                new_li[i+1:i+1] = ['', '', '']
            if el == 'tantum':
                new_li[i+1:i+1] = ['', '', '']
        new_brl.append(new_li)
    return new_brl


ordering0 = ['u1', 'u2', 'u3', 'u4', 'u5', 'u6']
ordering4 = ['sg1', 'sg2', 'sg3', 'sg4', 'pl1', 'pl2', 'pl3', 'pl4', '', ' ']


############################################
#  String manipulation before parsing      #
############################################

# https://de.wiktionary.org/wiki/Hilfe:Namensräume
# Pages will be ignored if title begins with:
namensraum_simple = r"(Spezial|Medium|Diskussion|Vorlage|Verzeichnis|Thesaurus|Reim|Flexion|Hilfe|Kategorie|Benutzer|Gadget|Gadget-Definition|Wiktionary|Datei|MediaWiki|Modul|Benutzerin|BD|WT|Bild|Image|WikiSaurus)"
colon = r"\:"
diskussion_colon = r" Diskussion:"

''' strings to remove from xml to clean it before parsing: '''

html_comment_string = r"(<|&lt;)!--(.(?!--(>|&gt;)))+.--(>|&gt;)"
wiki_comment_string = r"<comment(.(?!</comment>))+.</comment>"
nowiki_string =  r"(<|&lt;)nowiki(>|&gt;)(.(?!(<|&lt;)nowiki(>|&gt;)))+.(<|&lt;)nowiki(>|&gt;)"
html_tag_string =  r"(<|\&lt;)(small|sup|ref)(.(?!\1/\2))*.?\1\/\2(>|\&gt;)" # \2 is the second group, e.g., small, sup, ref
html_tag_string_onetag =  r"(<|\&lt;)(small|sup|ref)(.(?!(>|\&gt;)))*.?(>|\&gt;)" # e.g., "{{Ü|en|observation}}<ref name="law_d" />,"
unicode_char_to_del = u'(\u00AE|\u200e)'

'''could also be included in to_del_strings:'''

html_break = r"(<|\&lt;)br\s*/*(>|\&gt;)"
angle_quoted_string = r"\(?\u00bb[^\u00ab]+\u00ab\)?"  # stuff between angle quotation marks usually comments, but these are not deleted for now.
quoted_string = r"\(?„[^“]+“\)?"


'''list of all strings to delete:'''

to_del_strings = [html_comment_string, wiki_comment_string, nowiki_string, html_tag_string, html_tag_string_onetag, unicode_char_to_del]


'''strings to replace:'''
wiki_link_string = r'\[\[([^\|\]]+\|)?([^\]]+)\]\]'  ## delete all hyperlink indicators: string = re.sub(wiki_link_string, r'\2', string)
specstring = r"\&(amp)?;nbsp;" # e.g., "nothing&nbsp;of&nbsp;", replace as space: string = re.sub(specstring, ' ', string)
quote_html = r'&quot;'  # replace as ": string = re.sub(quote_html, '"', string)
amp_html = r'&amp;'  # replace as ": string = re.sub(amp_html, '&', string)

def clean_up_string(string:str):
    string = re.sub(wiki_link_string, r'\2', string)
    string = re.sub(specstring, ' ', string)
    string = re.sub(quote_html, '"', string)
    string = re.sub(amp_html, '&', string)
    for to_del_string in to_del_strings:
        string = re.sub(to_del_string, '', string)
    return string


########################
# Major-level regexes  #
########################

de_headword_regex = re.compile(r"([^=]|^|\n)== (\w\S+) \(\{\{Sprache\|Deutsch")  # headword is .group(2)
de_headword_spaces_allowed_regex = re.compile(r"([^=]|^|\n)== (\w(.(?!\(\{\{Sprache\|))+) \(\{\{Sprache\|Deutsch")  # headword is .group(2)
new_heading_two_regex = re.compile(r"([^=]|^|\n)== (\w\S+) \(\{\{Sprache\|(?P<lang>\w+)")
new_heading_two_spaces_allowed_regex = re.compile(r"([^=]|^|\n)== (\w(.(?!\(\{\{Sprache\|))+) \(\{\{Sprache\|(?P<lang>\w+)")
new_usage_pattern = re.compile(r"""=== {{Wortart\|([^\|]+)\|Deutsch}}""", re.U)  # A 3rd-level heading specifying word type (Wortart) and German (Deutsch) as the language
# Ex.: "=== {{Wortart|Substantiv|Deutsch}}, {{f}} ==="
### for finding information in the new usage (===) line:
new_usage_line = re.compile(r"""[^\n]*[^=]?===\s{{Wortart\|[^\|]+\|Deutsch}}[^\n]+""", re.M | re.U)

title_pattern = re.compile(r"<title>(?P<pagetitle>(.(?!</title>))+.)</title>")
text_begin_pattern = re.compile(r"<text")
text_end_pattern = re.compile(r"</text>")


###################################
##   POS-specific definitions    ##
###################################

de_noun_regex = re.compile(r"([^=]|^|\n)=== \{\{Wortart\|(Substantiv|Abkürzung|Toponym|Nachname|Vorname|Eigenname|Name|Buchstabe|Zahlklassifikator|Straßenname)\|Deutsch\}\}")
de_adj_regex = re.compile(r"([^=]|^|\n)=== \{\{Wortart\|Adjektiv\|Deutsch\}\}")


########################################
##  Translation-specific definitions  ##
########################################

''' Translations-specific delete list  '''

empty_entrans_tag = r"\{\{Ü\|en\}\}"  # e.g., in 'Windschutzscheibenwaschanlage'
wiki_tag_string = r"\(?\{\{[^Ü][^\}]*\}\}\)?"  # delete all non-translation tags, e.g., {{amer.}}
wiki_italics_string = r"\(?''[^']+''\)?\s*"
to_del_char_from_ubersetzung_tag = r"(\{\{Ü\|en\|[^\}]*),([^\}]*\}\})"  # to remove comma replace with \1\2 (e.g., "{{Ü|en|atomic absorption spectrometry, en|atomic absorption spectroscopy}}")
to_del_strings_transl = [wiki_italics_string, wiki_tag_string, empty_entrans_tag, angle_quoted_string, quoted_string] # note: order might matter (e.g, wiki_italics string before wiki_tag_string)


''' Patterns and variables used to get translations '''

transl_en_line_regex = re.compile(r"^\*\{\{en\}\}\:(.(?!\*+\{\{))+.", re.U | re.M)
#    .group(0) = line with all English translations

transl_lexeme_and_transl_regex = re.compile(r"\[(\d+[^\]]*)\]((.(?!\[\d))+.)", re.M)
#   .group(1) = lexeme numbers specification, e.g., 1 or 1-4, or 1, 3
#   .group(2) = all translations belonging to the lexeme(s)

transl_lex_range_regex = re.compile(r"(\d+)[-–](\d+)")
transl_lexes_from_lexeme_and_transl_regex = re.compile(r"(\d+)")
transl_en_regex = re.compile(r"""
    (?P<pretransl>[^\{\|\}]*)           # perhaps some stuff before {{Ü|en... belonging to translation (e.g., "[[play]] {{Ü|en|catch}}")               
    \{\{Ü(t)?\|en(\|[^\}\|]+)?      # {{Ü|en or {{Üt|en indicates English translation; we need the first bunch after en, or the second, if there are multiple attributes inside {{Ü|en|...|....}}
    \|(?P<transl>[^\}\|]+)
    (\|[^\}\|]+)*\}\}                 # zero or more extra group after the translation group
    (?P<posttransl>[^,;\{]*)    # potential post-translation stuff, currently not added.
    """, re.X)
