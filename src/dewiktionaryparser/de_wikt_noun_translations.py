#!python3
# -*- coding: utf-8 -*-

from .common_defs import *

# This script creates a dictionary of (currently only English) translations of German nouns and abbreviations.
# Note: no filtering for Abbreviation-only entries, so the translations contain entries like "usw." ('etc.').
# Note: not all German noun entries have English translations. (Especially special word types like family names tend not to.) Also, not all lexemes of a noun usage have associated translations.

'''
See German wiktionary help files on translations:
https://de.wiktionary.org/wiki/Hilfe:Übersetzungen 
https://de.wiktionary.org/wiki/Hilfe:Ü-Vorlagen
'''

class GermanNounTranslationDict(WordEntriesDict):

    def make_inv_dict(self, exclude=list(), include=list({'translations'})):
        '''Returns an inverse dictionary containing by default (with exclude=list(), include=list({'translations'})) only translations as keys.'''
        inv_dict = super().make_inv_dict(exclude=exclude, include=include)
        return WordEntriesDict(inv_dict)

    def generate_translations(self, file_path, encoding='utf-8', strict=False):
        '''Populates self with translations generated from German wiktionary xml file.'''
        with open(file_path, 'r', encoding=encoding) as wikif:
            page_list = []
            page_no = 0
            print('Generating translations from wiktionary source: {0}\nThis may take several minutes . . .'.format(file_path))
            for line in wikif:
                page_list.append(line)
                if '</page>' in line:
                    page_no += 1
                    if page_no % 50000 == 0:
                        print(page_no, 'pages processed')

                    one_page_str = ''.join(page_list)
                    ## Cleaning up page before parsing:
                    one_page_str = clean_up_string(one_page_str)

                    page_list = one_page_str.splitlines()

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
                    self.parse_word_page_transl(page_list, noun_form, strict)
                    try:
                        if not self[noun_form]:
                            del self[noun_form]
                    except KeyError:
                        pass
                    page_list = []
            print('\nRead {0} pages.'.format(page_no))
            print('Generated {0} entries.'.format(len(self)))

    def parse_word_page_transl(self, page_list: list, noun_form: str, strict=False):
        '''Parses a German word page (between <page> .. </page> tags) from the xml file, separates it into usages and calls the usage parser function on each usage.'''
        not_german_word = False
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
            if strict:
                self.parse_usage_for_en_translation_strict('\n'.join(usage), usage_index, noun_form)
            else:
                self.parse_usage_for_en_translation_greedy('\n'.join(usage), usage_index, noun_form)

    def parse_usage_for_en_translation_strict(self, usage: str, usage_index: str, noun_form: str):
        '''Parses a word usage (level 3 heading in wiktioanry) for translations of the German noun. Uses a strict heuristic, only collecting information from the translation tags (e.g., "[[insect]] {{Ü|en|colony}}" will be entered as "colony").'''
        transl_en_line_match = re.search(transl_en_line_regex, usage)
        if transl_en_line_match:
            transl_en_line = transl_en_line_match.group(0)
            # Example: "*{{en}}: [1] {{Ü|en|cock}}, {{Ü|en|rooster}}; [2] {{Ü|en|cock}}; [4] {{Ü|en|tap}}, {{Ü|en|valve}}; [5] {{Ü|en|hammer}}"

            ## cleaning up translation line:
            for todel in to_del_strings_transl:
                transl_en_line = re.sub(todel, '', transl_en_line)
            transl_en_line = re.sub(to_del_char_from_ubersetzung_tag, '\1\2', transl_en_line)

            transl_lexeme_and_transl_match = re.findall(transl_lexeme_and_transl_regex, transl_en_line)

            if transl_lexeme_and_transl_match:
                ## a list of (<lexeme-specification-string>, <translations-string>) pairs
                for bylex in transl_lexeme_and_transl_match:
                    # collecting the lexeme numbers:
                    lexeme_spec = bylex[0]
                    transl_lex_range_match = re.findall(transl_lex_range_regex, lexeme_spec)
                    lexemes = []
                    for tuple in transl_lex_range_match:  # from lexeme ranges, e.g., 1-4
                        lex_first = tuple[0]
                        lex_last = tuple[1]
                        lexemes.extend([str(i) for i in range(int(lex_first), int(lex_last) + 1)])
                        lexeme_spec = re.sub(r"{0}[-–]{1}".format(lex_first, lex_last), '', lexeme_spec)
                    transl_lexes_from_multi_lexeme_match = re.findall(transl_lexes_from_lexeme_and_transl_regex, lexeme_spec)  # adding remaining lexeme specifications, e.g., 1, 3
                    for lex in transl_lexes_from_multi_lexeme_match:
                        lexemes.append(lex)

                    # finding translations for the lexemes in lexemes:
                    lexeme_translations = []
                    transl_en_match = re.findall(transl_en_regex, bylex[1])
                    for match in transl_en_match:
                        lexeme_translations.append(match[3])

                    # adding lexeme_specification + translations to the dictionary:
                    if lexeme_translations:
                        for lexeme in lexemes:
                            lexeme = 'm' + lexeme  # adding 'm' for 'meaning'
                            try:
                                to_add = get_by_keypath(self, [noun_form, usage_index, 'translations', 'en', lexeme]) + lexeme_translations
                            except KeyError:
                                to_add = lexeme_translations
                            set_by_keypath(self, [noun_form, usage_index, 'translations', 'en', lexeme], to_add)

    def parse_usage_for_en_translation_greedy(self, usage: str, usage_index: str, noun_form: str):
        '''Parses a word usage (level 3 heading in wiktioanry) for translations of the German noun. Uses a looser, more greedy heuristic, and collects information from before the translation tags (e.g., "[[insect]] {{Ü|en|colony}}" will be entered as "insect colony")'''
        transl_en_line_match = re.search(transl_en_line_regex, usage)
        if transl_en_line_match:
            transl_en_line = transl_en_line_match.group(0)
            # Example: "*{{en}}: [1] {{Ü|en|cock}}, {{Ü|en|rooster}}; [2] {{Ü|en|cock}}; [4] {{Ü|en|tap}}, {{Ü|en|valve}}; [5] {{Ü|en|hammer}}"

            ## cleaning up translation line:
            for todel in to_del_strings_transl:
                transl_en_line = re.sub(todel, '', transl_en_line)
            transl_en_line = re.sub(to_del_char_from_ubersetzung_tag, '\1\2', transl_en_line)

            transl_lexeme_and_transl_match = re.findall(transl_lexeme_and_transl_regex, transl_en_line)

            if transl_lexeme_and_transl_match:
                ## a list of (<lexeme-specification-string>, <translations-string>) pairs
                for bylex in transl_lexeme_and_transl_match:
                    # collecting the lexeme numbers:
                    lexeme_spec = bylex[0]
                    transl_lex_range_match = re.findall(transl_lex_range_regex, lexeme_spec)
                    lexemes = []
                    for tuple in transl_lex_range_match:  # from lexeme ranges, e.g., 1-4
                        lex_first = tuple[0]
                        lex_last = tuple[1]
                        lexemes.extend([str(i) for i in range(int(lex_first), int(lex_last) + 1)])
                        lexeme_spec = re.sub(r"{0}[-–]{1}".format(lex_first, lex_last), '', lexeme_spec)
                    transl_lexes_from_multi_lexeme_match = re.findall(transl_lexes_from_lexeme_and_transl_regex, lexeme_spec)  # adding remaining lexeme specifications, e.g., 1, 3
                    for lex in transl_lexes_from_multi_lexeme_match:
                        lexemes.append(lex)

                    # finding translations for the lexemes in lexemes:
                    lexeme_translations = []
                    ## splitting the big list into translations along a comma -- note: e.g., won't include pre-translation "insect society" in "[5] [[insect]] [[society]], {{Ü|en|colony}}" (in "Staat")
                    translation_spec_list = bylex[1].split(',')
                    for translation_spec in translation_spec_list:
                        transl_en_match = re.findall(transl_en_regex, translation_spec)
                        for match in transl_en_match:
                            pre_translation_stuff = match[0]
                            pre_translation_stuff = re.sub(r'^\W+\s+', '', pre_translation_stuff)
                            pre_translation_stuff = re.sub(r'^[^\w\(]+\s*', '', pre_translation_stuff)
                            pre_translation_stuff = re.sub(r'^\W+\s*$', '', pre_translation_stuff)
                            pre_translation_stuff = re.sub(r'^\(auch\:\s*', '', pre_translation_stuff)
                            translation_stuff = match[3]
                            if pre_translation_stuff:
                                translation_stuff = pre_translation_stuff + translation_stuff
                            lexeme_translations.append(translation_stuff)

                    # adding lexeme_specification + translations to the dictionary:
                    if lexeme_translations:
                        for lexeme in lexemes:
                            lexeme = 'm' + lexeme  # adding 'm' for 'meaning'
                            try:
                                to_add = get_by_keypath(self, [noun_form, usage_index, 'translations', 'en', lexeme]) + lexeme_translations
                            except KeyError:
                                to_add = lexeme_translations
                            set_by_keypath(self, [noun_form, usage_index, 'translations', 'en', lexeme], to_add)



#####################################################
#  Patterns and variables used to get translations  #
#####################################################

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


######################################
# Translations-specific delete list  #
######################################

empty_entrans_tag = r"\{\{Ü\|en\}\}"  # e.g., in 'Windschutzscheibenwaschanlage'
wiki_tag_string = r"\(?\{\{[^Ü][^\}]*\}\}\)?"  # delete all non-translation tags, e.g., {{amer.}}
wiki_italics_string = r"\(?''[^']+''\)?\s*"
to_del_char_from_ubersetzung_tag = r"(\{\{Ü\|en\|[^\}]*),([^\}]*\}\})"  # to remove comma replace with \1\2 (e.g., "{{Ü|en|atomic absorption spectrometry, en|atomic absorption spectroscopy}}")
to_del_strings_transl = [wiki_italics_string, wiki_tag_string, empty_entrans_tag, angle_quoted_string, quoted_string] # note: order might matter (e.g, wiki_italics string before wiki_tag_string)
