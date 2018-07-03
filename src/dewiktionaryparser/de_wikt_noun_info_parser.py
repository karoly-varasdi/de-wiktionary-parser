#!python3
# -*- coding: utf-8 -*-

from .common_defs import *
import ujson


class GermanNounEntriesDict(WordEntriesDict):
    """Dictionary for storing morphological information about German nouns from the German wiktionary."""

    def make_inv_dict(self, exclude=list({'genus'}), include=list({'gen_case_num'})):
        '''Returns an inverse dictionary containing by default (with exclude=list({'genus'}), include=list({'gen_case_num'})) only declined forms as keys.'''
        inv_dict = super().make_inv_dict(exclude=exclude, include=include)
        return WordEntriesDict(inv_dict)

    def make_commons_dict(self):
        '''Generates a subdictionary which doesn't have entries with the key 'spec_word_type' '''
        print('Generating entries for the common-nouns-only dictionary . . .')
        copy_dic = GermanNounEntriesDict(ujson.loads(ujson.dumps(self)))
        orig_size = len(copy_dic)
        for w in self:
            for u in self[w]:
                if self[w][u].__contains__('spec_word_type'):
                    del copy_dic[w][u]
            if not copy_dic[w]:
                del copy_dic[w]
        new_size = len(copy_dic)
        print('Generated {0} entries (excluded {1} special words).'.format(new_size, orig_size - new_size))
        return copy_dic


    ############################################
    #    Methods for parsing wiktionary xml.   #
    ############################################

    def full_info(self, decl_table: str):
        '''Returns a list of ('MORPH_pattern_regex', ['DECL_NUM', 'STARRED', 'VALUE']) tuples for morphological pattern regexes in the regexes dictionary.'''
        return [(reg, re.findall(regexes_noun_dic[reg], decl_table)) for reg in regexes_noun_dic]
        ## Sample output:
        # [('genus_pattern_regex', [('', '', 'f')]), ('nominativ_singular_pattern_regex', [('', '', 'Mutter')]), ('nominativ_plural_pattern_regex', [('1',
        # '', 'Mütter'), ('2', '', 'Muttern')]), ('genitiv_singular_pattern_regex', [('', '', 'Mutter')]), ('genitiv_plural_pattern_regex', [('1', '',
        # 'Mütter'), ('2', '', 'Muttern')]), ('dativ_singular_pattern_regex', [('', '', 'Mutter')]), ('dativ_plural_pattern_regex', [('1', '', 'Müttern'),
        # ('2', '', 'Muttern')]), ('akkusativ_singular_pattern_regex', [('', '', 'Mutter')]), ('akkusativ_plural_pattern_regex', [('1', '', 'Mütter'),
        # ('2', '', 'Muttern')])]

    def parse_decl_table(self, decl_table):
        '''Parses a declension table (a multi-line string) and returns a dictionary of grammatical information ready for inclusion as value of the usage number key.'''
        wd = {}
        info = self.full_info(decl_table)
        to_add_starred = ()  # (keyseq, str) tuple for starred versions appearing before non-starred versions
        to_add_starred_pre = ()  # (keyseq, str) tuple for stuff preceding the actual value (typically in dialectal forms like 'Krebbelche' (e.g., "von dem")

        for pair in info:
            morphs_list = keymaps_noun[pair[0]]  # e.g., ['nominativ', 'singular'] or ['genus']
            list_of_triples = pair[1]  # (decl_num, *, value)
            morphs_pre_list = [morph + '_pre' for morph in morphs_list]  # e.g., ['nominativ_pre', 'singular_pre']
            for three_tupl in list_of_triples:
                three_list = list(three_tupl)
                ## splitting value along spaces, so that we can collect the last word as value_to_add, and the rest as prefixes:
                three_list_2_list_of_words = three_list[2].strip().split()
                try:
                    if 'genus' in morphs_list and '+' in three_list_2_list_of_words[-1]:
                        value_to_add = re.split(r" *\+ *", three_list_2_list_of_words[-1])
                    else:
                        value_to_add = [three_list_2_list_of_words[-1]]
                    value_prefix = None
                    if len(three_list_2_list_of_words) > 1:
                        value_prefix = ' '.join(three_list_2_list_of_words[:-1])
                except IndexError:
                    continue

                ## setting the string before the declension number appearing in the dictionary:
                if morphs_list[-1] == 'singular' or morphs_list[-1] == 'genus':
                    pre_decnum = 'sg'
                elif morphs_list[-1] == 'plural':
                    pre_decnum = 'pl'
                # currently no other option in the declension tables, but "else" included for potential extensions:
                else:
                    pre_decnum = 'd'

                ## setting the path as a keyseq list where value is to be entered:
                if not three_list[0]:  # use declension 1 if only one non-numbered declension is given
                    decnum = pre_decnum + '1'
                else:
                    decnum = pre_decnum + three_list[0]  # prepend sg or pl to declension numbers
                keyseq = ['gen_case_num'] + morphs_list + [decnum]
                keyseq_pre = ['spec_pre'] + morphs_pre_list + [decnum]
                try:
                    if three_list[1]:
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
                if value_prefix:
                    try:
                        if three_list[1]:
                            if get_by_keypath(wd, keyseq_pre):
                                value_prefix_to_add = get_by_keypath(wd, keyseq_pre) + [value_prefix]
                        else:
                            if not to_add_starred_pre:
                                value_prefix_to_add = [value_prefix]
                            else:
                                if keyseq_pre == to_add_starred_pre[0]:
                                    value_prefix_to_add = [value_prefix, to_add_starred_pre[1]]
                                else:
                                    value_prefix_to_add = [value_prefix]
                        set_by_keypath(wd, keyseq_pre, value_prefix_to_add)
                    except KeyError:
                        to_add_starred_pre = (keyseq_pre, value_prefix)
        return wd

    def parse_usage(self, noun_form: str, usage_index: str, usage: str):
        '''Parses a word usage string and populates the dictionary with the relevant grammatical information.'''

        ###############################################################################################
        # First, retrieve grammatical information from "Übersicht" (declension) table, if available. #
        ###############################################################################################
        uebersicht = re.search(uebersicht_noun_regex, usage)
        if uebersicht:
            decl_table = uebersicht.group(2)
            try:
                set_by_keypath(self, [noun_form, usage_index], self.parse_decl_table(decl_table))
                for twig in twig_collector(self[noun_form][usage_index]):
                    if '—' in twig:
                        twig.remove('—')  # remove '—' from the list of values to add
                    if '-' in twig:
                        twig.remove('-')
                    if '–' in twig:
                        twig.remove('–')
            except:
                print("Couldn't parse declension table:", noun_form, usage_index)

        ################################################################
        # If no gender info from Übersicht (declension) table available, use gender information from the new usage (===) line and add it under declension number 1 under the relevant usage. #
        ################################################################
        try:
            if get_by_keypath(self, [noun_form, usage_index, 'gen_case_num', 'genus', 'sg1']) == ['0']:
                set_by_keypath(self, [noun_form, usage_index, 'gen_case_num', 'genus', 'sg1'], [])
                new_usage_line_match = re.search(new_usage_line, usage)
                usage_line = new_usage_line_match.group(0)
                self.gender_from_heading(noun_form, usage_index, usage_line)
        except KeyError:
            try:
                if get_by_keypath(self, [noun_form, usage_index, 'gen_case_num', 'genus']):
                    pass
            except KeyError:
                new_usage_line_match = re.search(new_usage_line, usage)
                usage_line = new_usage_line_match.group(0)
                self.gender_from_heading(noun_form, usage_index, usage_line)

        ############################################################
        # Adding additional usage-related grammatical information. #
        ############################################################

        ## -sch declension nouns like "Deutsch":
        uebersicht_sch = re.search(uebersicht_sch_regex, usage)
        if uebersicht_sch:
            set_by_keypath(self, [noun_form, usage_index, 'decl_type'], ['-sch'])

        ## adjectival declension nouns like "Erwachsene":
        uebersicht_adj = re.search(uebersicht_adjektivisch_regex, usage)
        if uebersicht_adj:
            set_by_keypath(self, [noun_form, usage_index, 'decl_type'], ['adj'])

        else:
            adj_decl_match = re.search(adj_decl_pattern, usage)
            if adj_decl_match:
                set_by_keypath(self, [noun_form, usage_index, 'decl_type'], ['adj'])

        ## The following, female/male related form searcher version is not implemented, as it is a purely semantic feature, and in the case of adjectival declension, deterministic.
        # adj_decl_match = re.search(adj_decl_pattern, usage)
        # if adj_decl_match:
        #     if not uebersicht_adj:
        #         set_by_keypath(self, [noun_form, usage_index, 'decl_type', 'dtype'],  ['adj'])
        #     adj_related_match = re.search(adj_related_pattern, usage)
        #     if adj_related_match:
        #         if adj_related_match.group('adjfm') == 'Männliche':
        #             relform_gender = 'rel_form_m'
        #         elif adj_related_match.group('adjfm') == 'Weibliche':
        #             relform_gender = 'rel_form_f'
        #         else:
        #             print('rel_form_?', noun_form, usage_index)
        #             relform_gender = 'rel_form_?'
        #         set_by_keypath(self, [noun_form, usage_index, 'decl_type', relform_gender],  [adj_related_match.group('relform')])

        #########################################
        #   Singular/plural tantum information  #
        #########################################

        sg_pl_tantum_match = re.search(sg_pl_tantum_pattern, usage)
        if sg_pl_tantum_match:
            # Note: "kPl." ("kein Plural") means it's a Sg tantum noun.
            if sg_pl_tantum_match.group('tantum') == 'Pl':
                set_by_keypath(self, [noun_form, usage_index, 'tantum'], ['Sg'])
            elif sg_pl_tantum_match.group('tantum') == 'Sg':
                set_by_keypath(self, [noun_form, usage_index, 'tantum'], ['Pl'])

        ###################################
        #  special feature information    #
        ###################################

        spec_feature_match = re.findall(spec_feature_pattern, usage)
        if spec_feature_match:
            set_by_keypath(self, [noun_form, usage_index, 'spec_word_type'], [])
            for spec_feat in spec_feature_match:
                if spec_feat not in self[noun_form][usage_index]['spec_word_type']:
                    self[noun_form][usage_index]['spec_word_type'].append(spec_feat)
            # Now remove Abkürzung-only entries, for which no other information is specified (e.g., "usw."):
            if 'Abkürzung' in self[noun_form][usage_index]['spec_word_type']:
                usage_dict = ujson.loads(ujson.dumps(self[noun_form][usage_index]))
                usage_dict['spec_word_type'].remove('Abkürzung')
                if not usage_dict['spec_word_type']:
                    del usage_dict['spec_word_type']
                if not usage_dict:
                    del self[noun_form][usage_index]
                    # note: in entries ['MP3', 'Fon', 'grad', 'Mal', 'BMW®', 'Bar', 'BAföG', 'Am', 'Ari', 'Jak', 'Hab', 'Mio', 'Hag', 'Dan', 'Stasi', 'C4', 'Röntgen'], there is 'u2', but no 'u1' as a result


    def gender_from_heading(self, noun_form, usage_index, usage_line):
        '''A helper function for parse_usage, to retrieve gender information from usage heading (===) line.'''
        gender_from_wortart_main_match = re.findall(gender_from_wortart_pattern_main, usage_line)
        keyseq = [noun_form, usage_index, 'gen_case_num', 'genus', 'sg1']
        if gender_from_wortart_main_match:
            set_by_keypath(self, keyseq, [])
            for gender_group in gender_from_wortart_main_match:
                for gender in gender_group:
                    if gender not in get_by_keypath(self, keyseq):
                        try:
                            to_add = get_by_keypath(self, keyseq) + [gender]
                        except KeyError:
                            to_add = [gender]
                        set_by_keypath(self, keyseq, to_add)


    def parse_word_page(self, noun_form: str, page_list: list):
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
            # we do not want to include usages that are not German nouns (e.g., the Interjektion for 'Alter'):
            if not re.search(de_noun_regex, '\n'.join(usage)):
                continue
            usage_index = "u" + str(usages.index(usage) + 1)  # so usage numbering starts from 1, not 0
            self.parse_usage(noun_form, usage_index, '\n'.join(usage))


    def generate_entries(self, file_path):
        '''Populates dictionary with noun information from the German wiktionary xml at file_path.'''
        with open(file_path, 'r', encoding='utf-8') as wikif:
            page_list = []
            page_no = 0
            print('Generating dictionary with noun information from wiktionary source: {0}\nThis may take several minutes . . .'.format(file_path))
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

                    # we are only interested in pages which contain German noun info
                    if re.search(de_noun_regex, one_page_str) is None:
                        page_list = []
                        continue

                    word_match = re.search(de_headword_regex, one_page_str)
                    if word_match:
                        title_match = re.search(title_pattern, one_page_str)
                        if title_match:
                            noun_form = title_match.group('pagetitle')
                            ## Ignore pages under wiktionary-namespaces:
                            if re.match(namensraum_simple + colon, noun_form) or re.match(namensraum_simple + diskussion_colon, noun_form):
                                page_list = []
                                continue
                        else:
                            page_list = []
                            continue
                    else:
                        page_list = []
                        continue
                    # call the next lower level parser function on a page with German noun info:
                    self.parse_word_page(noun_form, page_list)
                    # delete entries with no usages (can happen if Abkürzung-only info in page)
                    try:
                        if not self[noun_form]:
                            del self[noun_form]
                    except KeyError:
                        pass
                    page_list = []
            print('Read {0} pages.'.format(page_no))
            print('Generated {0} entries.'.format(len(self)))


