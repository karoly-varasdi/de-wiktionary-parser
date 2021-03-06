# Documentation on the types and structure of dictionaries

* [Dictionary types](#dictionary-types)
* [Dictionary structure](#dictionary-structure)
	* [The basic structure of a `GermanNounEntriesDict` dictionary](#dictionary-GermanNounEntriesDict)
	    * [Usages (`u<usage_#>`)](#usages)
	    * [`'gen_case_num'` and declensions (`sg#`, `pl#`)](#gencasenum)
	    * [`'spec_pre'` for multi-word inflected forms](#specpre)
	    * [`'decl_type'` for declension class](#decltype)
	    * [`'tantum'`](#tantum)
	    * [`'spec_word_type'` for non-common nouns](#specwordtype)
	* [The basic structure of a `GermanAdjEntriesDict` dictionary](#dictionary-GermanAdjEntriesDict)
	* [The basic structure of a translation dictionary (`GermanNounTranslationDict` and `GermanAdjTranslationDict`)](#dictionary-German-TranslationDict)
* [Some remarks on the entries](#remarks)


## <a name="dictionary-types"></a>Dictionary types 

We have defined dictionary subclasses, corresponding to different, though related dictionary types:
1. Noun-related dictionaries: 
    1. `GermanNounEntriesDict`: the instances of this class are dictionaries the entries of which contain grammatical (in particular, usage-related and morphological) information about the German nouns in the German wiktionary
    2. `GermanNounTranslationDict`: the instances of this class are dictionaries the entries of which contain (for the time being, only English) translations of the entries of a `GermanNounEntriesDict` (if such translations exist in the German wiktionary)
    
2. Adjective-related dictionaries:
    1. `GermanAdjEntriesDict`: the instances of this class are dictionaries the entries of which contain grammatical (primarily degree of comparison) information about the German adjectives in the German wiktionary
    2. `GermanAdjTranslationDict`: the instances of this class are dictionaries the entries of which contain (for the time being, only English) translations of the entries of a `GermanAdjEntriesDict` (if such translations exist in the German wiktionary)
    
3. `WordEntriesDict`: the superclass of the classes above

The dictionaries are populated with information by a parser script that parses the German Wiktionary xml pages into two kinds of dictionary: a *grammatical* or a *translation* dictionary.
The result of the parsing phase can then be exported (saved) in the popular JSON format. Beside generating 
and storing the dictionaries, there are methods and functions that manipulate, search, or display these dictionaries.      

## <a name="dictionary-structure"></a>Dictionary structure
Below we describe the structure of the generated dictionary entries in detail. The illustrative examples all pertain to the *June 1, 2018 version* of the German wiktionary dump, and they might have been modified by the time you are reading this text.
     
You can find a completely detailed chart of the noun entries extracted for the June 1, 2018 version of German wiktionary in the data folder under the name [dictionary_structure_for_June 1_2018.txt](./data/dictionary_structure_for_June 1_2018.txt). 

We are using *the following terminology*: the dictionaries below consist of several thousand **entries** which, in turn, are **headword:headword_content** pairs. The headword is always a string (e.g., 'Hahn'), and the content is itself again a dictionary or a list of strings (actual word forms or
 grammatical values). Since 
dictionaries are trees, we call the keyword sequences that start at the top node (e.g., 'Hahn') and end at a particular word form (e.g., 'Hahnes') **branches**, the strings like 'Hahnes' at the end of the branches **leaves**, while the lists thereof (e.g., ['Hahnes', 'Hahns']) **twigs**.    

### <a name="dictionary-GermanNounEntriesDict"></a>The basic structure of a `GermanNounEntriesDict` dictionary
```
{
 <noun_headword>: 
	{'u<usage_#>': 
		{'gen_case_num':
			{'genus': 
				{'sg<decl_#>': ['m'|'f'|'n',]},
			'akkusativ': 
				{'plural': 
					{'pl<decl_#>': [<pluralform1>,]},
				'singular': 
					{'sg<decl_#>': [<sgform1>,]}},
			'dativ':
				{'plural': 
					{'pl<decl_#>': [<pluralform1>,]},
				'singular': 
					{'sg<decl_#>': [<sgform1>,]}},
			'genitiv': 
				{'plural': 
					{'pl<decl_#>': [<pluralform1>,]},
				'singular': 
					{'sg<decl_#>': [<sgform1>,]}},
			'nominativ': 
				{'plural': 
					{'pl<decl_#>': [<pluralform1>,]},
				'singular': 
					{'sg<decl_#>': [<sgform1>,]}}
			},
		{'spec_pre':
			{'genus_pre': 
				{'sg<decl_#>': ['m'|'f'|'n',]},
			'akkusativ_pre': 
				{'plural_pre': 
					{'pl<decl_#>': [<pluralform1>,]},
				'singular_pre': 
					{'sg<decl_#>': [<sgform1>,]}},
			'dativ_pre':
				{'plural_pre': 
					{'pl<decl_#>': [<pluralform1>,]},
				'singular_pre': 
					{'sg<decl_#>': [<sgform1>,]}},
			'genitiv_pre': 
				{'plural_pre': 
					{'pl<decl_#>': [<pluralform1>,]},
				'singular_pre': 
					{'sg<decl_#>': [<sgform1>,]}},
			'nominativ_pre': 
				{'plural_pre': 
					{'pl<decl_#>': [<pluralform1>,]},
				'singular_pre': 
					{'sg<decl_#>': [<sgform1>,]}}
			},
		'decl_type': ['adj'|'-sch'],
		'tantum': ['Sg'|'Pl'],
		'spec_word_type': ['Abkürzung'|'Toponym'|'Eigenname'|'Nachname'|'Vorname'|'Name'|'Straßenname'],
		},
	},
}
```
In what follows we describe the features (aspects, keys) that we use in the entries.

#### <a name="usages"></a>-> Usages (`u<usage_#>`)
The information about a noun in the German wiktionary is partitioned into separate "usages" (level 3 headings in the German wiktionary); three usages in the case of the noun [*Hahn*](https://de.wiktionary.org/wiki/Hahn), for example:
```
{'u1': {'gen_case_num': {'akkusativ': {'plural': {'pl1': ['Hähne']},
                                       'singular': {'sg1': ['Hahn']}},
                         'dativ': {'plural': {'pl1': ['Hähnen']},
                                   'singular': {'sg1': ['Hahn', 'Hahne']}},
                         'genitiv': {'plural': {'pl1': ['Hähne']},
                                     'singular': {'sg1': ['Hahnes', 'Hahns']}},
                         'genus': {'sg1': ['m']},
                         'nominativ': {'plural': {'pl1': ['Hähne']},
                                       'singular': {'sg1': ['Hahn']}}}},
 'u2': {'gen_case_num': {'genus': {'sg1': ['m', 'f']}},
        'spec_word_type': ['Nachname']},
 'u3': {'gen_case_num': {'genus': {'sg1': ['n']}},
        'spec_word_type': ['Toponym'],
        'tantum': ['Sg']}}

``` 
Different usages usually involve differences in the grammatical properties of the word (such as having a different gender value or a making use of a different way to produce the plural forms) or describe a special usage of the word (such as when it is used as a family name or a place name), but 
it is also often the case that nouns with varying gender are lumped together in one usage only if the grammatical difference does not result in a semantic difference (see, e.g., [*Joghurt*](https://de.wiktionary.org/wiki/Joghurt)). At the highest level of a dictionary entry, the usage number 'u1', 
'u2', ... identifies a particular usage of the given word.

#### <a name="gencasenum"></a>-> `'gen_case_num'` and declensions (`sg#`, `pl#`)
The `'gen_case_num'` feature introduces the information concerning the gender (or genders) of the word in that particular usage, as well as its inflected forms in various cases (accusative, dative, genitive, and nominative) and numbers (singular and plural). When a word has several free variants for any case and number, they are grouped together. For example, the word [*Hahn*](https://de.wiktionary.org/wiki/Hahn) has 3 different usages, and in the first usage ('u1') its dative singular form may either be 'Hahn' or 'Hahne'. 

Sometimes a noun has several declensions: the noun [*Joghurt*](https://de.wiktionary.org/wiki/Joghurt), for example, has three different singular declensions. These three different declensions are marked by 'sg1', 'sg2' and 'sg3' in its first (and only) usage 'u1':
```
{'u1': {'gen_case_num': {'akkusativ': {'plural': {'pl1': ['Joghurts']},
                                       'singular': {'sg1': ['Joghurt'],
                                                    'sg2': ['Joghurt'],
                                                    'sg3': ['Joghurt']}},
                         'dativ': {'plural': {'pl1': ['Joghurts']},
                                   'singular': {'sg1': ['Joghurt'],
                                                'sg2': ['Joghurt'],
                                                'sg3': ['Joghurt']}},
                         'genitiv': {'plural': {'pl1': ['Joghurts']},
                                     'singular': {'sg1': ['Joghurts'],
                                                  'sg2': ['Joghurt'],
                                                  'sg3': ['Joghurts']}},
                         'genus': {'sg1': ['m'], 'sg2': ['f'], 'sg3': ['n']},
                         'nominativ': {'plural': {'pl1': ['Joghurts']},
                                       'singular': {'sg1': ['Joghurt'],
                                                    'sg2': ['Joghurt'],
                                                    'sg3': ['Joghurt']}}}}}

``` 
The 'sg#' values are *co-indexed* in the sense that the genus, akkusativ singular, dativ singular, genitiv singular and nominativ singular values under the same 'sg'-number go together to give one declension. Similarly, some words have several declensions in the plural; the noun [*Staat*](https://de.wiktionary.org/wiki/Staat) is a case in point:
```
{'u1': {'gen_case_num': {'akkusativ': {'plural': {'pl1': ['Staaten'],
                                                  'pl2': ['Stäte'],
                                                  'pl3': ['Staat'],
                                                  'pl4': ['Staate']},
                                       'singular': {'sg1': ['Staat']}},
                         'dativ': {'plural': {'pl1': ['Staaten'],
                                              'pl2': ['Stäten'],
                                              'pl3': ['Staaten'],
                                              'pl4': ['Staaten']},
                                   'singular': {'sg1': ['Staat', 'Staate']}},
                         'genitiv': {'plural': {'pl1': ['Staaten'],
                                                'pl2': ['Stäte'],
                                                'pl3': ['Staat'],
                                                'pl4': ['Staate']},
                                     'singular': {'sg1': ['Staats',
                                                          'Staates']}},
                         'genus': {'sg1': ['m']},
                         'nominativ': {'plural': {'pl1': ['Staaten'],
                                                  'pl2': ['Stäte'],
                                                  'pl3': ['Staat'],
                                                  'pl4': ['Staate']},
                                       'singular': {'sg1': ['Staat']}}}}}

```
Here, the corresponding 'pl'-numbers define one particular declension (there are four of them altogether), this time in the plural. There are two important remarks to make here, however:
1. The 'sg#' and the 'pl#' identifiers are obligatory, and they always start with '1' (even if there are no more of them).
2. Although all the word forms under 'sg1' go together, as do the forms under 'sg2', etc., and this is also true of 'pl1', etc., ***there is no such connection between the indices of the singular and the plural***. In other words, the forms under 'sg1' and 'pl1' do not necessarily go 
together to the exclusion of 'sg2' or 'pl2' and might have no intra-declension relationship at all. 

#### <a name="specpre"></a>-> `'spec_pre'` for multi-word inflected forms
The `'spec_pre'` feature only appears when an inflected form consists of multiple words. In this case, the last word is entered in the respective place under `gen_case_num`, while the rest (initial part) of the multi-word inflected form is entered in the respective place under `spec_pre`. 
(Note that the suffix *_pre* is appended to all feature names under `spec_pre`.) 
Such extra words typically come from dialectal variants, where special determiners are specified. For example, the value generated for [*Krebbelche*](https://de.wiktionary.org/wiki/Krebbelche) is the following:

```
{'u1': {'gen_case_num': {'akkusativ': {'plural': {'pl1': ['Krebbelcher']},
                                       'singular': {'sg1': ['Krebbelche']}},
                         'dativ': {'plural': {'pl1': ['Krebbelcher']},
                                   'singular': {'sg1': ['Krebbelche']}},
                         'genitiv': {'plural': {'pl1': ['Krebbelcher']},
                                     'singular': {'sg1': ['Krebbelche']}},
                         'genus': {'sg1': ['n']},
                         'nominativ': {'plural': {'pl1': ['Krebbelcher']},
                                       'singular': {'sg1': ['Krebbelche']}}},
        'spec_pre': {'akkusativ_pre': {'singular_pre': {'sg1': ['dat']}},
                     'dativ_pre': {'plural_pre': {'pl1': ['de']},
                                   'singular_pre': {'sg1': ['demm']}},
                     'genitiv_pre': {'plural_pre': {'pl1': ['von de']},
                                     'singular_pre': {'sg1': ['von demm']}},
                     'nominativ_pre': {'singular_pre': {'sg1': ['dat']}}}}}
```
    
The genitive singular form as specified on Wiktionary for *Krebbelche* is "von demm Krebbelche"; the value under `gen_case_num`>`genitiv`>`singular` is "Krebbelche", while "von demm" comes under `spec_pre`>`genitiv_pre`>`singular_pre`.


#### <a name="decltype"></a>-> `'decl_type'` for declension class
The feature `decl_type` shows if a noun belongs to a class of German nouns with special declension. This can currently happen in two cases: 
1. For nouns that have an  adjective-like declension
(e.g., [*Erwachsene*](https://de.wiktionary.org/wiki/Erwachsene#Substantiv,_f,_adjektivische_Deklination)). In this case, the value of `'decl_type'` is `['adj']` .
2. For nouns that typically designate languages and end in *-sch* (e.g., [*Lateinisch*](https://de.wiktionary.org/wiki/Lateinisch)).
 In this case, the value of `'decl_type'` is `['-sch']`.


#### <a name="tantum"></a>-> `'tantum'`
The value of the feature `tantum` indicates if the noun is used in that particular usage as a *singulare tantum* ("in singular number only") or a plurale tantum ("plural only"). For example, the noun [*Leute*](https://de.wiktionary.org/wiki/Leute) (*people*) has the characterisation `'tantum': 
['Pl']` because it is only used in the plural.  

#### <a name="specwordtype"></a>-> `'spec_word_type'` for non-common nouns

The `spec_word_type` feature indicates the type of a particular usage that the editors considered important, such as when the noun is a family name or a toponym, etc. The current list of special word types is as follows: 
Abkürzung (abbreviation), Toponym (toponym), Nachname (family name), Vorname (first name), Eigenname (proper name), Name (name), Straßenname (street name).

### <a name="dictionary-GermanAdjEntriesDict"></a>The basic structure of a `GermanAdjEntriesDict` dictionary

```
{
 <adj_headword>: 
	{'u<usage_#>': 
		{'deg_of_comp':
			{'positiv': [<form1>,],
			 'komparativ': [<form1>,],
			 'superlativ': [<form1>,],
			},
	 	 'spec_comp': ['no_am'|'no_other_forms',],
		 'decl_feat': ['no_comp'|'no_decl'],
		 'attr_pred': ['attr_only'|'pred_only'],
		},
	},
}
```

The `deg_of_comp` feature collects all degrees of comparison forms of the adjective specified explicitly in the Wiktionary, in particular, the positive (`positive`), the comparative (`komparativ`) and superlative (`superlativ`) forms.

The leaves under the `spec_comp` feature can be the following:
* `no_am`: indicating that 'am' is not to be used at the beginning of the superlative form.
* `no_other_forms`: indicating that the adjective has no degree of comparison forms other than that specified under `deg_of_comp`. 

The leaves under the `decl_feat` feature can be the following: 
* `no_comp`: indicating that adjectival usage is specified explicitly as having no comparative forms.
* `no_decl`: indicating that the adjectival usage is explicitly specified as having no inflected forms.

Finally, `attr_pred` can indicate if an adjectival usage is attributive-only (`attr_only`) or predicative-only (`pred_only`). 
Since this information is rare and in any case mostly given at lexeme-level in the Wiktionary (see, e.g., [_interessiert_](https://de.wiktionary.org/wiki/interessiert)), only a handful of adjectives carry this feature in the generated dictionary. 


### <a name="dictionary-German-TranslationDict"></a>The basic structure of a translation dictionary (`GermanNounTranslationDict` and `GermanAdjTranslationDict`)

```
{
 <headword>: 
	{'u<usage_#>': 
		{'translations':
			{'en': 
				{'m<lexeme_#>': [<EN-translation1>,]},
			},
		},
	},
}
```
Here is an example, the translation entry of [Hahn](https://de.wiktionary.org/wiki/Hahn):
```
{'u1': {'translations': {'en': {'m1': ['cock', 'rooster'],
                                'm2': ['cock'],
                                'm4': ['tap', 'valve'],
                                'm5': ['hammer']}}}}
```
The different 'm'-indices correspond to the different lexemes (meanings) in which the word can be used in a particular usage, where these meanings are represented by English translations. In the case of [*Hahn*](https://de.wiktionary.org/wiki/Hahn) there are five different meanings that this noun 
may express, but English translations for the 3rd one ("eine Wetterfahne") were omitted by the editors of Wiktionary.
  

## <a name="remarks"></a>Some remarks on the entries

* Even a cursory look at the regular expressions that we had to use shows that Wiktionary pages are not exactly easy to parse by a machine. Despite all the efforts of the editors of the German Wiktionary, in projects as big as this, errors are simply unavoidable. Fortunately, there are relatively 
few serious errors in the pages we have processed (at least in those parts of them that we were interested in). Our general policy was to ignore an error if it affects entries of the 0.01% magnitude relative to the size of the dictionary (i.e., less than a hundred entries). This means that a 
couple of entries might contain free-floating html tag fragments (like `<br`) entered by a less attentive human editor, etc. (See, e.g., the entry for [*Charlie*](https://de.wiktionary.org/wiki/Charlie).) 
But (to our best knowledge) there are only a handful of such items in the generated dictionaries and they can easily be corrected by hand if necessary.   

    A case in point: although only 'm' (male), 'n' (neutral) and 'f' (female) should occur as grammatical gender values, in a small number (in the 1 June 2018 version, 14) of the entries on Wiktionary, genus was specified *x* (e.g., [*Everglades*](https://de.wiktionary.org/wiki/Everglades)) or *pl* (e.g., [*Seschellen*](https://de.wiktionary.org/wiki/Seschellen)).

* A further small number of errors in the generated dictionary result from the automated scripts not being suitable for a fraction of the entries due to the entry's special nature. 
For example, while the algorithm for entering the last word in inflected noun forms under the relevant (e.g., genitive
singular) `gen_case_num` slot and the preceding string under the relevant `spec_pre` slot (see [description of `spec_pre` feature](#specpre)) works well for the vast majority of the cases, 
it fails in the case of one or two special words like the dialectal [*Teifi*](https://de.wiktionary.org/wiki/Teifi). 

* Finally, note that the handful of 1-character-long words (e.g., [A](https://de.wiktionary.org/wiki/A)) and, 
in the case of noun-related dictionaries, head words containing spaces (e.g., [Vereinigte Staaten](https://de.wiktionary.org/wiki/Vereinigte_Staaten)) are not included in the generated dictionaries. 
(The properties of multi-word nouns normally depend on their final noun anyway.)
