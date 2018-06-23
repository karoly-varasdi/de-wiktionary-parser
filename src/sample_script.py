#!python3
# -*- coding: utf-8 -*-

'''
This is a sample script to use the German wiktionary parser python library.

Make sure you have installed dewiktionaryparser.
To install dewiktionaryparser, navigate to the dist directory of the package and run the following command in your terminal:
pip install dewiktionaryparser-1.0.tar.gz
'''

# import the noun parser module functions:
try:
    import dewiktionaryparser as dw
except ModuleNotFoundError:
    import src.dewiktionaryparser as dw

##########################################################
# Generating dictionaries from scratch (= from xml file) #
##########################################################

# initialize a dictionary for grammatical information:
word_entries = dw.GermanNounEntriesDict()

# generate entries from dewiktionary-20180601-pages-meta-current.xml located in the data folder under current working directory:
word_entries.generate_entries('.\data\dewiktionary-20180601-pages-meta-current.xml')
# # save the resulting dictionary under the data folder of the current working dictionary:
# word_entries.export_to_json('.\data\de_noun_entries.json')

# create inverse dictionary for grammatical information dictionary:
inv_dic = word_entries.make_inv_dict()
# save the resulting dictionary under the data folder of the current working dictionary:
inv_dic.export_to_json('.\data\de_noun_entries_inv.json')


# initialize a dictionary for translation information:
translations = dw.GermanNounTranslationDict()
# generate entries from dewiktionary-20180601-pages-meta-current.xml located in the data folder under current working directory:
translations.generate_translations('.\data\dewiktionary-20180601-pages-meta-current.xml')
# # alternatively, generate entries using a strict, non-greedy algorithm (excludes spurious explanation texts, but also incurs information loss):
# translations.generate_translations('.\data\dewiktionary-20180601-pages-meta-current.xml', strict=True)
# # save the resulting dictionary under the data folder of the current working dictionary:
# translations.export_to_json('.\data\de_noun_translations.json')

# create inverse dictionary for translation information dictionary:
inv_dic_translations = translations.make_inv_dict()
# save the resulting dictionary under the data folder of the current working dictionary:
inv_dic_translations.export_to_json('.\data\de_noun_translations_inv.json')


# enhance grammatical dictionary with translation information  #
word_entries.enhance_usages(translations)
# save the resulting dictionary under the data folder of the current working dictionary:
word_entries.export_to_json('.\data\dde_noun_entries_with_translations.json')

###########################################
# Retrieving dictionaries from .json file #
###########################################

# word_entries = dw.GermanNounEntriesDict()
# word_entries.retrieve_from_json('.\data\de_noun_entries_with_translations.json')
# print("Main dictionary 'word_entries' has been loaded.\n")
# inv_dic = dw.WordEntriesDict()
# inv_dic.retrieve_from_json('.\data\de_noun_entries_inv.json')
# print("Dictionary 'inv_dic' mapping word form variants to their base forms is loaded.\n")
# inv_dic_trans = dw.WordEntriesDict()
# inv_dic_trans.retrieve_from_json('.\data\de_noun_translations_inv.json')
# print("Dictionary 'inv_dic_trans' mapping English words to their possible German sources is loaded.\n")


#################################################
#     Creating a subdictionary of common nouns  #
#################################################

# create a subdictionary of word_entries containing common nouns only:
commons = word_entries.make_commons_dict()

# save the resulting dictionary under the data folder of the current working dictionary:
commons.export_to_json('.\data\de_noun_entries_commons.json')

# create inverse dictionary:
inv_dic_commons = commons.make_inv_dict()
# save the resulting dictionary under the data folder of the current working dictionary:
inv_dic_commons.export_to_json('.\data\de_noun_entries_commons_inv.json')