##############################################################
#  Patterns and other variables for parsing wiktionary xml   #
##############################################################

# The morphological attributes we will collect from noun declension tables (if available):
MORPH_ATTRS_NOUN = ['Genus', 'Nominativ Singular', 'Nominativ Plural', 'Genitiv Singular', 'Genitiv Plural', 'Dativ Singular', 'Dativ Plural', 'Akkusativ Singular', 'Akkusativ Plural', ]

patterns_noun_dic = {}
for feat_name in MORPH_ATTRS_NOUN:
    patterns_noun_dic[feat_name.lower().replace(' ', '_') + '_pattern'] = r"\|{0} ?(\d)? *(\*)?\** *= *([^\n\|]+)\s*".format(feat_name)
    # patterns_noun_dic[feat_name.lower().replace(' ', '_') + '_pattern'] = r"\|{0} ?(\d)? *(\*)?\** *= *(\S+|—)[^(\s+\w+)]?".format(feat_name)
    # patterns_noun_dic[feat_name.lower().replace(' ', '_') + '_pattern'] = r"\|{0} ?(\d)?(\*)? *= *(([0-9|,|-])*\w+(-\w+)*|—)[^(\s+\w+)]?".format(feat_name)
    # patterns_noun_dic[feat_name.lower().replace(' ', '_') + '_pattern'] = r"\|{0} ?(\d)?(\*)? *= *(\w+|—)[^(\s+\w+)]?".format(feat_name)
    # patterns_noun_dic[name.lower().replace(' ', '_')+'_pattern'] = r"\|{0} ?(\d)?(\*)? *= *(\w+|—)".format(name)
