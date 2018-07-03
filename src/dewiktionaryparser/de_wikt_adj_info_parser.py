#!python3
# -*- coding: utf-8 -*-

from .common_defs import *
import ujson


class GermanAdjEntriesDict(WordEntriesDict):
    """Dictionary for storing morphological information about German nouns from the German wiktionary."""

    def make_inv_dict(self, exclude=list(), include=list({'positiv', 'komparativ', 'superlativ'})):
        '''Returns an inverse dictionary containing by default degrees of comparison forms as keys.'''
        inv_dict = super().make_inv_dict(exclude=exclude, include=include)
        return WordEntriesDict(inv_dict)

    ############################################
    #    Methods for parsing wiktionary xml.   #
    ############################################

    def full_info(self, decl_table: str):
        '''Returns a list of ('MORPH_pattern_regex', [('STARRED', 'VALUE'), ]) tuples for morphological pattern regexes in the regexes dictionary.'''
        return [(reg, re.findall(regexes_adj_dic[reg], decl_table)) for reg in regexes_adj_dic]

    def parse_decl_table(self, decl_table):
        '''Parses a declension table (a multi-line string) and returns a dictionary of grammatical information ready for inclusion as value of the usage number key.'''
        wd = {}
        info = self.full_info(decl_table)
        to_add_starred = ()  # (keyseq, str) tuple for starred versions appearing before non-starred versions

        for pair in info:
            morphs_list = keymaps_adj[pair[0]]  # e.g., ['komparativ']
            list_of_tuples = pair[1]  # (*, value)
            for tupl in list_of_tuples:
                try:
                    if 'am' in morphs_list and (tupl[1] == 'nein' or tupl[1] == '0'):
                        value_to_add = ['no_am']
                    elif 'keine_weiteren_formen' in morphs_list and (tupl[1] == 'ja' or tupl[1] == '1'):
                        value_to_add = ['no_other_forms']
                    else:
                        value_to_add = [tupl[1]]
                except IndexError:
                    continue

                ## setting the path as a keyseq list where value is to be entered:
                if morphs_list == ['am'] or morphs_list == ['keine_weiteren_formen']:
                    keyseq = ['spec_comp']
                else:
                    keyseq = ['deg_of_comp'] + morphs_list
                try:
                    if tupl[0]:
                        if get_by_keypath(wd, keyseq):
                            to_add = get_by_keypath(wd, keyseq) + value_to_add
                    else:
                        if not to_add_starred:
                            to_add = value_to_add
                        else:
                            if keyseq == to_add_starred[0]:
                                to_add = value_to_add + to_add_starred[1]
                            else:
                                to_add = value_to_add
                    set_by_keypath(wd, keyseq, to_add)
                except KeyError:
                    to_add_starred = (keyseq, value_to_add)
        return wd

    def parse_usage(self, adj_form: str, usage_index: str, usage: str):
        '''Parses a word usage string and populates the dictionary with the relevant grammatical information.'''

        ###############################################################################################
        # First, retrieve grammatical information from "Übersicht" (declension) table, if available. #
        ###############################################################################################
        uebersicht = re.search(uebersicht_adj_regex, usage)
        if uebersicht:
            decl_table = uebersicht.group(1)
            try:
                set_by_keypath(self, [adj_form, usage_index], self.parse_decl_table(decl_table))
                for twig in twig_collector(self[adj_form][usage_index]):
                    if '—' in twig:
                        twig.remove('—')  # remove '—' from the list of values to add
                    if '-' in twig:
                        twig.remove('-')
                    if '–' in twig:
                        twig.remove('–')
            except Exception as ex:
                print("Couldn't parse declension table:", adj_form, usage_index, ': ', ex)

        ##############################################
        # Checking for positive form-only adjectives #
        ##############################################

        keine_steigerung_match = re.search(keine_steigerung_pattern, usage)
        if keine_steigerung_match:
            set_by_keypath(self, [adj_form, usage_index, 'decl_feat'], ['no_comp'])

        ##############################################
        # Checking for positive form-only adjectives #
        ##############################################
        adj_decl_match = re.search(adj_no_decl_pattern, usage)
        if adj_decl_match:
            try:
                get_by_keypath(self, [adj_form, usage_index, 'decl_feat'])
                decl_feat = get_by_keypath(self, [adj_form, usage_index, 'decl_feat']) + ['no_decl']
            except KeyError:
                decl_feat = ['no_decl']
            set_by_keypath(self, [adj_form, usage_index, 'decl_feat'], decl_feat)

        ########################################################
        # Checking for attributive/predicative-only adjectives #
        ########################################################

        adj_only_attr_match = re.search(adj_only_attr_pattern, usage)
        if adj_only_attr_match:
            try:
                get_by_keypath(self, [adj_form, usage_index, 'attr_pred'])
                attr_pred = get_by_keypath(self, [adj_form, usage_index, 'attr_pred']) + ['attr_only']
            except KeyError:
                attr_pred = ['attr_only']
            set_by_keypath(self, [adj_form, usage_index, 'attr_pred'], attr_pred)

        adj_only_pred_match = re.search(adj_only_pred_pattern, usage)
        if adj_only_pred_match:
            try:
                get_by_keypath(self, [adj_form, usage_index, 'attr_pred'])
                attr_pred = get_by_keypath(self, [adj_form, usage_index, 'attr_pred']) + ['pred_only']
            except KeyError:
                attr_pred = ['pred_only']
            set_by_keypath(self, [adj_form, usage_index, 'attr_pred'], attr_pred)


    def parse_word_page(self, adj_form: str, page_list: list):
        '''Parses a word page from the xml file, separates it into usages and calls the usage parser function on each usage.'''
        not_german_word = False  # variable to keep track of non-German word entries (==) within a page.
        usages = []
        usage = []
        for line in page_list:
            usage_begin_match = re.search(new_usage_pattern, line)
            new_heading_two_matches = re.search(new_heading_two_regex, line)
            if new_heading_two_matches:
                if new_heading_two_matches.group('lang') == 'Deutsch':
                    not_german_word = False
                else:
                    not_german_word = True
            if not_german_word == False:
                if usage_begin_match:
                    if usage:
                        usages.append(usage)
                    usage = []
                    usage.append(line)
                else:
                    usage.append(line)
        usages.append(usage)  # because no "new_usage_pattern" at the end of the page, we need this after the for-cycle to add the last usage to the usages list.
        usages.pop(0)
        for usage in usages:
            # we do not want to include usages that are not German adjectives:
            if not re.search(de_adj_regex, '\n'.join(usage)):
                continue
            usage_index = "u" + str(usages.index(usage) + 1)  # so usage numbering starts from 1, not 0
            self.parse_usage(adj_form, usage_index, '\n'.join(usage))


    def generate_entries(self, file_path):
        '''Populates dictionary with noun information from the German wiktionary xml at file_path.'''
        with open(file_path, 'r', encoding='utf-8') as wikif:
            page_list = []
            page_no = 0
            print('Generating dictionary with adjectival information from wiktionary source: {0}\nThis may take several minutes . . .'.format(file_path))
            for line in wikif:
                page_list.append(line)
                if '</page>' in line:
                    page_no += 1
                    if page_no % 50000 == 0:
                        print(page_no, 'pages processed')

                    one_page_str = ''.join(page_list)
                    # ## Cleaning up page before parsing:
                    one_page_str = clean_up_string(one_page_str)

                    page_list = one_page_str.splitlines()

                    # we are only interested in pages which contain German adjectival information
                    if re.search(de_adj_regex, one_page_str) is None:
                        page_list = []
                        continue

                    word_match = re.search(de_headword_spaces_allowed_regex, one_page_str)
                    if word_match:
                        title_match = re.search(title_pattern, one_page_str)
                        if title_match:
                            adj_form = title_match.group('pagetitle')
                            ## Ignore pages under wiktionary-namespaces:
                            if re.match(namensraum_simple + colon, adj_form) or re.match(namensraum_simple + diskussion_colon, adj_form):
                                page_list = []
                                continue
                        else:
                            page_list = []
                            continue
                    else:
                        page_list = []
                        continue
                    # call the next lower level parser function on a page with German noun info:
                    self.parse_word_page(adj_form, page_list)
                    # delete entries with no usages (can happen if Abkürzung-only info in page)
                    try:
                        if not self[adj_form]:
                            del self[adj_form]
                    except KeyError:
                        pass
                    page_list = []
            print('Read {0} pages.'.format(page_no))
            print('Generated {0} entries.'.format(len(self)))


