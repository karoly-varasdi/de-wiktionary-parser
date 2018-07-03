#!python3
# -*- coding: utf-8 -*-

'''
This is a sample script to use the German wiktionary parser python library.

Make sure you have installed dewiktionaryparser.
To install dewiktionaryparser, navigate to the dist directory of the package and run the following command in your terminal:
pip install FILENAME-OF-TAR-GZ-FILE
'''

# import the noun parser module functions:
import dewiktionaryparser as dw

######################################
######################################
###   NOUN-RELATED DICTIONARIES    ###
######################################
######################################

##########################################################
# Generating dictionaries from scratch (= from xml file) #
##########################################################

# initialize a dictionary for grammatical information:
noun_entries = dw.GermanNounEntriesDict()

# generate entries from dewiktionary-20180601-pages-meta-current.xml located in the data folder under current working directory:
noun_entries.generate_entries('.\data\dewiktionary-20180601-pages-meta-current.xml')
# # save the resulting dictionary under the data folder of the current working dictionary:
# noun_entries.export_to_json('.\data\de_noun_entries.json')

# create inverse dictionary for grammatical information dictionary:
inv_dic = noun_entries.make_inv_dict()
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
noun_entries.enhance_usages(translations)
# save the resulting dictionary under the data folder of the current working dictionary:
noun_entries.export_to_json('.\data\de_noun_entries_with_translations.json')

###########################################
# Retrieving dictionaries from .json file #
###########################################

# noun_entries = dw.GermanNounEntriesDict()
# noun_entries.retrieve_from_json('.\data\de_noun_entries_with_translations.json')
# print("Main dictionary 'noun_entries' has been loaded.\n")
# inv_dic = dw.WordEntriesDict()
# inv_dic.retrieve_from_json('.\data\de_noun_entries_inv.json')
# print("Dictionary 'inv_dic' mapping word form variants to their base forms is loaded.\n")
# inv_dic_trans = dw.WordEntriesDict()
# inv_dic_trans.retrieve_from_json('.\data\de_noun_translations_inv.json')
# print("Dictionary 'inv_dic_trans' mapping English words to their possible German sources is loaded.\n")


#################################################
#     Creating a subdictionary of common nouns  #
#################################################

# create a subdictionary of noun_entries containing common nouns only:
commons = noun_entries.make_commons_dict()

# save the resulting dictionary under the data folder of the current working dictionary:
commons.export_to_json('.\data\de_noun_entries_commons.json')

# create inverse dictionary:
inv_dic_commons = commons.make_inv_dict()
# save the resulting dictionary under the data folder of the current working dictionary:
inv_dic_commons.export_to_json('.\data\de_noun_entries_commons_inv.json')



###########################################
###########################################
###   ADJECTIVE-RELATED DICTIONARIES    ###
###########################################
###########################################

##########################################################
# Generating dictionaries from scratch (= from xml file) #
##########################################################

# generating and saving the adjectival grammatical information dictionary:
adj_entries = dw.GermanAdjEntriesDict()
adj_entries.generate_entries('.\data\dewiktionary-20180601-pages-meta-current.xml')

# generating and saving the inverse dictionary:
adj_entries_inv = adj_entries.make_inv_dict()
adj_entries_inv.export_to_json('.\data\de_adj_entries_inv.json')

# generating and saving the adjective translations dictionary:
adj_translations = dw.GermanAdjTranslationDict()
adj_translations.generate_translations('.\data\dewiktionary-20180601-pages-meta-current.xml')

# generating and saving the inverse dictionary:
adj_translations_inv = adj_translations.make_inv_dict()
adj_translations_inv.export_to_json('.\data\de_adj_translations_inv _inv.json')

# enhancing grammatical dictionary with translation information and saving it:
adj_entries.enhance_usages(translations)
# save the resulting dictionary under the data folder of the current working dictionary:
adj_entries.export_to_json('.\data\de_adj_entries_with_translations.json')


###########################################
# Retrieving dictionaries from .json file #
###########################################

# adj_entries = dw.GermanAdjEntriesDict()
# adj_entries.retrieve_from_json('.\data\de_adj_entries_with_translations.json')
# print("Main dictionary 'adj_entries' has been loaded.\n")
# inv_dic_adj = dw.WordEntriesDict()
# inv_dic_adj.retrieve_from_json('.\data\de_adj_entries_inv.json')
# print("Dictionary 'inv_dic' mapping word form variants to their base forms is loaded.\n")
# inv_dic_adj_trans = dw.WordEntriesDict()
# inv_dic_adj_trans.retrieve_from_json('.\data\de_adj_translations_inv.json')
# print("Dictionary 'inv_dic_trans' mapping English words to their possible German sources is loaded.\n")


#########################################################################
##  Creating a super-dictionary containing nouns and adjectives alike  ##
#########################################################################

# ## The following assumes that both adj_entries and noun_entries has been loaded and populated as above.
#
# # initialize a generic WordEntriesDict dictionary:
# word_entries = dw.WordEntriesDict()
#
# # populate it with noun information:
# word_entries.update(noun_entries)
#
# # now add adjectival words and word usages:
# for w in adj_entries:
#     if w not in word_entries:
#         word_entries.setdefault(w, adj_entries[w])
#     else:
#         for u in adj_entries[w]:
#             if u not in word_entries[w]:
#                 word_entries[w].setdefault(u, adj_entries[w][u])