# {'genus_pattern': '\\|Genus ?(\\d)?(\\*)?=(\\w+|—)', 'nominativ_singular_pattern': '\\|Nominativ Singular ?(\\d)?(\\*)?=(\\w+|—)',
# 'nominativ_plural_pattern': '\\|Nominativ Plural ?(\\d)?(\\*)?=(\\w+|—)', 'genitiv_singular_pattern': '\\|Genitiv Singular ?(\\d)?(\\*)?=(
# \\w+|—)', 'genitiv_plural_pattern': '\\|Genitiv Plural ?(\\d)?(\\*)?=(\\w+|—)', 'dativ_singular_pattern': '\\|Dativ Singular ?(\\d)?(\\*)?=(
# \\w+|—)', 'dativ_plural_pattern': '\\|Dativ Plural ?(\\d)?(\\*)?=(\\w+|—)', 'akkusativ_singular_pattern': '\\|Akkusativ Singular ?(\\d)?(\\*)?=(
# \\w+|—)', 'akkusativ_plural_pattern': '\\|Akkusativ Plural ?(\\d)?(\\*)?=(\\w+|—)'}

regexes_noun_dic = {}
for pattern in patterns_noun_dic:
    regexes_noun_dic[pattern + '_regex'] = re.compile(patterns_noun_dic[pattern])