##############################################################
#  Patterns and other variables for parsing wiktionary xml   #
##############################################################

# The morphological attributes we will collect from adjectival inflection tables (if available):
MORPH_ATTRS_ADJ = ['Positiv', 'Komparativ', 'Superlativ', 'am', 'keine weiteren Formen']

patterns_adj_dic = {}
for feat_name in MORPH_ATTRS_ADJ:
    patterns_adj_dic[feat_name.lower().replace(' ', '_') + '_pattern'] = r"\|{0} *(\*)?\** *= *([^\n\|]+)\s*".format(feat_name)

regexes_adj_dic = {}
for pattern in patterns_adj_dic:
    regexes_adj_dic[pattern + '_regex'] = re.compile(patterns_adj_dic[pattern])

keymaps_adj = {reg_name: [re.sub('_pattern_regex', '', reg_name)] for reg_name in regexes_adj_dic}

###########################################
# Grammatical information regexes #
###########################################

uebersicht_adj_regex = re.compile(r"\{\{Deutsch Adjektiv Übersicht([^\}]+)\}\}", re.DOTALL)  # this is the übersicht (the decl. table)

keine_steigerung_pattern = re.compile(r"{{Worttrennung}}.*\n:.*{{kSt\.}}", re.U)  # for use in multiline texts ONLY!

# adj_no_decl_pattern = re.compile(r"([^=]|^|\n)=== {{Wortart\|Adjektiv\|Deutsch}}[^']+('')?indeklinabel('')?", re.U)  # the "''indeklinabel''" text follows the adjectival word type new usage indicator.
adj_no_decl_pattern = re.compile(r"([^=]|^|\n)=== {{Wortart\|Adjektiv\|Deutsch}}[^\n]+('')?indeklinabel('')?", re.U)  # the "''indeklinabel''" text follows the adjectival word type new usage indicator.
adj_only_attr_pattern = re.compile(r"([^=]|^|\n)=== {{Wortart\|Adjektiv\|Deutsch}}[^\n]+('')?nur attributiv('')?", re.U)  # the "''indeklinabel''" text follows the adjectival word type new usage indicator.
adj_only_pred_pattern = re.compile(r"([^=]|^|\n)=== {{Wortart\|Adjektiv\|Deutsch}}[^\n]+('')?nur prädikativ('')?", re.U)  # the "''indeklinabel''" text follows the adjectival word type new usage indicator.