# {'genus_pattern_regex': re.compile('\\|Genus ?(\\d)?(\\*)?=(\\w+|—)'), 'nominativ_singular_pattern_regex': re.compile('\\|Nominativ Singular ?(
# \\d)?(\\*)?=(\\w+|—)'), 'nominativ_plural_pattern_regex': re.compile('\\|Nominativ Plural ?(\\d)?(\\*)?=(\\w+|—)'),
# 'genitiv_singular_pattern_regex': re.compile('\\|Genitiv Singular ?(\\d)?(\\*)?=(\\w+|—)'), 'genitiv_plural_pattern_regex': re.compile(
# '\\|Genitiv Plural ?(\\d)?(\\*)?=(\\w+|—)'), 'dativ_singular_pattern_regex': re.compile('\\|Dativ Singular ?(\\d)?(\\*)?=(\\w+|—)'),
# 'dativ_plural_pattern_regex': re.compile('\\|Dativ Plural ?(\\d)?(\\*)?=(\\w+|—)'), 'akkusativ_singular_pattern_regex': re.compile('\\|Akkusativ
# Singular ?(\\d)?(\\*)?=(\\w+|—)'), 'akkusativ_plural_pattern_regex': re.compile('\\|Akkusativ Plural ?(\\d)?(\\*)?=(\\w+|—)')}

keymaps_noun = {reg_name: reg_name.split('_')[:-2] for reg_name in regexes_noun_dic}
# {'genus_pattern_regex': ['genus'], 'nominativ_singular_pattern_regex': ['nominativ', 'singular'], 'nominativ_plural_pattern_regex': ['nominativ',
# 'plural'], 'genitiv_singular_pattern_regex': ['genitiv', 'singular'], 'genitiv_plural_pattern_regex': ['genitiv', 'plural'],
# 'dativ_singular_pattern_regex': ['dativ', 'singular'], 'dativ_plural_pattern_regex': ['dativ', 'plural'], 'akkusativ_singular_pattern_regex': [
# 'akkusativ', 'singular'], 'akkusativ_plural_pattern_regex': ['akkusativ', 'plural']}


########################################
# Noun grammatical information regexes #
########################################

uebersicht_noun_regex = re.compile(r"\{\{Deutsch (Substantiv|Abkürzung|Toponym|Name|Nachname|Vorname|Eigenname|Buchstabe|Zahlklassifikator) Übersicht([^\}]+)\}\}", re.DOTALL)  # this is the übersicht (the decl. table)
uebersicht_sch_regex = re.compile(r"\{\{Deutsch Substantiv Übersicht\s+-sch[^\}]*\}\}", re.DOTALL)
uebersicht_toponym_regex = re.compile(r"\{\{Deutsch Toponym Übersicht[^\}]*\}\}", re.DOTALL)
uebersicht_adjektivisch_regex = re.compile(r"\{\{Deutsch adjektivisch Übersicht[^\}]*\}\}", re.DOTALL)

adj_decl_pattern = re.compile(r"([^=]|^|\n)=== {{Wortart\|Substantiv\|Deutsch}}[^']+('')?adjektivische Deklination('')?", re.U)  # the "''adjektivische Deklination''" text follows the nominal word type new usage indicator.
# Ex.: "=== {{Wortart|Substantiv|Deutsch}}, {{f}}, ''adjektivische Deklination'' ==="

# ### finding related forms in multi-line string:
# adj_related_pattern = re.compile(r"""\n\s*{{(?P<adjfm>Männliche|Weibliche)\s+Wortformen}}\s*\n  #first line: adjfm group: male or female related form
#     :\[\d+(,\s\d+)*\]\s\[\[(?P<relform>[^\]]+)\]\]   # second line: relform group is the related form itself
#     """, re.X)


## if new_usage_line, then we can look for multiple matches of gender:
gender_from_wortart_pattern_main = re.compile(r"{{(?P<gender>[fmn]+)\.?}}")  # for some reason, mn (masculine and neutral) is followed by a period: {{mn.}}. Then we need the closing curly brackets.

##############################
# Special word type patterns #
##############################

'''
Special word types are marked as {{Wortart|<WORD TYPE>|Deutsch}}: 
Abkürzung (abbreviation, e.g., VIP; note: not all are nouns!), Toponym (geographical name, e.g., Japan), 
Vorname (first name, e.g., Johann), Nachname (family name, e.g., Schmidt), Eigenname (proper name), 
Buchstabe (letter, e.g., A), Zahlklassifikator [classifier, e.g.: Paar], 
Wortverbindung [multi-word expressions; we don't collect them in our dictionary]
'''
spec_feature_pattern = re.compile(r""" # Ex. "{{Wortart|Vorname|Deutsch}}" >>> .group('spec') = "Vorname"
    \|(?P<spec>Abkürzung|Toponym|Name|Nachname|Vorname|Eigenname|Buchstabe|Straßenname)
    \|Deutsch}}""", re.X | re.U)

'''
Tantums: they are specified under {{Worttrennung}}. (If there is a declension table, the singular or plural is specified with -.)
Note: kPl means no plural, so it indicates a Sg tantum.

{{Worttrennung}}
:.*{{kPl.}} = kein Plural

{{Worttrennung}}
:.*{{kSg.}} = kein Singular
'''
sg_pl_tantum_pattern = re.compile(r"{{Worttrennung}}.*\n:.*{{k(?P<tantum>Pl|Sg)\.}}", re.U)  # for use in multiline texts ONLY!
