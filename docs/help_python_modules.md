# Documentation on the Python modules of the package

* [Installation](#installation)
* [The modules](#modules)
* [Populating dictionaries](#populate-dictionaries)
	* [Grammatical information dictionaries](#usage-grammatical)
	    * [Parsing a German wiktionary xml and creating a dictionary with grammatical information](#grammatical-generate)
	    * [Loading information saved in a .json file](#grammatical-load)
	* [Translation dictionaries](#usage-translation)
	    * [Parsing a German wiktionary xml and creating a dictionary with translation information](#translation-generate)
	    * [Loading information saved in a .json file](#translation-load)
* [Displaying the information in the dictionary entries](#display-info)
* [Some dictionary manipulation options](#dict-manipulation)
    * [Enhancing a grammatical dictionary with translation information](#enhance-dict)
    * [Creating an inverse dictionary](#inverse-dict)
    * [Creating a grammatical information dictionary containing common nouns only](#commons-dict)
* [Exploring the dictionaries](#explore)


## <a name="installation"></a>Installation

To install dewiktionaryparser, navigate to the **[dist](./dist/)** directory of this package and run the following command in your terminal:

`pip install dewiktionaryparser-1.0.tar.gz`

Note that you need to have a version of [**Python 3**](https://www.python.org/downloads/) installed on your computer.  (The scripts have been tested on Python 3.5 and 3.6 in a Windows environment.)

## <a name="modules"></a>The modules

The package consists of four modules, all of which are initiated when the package is imported.

1. `common_defs.py` is a collection of functions and variables (regexes, for the most part) that are used by most or all of the modules. 
The most general `WordEntriesDict` class is also defined here along with its basic methods for exporting to and importing from a .json file, 
for making inverse dictionaries and for enhancing entry usages with information from another dictionary. Basic displaying methods (`word_entry(<entry:str>)`, `printsorted(from:int, to:int)`) are also defined.

2. `de_wikt_noun_info_parser.py` includes the definition of the `GermanNounEntries` class along with its methods (and regexes) for extracting grammatical information from wiktionary xml files. The class-specific `make_inv_dict()` and `make_commons_dict` methods are also defined.

3. `de_wikt_noun_translations.py` includes the definition of the `GermanNounTranslationDict` class along with its methods (and regexes) for extracting translation information from wiktionary xml files. The class-specific `make_inv_dict()` is likewise defined.

4. `explore.py` contains functions useful in exploring the generated dictionaries.

In what follows, the above functionalities are described in more detail.
For some sample usages, see also the **[sample_script.py](./src/sample_script.py)** script in the src directory.


## <a name="populate-dictionaries"></a>Populating dictionaries

This section describes the basic methods and functions for generating, exporting and importing dictionaries.


### <a name="usage-grammatical"></a>Grammatical information dictionaries

#### <a name="grammatical-generate">Parsing a German wiktionary xml and creating a dictionary with grammatical information
 * Initialize an instance of the `GermanNounEntriesDict` class (which is a dict subclass via its parent class `WordEntriesDict`).
    
 * To populate this dictionary with information from a German wiktionary xml file, call the `generate_entries()` method on it with  `file_path=<path-to-xml-file>` as its argument (if `<path-to-xml-file>` is the first argument, no `file_path` keyword is necessary).
    
 * To save a `GermanNounEntriesDict` dictionary to a .json file, call the `export_to_json()` method on it, with the argument `file_path=<path-to-new-json-file>` and the optional argument `encoding` (default value: 'utf-8').
 
#### <a name="grammatical-load">Loading information saved in a .json file
 * Initialize an instance of the `GermanNounEntriesDict` class, or its parent, `WordEntriesDict` class (which is a dict subclass).
    
 * To populate a `GermanNounEntriesDict` object with information from a .json file, call the `retrieve_from_json()` method with the argument `file_path=<path-to-existing-json-file>` and the optional arguments `encoding` (default: 'utf-8') and `clear_dict` (default: `True`) to specify the source file path, the encoding and if the `GermanNounEntriesDict` dictionary should be cleared first. 
 
    By specifying the optional argument `clear_dict=False` (instead of the default `True`), the `GermanNounEntriesDict` dictionary is *not* cleared before populating it with the information (this is only relevant if it was populated with information earlier on in the session). In this case entries already present will be silently overwritten by the ones loaded if they are in conflict, but the rest will be left untouched.

### <a name="usage-translation"></a>Translation dictionaries

#### <a name="translation-generate">Parsing a German wiktionary xml and creating a dictionary with translation information
 * Initialize an instance of the `GermanNounEntriesTranslationDict` class (which is a dict subclass via its parent class `WordEntriesDict`).
    
 * To populate this dictionary with information from a German wiktionary xml file, call the `generate_translations()` method on it with  `file_path=<path-to-xml-file>` as its argument (if `<path-to-xml-file>` is the first argument, no `file_path` keyword is necessary).
    * An optional argument of `generate_translations` is called `strict`, whose default value is `False`. 
    If you set this to any non-False value (e.g., `strict=True`), then translations will be generated by a **strict, non-greedy** algorithm, meaning that only translations within wiktionary translations tags (`{{Ü|...}}`) will be included.
    
        Using `strict=True` no superfluous explanatory texts will be included in the translations. A case in point is [Bratkartoffelverhältnis](https://de.wiktionary.org/wiki/Bratkartoffelverhältnis), where the explanation "_idiomat.: Er hat ein Bratkartoffelverhältnis mit ihr engl.:_" was incorrectly not italicized in the source as per the Wiktionary guidelines: as a result this chunk of text gets included in the generated translation value using the default `strict=False`. In contrast, using `strict=True` would only include "_meal ticket_" in its translations.
        However, translation information also gets lost with the strict algorithm sometimes, e.g., a correct translation of [Staat](https://de.wiktionary.org/wiki/Staat) is "_insect society, colony_", but only "_colony_" is included by using `strict=True`.
            
 * To save a `GermanNounEntriesTranslationDict` dictionary to a .json file, call the `export_to_json()` method on it, with the argument `file_path=<path-to-new-json-file>` and the optional argument `encoding` (default value: 'utf-8').
 
#### <a name="translation-load">Loading information saved in a .json file
 * Initialize an instance of the `GermanNounEntriesTranslationDict` class, or its parent, `WordEntriesDict` class (which is a dict subclass).
    
 * To populate a `GermanNounEntriesTranslationDict` object with information from a .json file, call the `retrieve_from_json()` method with the argument `file_path=<path-to-existing-json-file>` and the optional arguments `encoding` (default: 'utf-8') and `clear_dict` (default: `True`) to specify the source file path, the encoding and if the `GermanNounEntriesTranslationDict` dictionary should be cleared first. 
    
    By specifying the optional argument `clear_dict=False` (instead of the default `True`), the `GermanNounEntriesTranslationDict` dictionary is *not* cleared before populating it with the information (this is only relevant if it was populated with information earlier on in the session).

## <a name="display-info"></a>Displaying the information in the dictionary entries
The German words extracted from the German wiktionary are organized into entries which, in turn, are simple Python dictionaries. To view any entry in a dictionary that you named, say, `word_entries`, you may use the syntax `word_entries[<noun>]` as in `word_entries['Hahn']`, or you can use the more user-friendly `word_entry()` method as in `word_entries.word_entry('Hahn')` which pretty-prints the entry related to the word [*Hahn*](https://de.wiktionary.org/wiki/Hahn). 

If you want to peek into your dictionary without having a specific entry in mind, you can call the `printsorted` method on it as `word_entries.printsorted(m, n)`, which pretty-prints entries between indexes m and n from the alphabetically sorted dictionary. (The default values for m and n are 0 and 10, respectively.)

## <a name="dict-manipulation"></a>Some dictionary manipulation options
### <a name="enhance-dict"></a>Enhancing a grammatical dictionary with translation information
The following is a way to *combine* the grammatical information with the respective translations into one single dictionary.
```python
# word_entries is your grammatical information dictionary; translations is your translation dictionary

# enhance grammatical dictionary with translation information  #
word_entries.enhance_usages(translations)

# save the resulting dictionary under the data folder of the current working dictionary:
word_entries.export_to_json('.\data\de_noun_entries_with_translations.json')

'''
The enhanced dictionary "word_entries" now contains both grammatical and translation information. 
E.g., the value for "Mutter" in word_entries is now:

{'u1': {'gen_case_num': {'akkusativ': {'plural': {'pl1': ['Mütter']},
                                       'singular': {'sg1': ['Mutter']}},
                         'dativ': {'plural': {'pl1': ['Müttern']},
                                   'singular': {'sg1': ['Mutter']}},
                         'genitiv': {'plural': {'pl1': ['Mütter']},
                                     'singular': {'sg1': ['Mutter']}},
                         'genus': {'sg1': ['f']},
                         'nominativ': {'plural': {'pl1': ['Mütter']},
                                       'singular': {'sg1': ['Mutter']}}},
        'translations': {'en': {'m1': ['mother']}}},
 'u2': {'gen_case_num': {'akkusativ': {'plural': {'pl1': ['Muttern']},
                                       'singular': {'sg1': ['Mutter']}},
                         'dativ': {'plural': {'pl1': ['Muttern']},
                                   'singular': {'sg1': ['Mutter']}},
                         'genitiv': {'plural': {'pl1': ['Muttern']},
                                     'singular': {'sg1': ['Mutter']}},
                         'genus': {'sg1': ['f']},
                         'nominativ': {'plural': {'pl1': ['Muttern']},
                                       'singular': {'sg1': ['Mutter']}}},
        'translations': {'en': {'m1': ['nut']}}},
 'u3': {'gen_case_num': {'akkusativ': {'plural': {'pl1': []},
                                       'singular': {'sg1': ['Muttern']}},
                         'dativ': {'plural': {'pl1': []},
                                   'singular': {'sg1': ['Muttern']}},
                         'genitiv': {'plural': {'pl1': []},
                                     'singular': {'sg1': ['Mutters']}},
                         'genus': {'sg1': ['f']},
                         'nominativ': {'plural': {'pl1': []},
                                       'singular': {'sg1': ['Mutter']}}},
        'spec_word_type': ['Eigenname'],
        'tantum': ['Sg']}}
'''
```

### <a name="inverse-dict"></a>Creating an inverse dictionary
The grammatical dictionary maps nouns to various information, including the inflected forms associated with the head word. The information in the grammatical dictionary, however, makes it possible to solve the inverse task as well, that of finding the base word form given an inflected form. An inverse dictionary is a dictionary which reduces this task to a simple look-up, which speeds up the search for the base word remarkably. An inverse dictionary can also be generated for translations, if needed.       

Note that in order to correctly select the leaves of the original dictionary to be included as keys of the inverse dictionary, grammatical dictionaries must be of type `GermanNounEntriesDict` and translation dictionaries of type `GermanNounTranslationDict`. 
Alternatively, you can explicitly specify an `exclude` and/or an `include` keyword argument (both take lists of feature strings as values) to the `make_inv_dict` method: leaves of a branch containing *any* of the `exclude` features are disregarded, as are leaves of a branch containing *none* of 
the `include` features, when creating the inverse dictionary. 

For example, the default arguments of `make_inv_dict()` on a `GermanNounEntriesDict` object are `exclude=['genus'], include=['gen_case_num']` in order to avoid having 'f', 'm' or 'n' among the keys of the inverse dictionary (the *exclude* part) 
as well as to include only the word forms under the genus-case-number features (the *include* part).
The default arguments of `make_inv_dict()` on a `GermanNounTranslationDict` object are `exclude=[], include=['translations']` to include only translation leaves. 
By contrast, the method has empty lists as default exclude/include arguments on a generic `WordEntriesDict` object, and as a result, *all* leaves are included as keys in the resulting inverse dictionary by default.

```python
# word_entries is your grammatical information dictionary of type GermanNounEntriesDict

# create inverse dictionary for grammatical information dictionary:
inv_dic = word_entries.make_inv_dict()
# save the resulting dictionary under the data folder of the current working dictionary:
inv_dic.export_to_json('.\data\de_noun_entries_inv.json')

'''
inv_dic now contains inflected forms as keys and base form lists as values. 

E.g., the value for "Mais" in inv_dic is:
['Mai', 'Mais']
'''

# translations is your translation information dictionary of type GermanNounTranslationDict

# create inverse dictionary for translation information dictionary:
inv_dic_translations = translations.make_inv_dict()
# save the resulting dictionary under the data folder of the current working dictionary:
inv_dic_translations.export_to_json('.\data\de_noun_translations_inv.json')

'''
inv_dic_translations now contains English nouns as keys and lists of its German translations as values. 

E.g., the value for "table" in inv_dic_translations is:
['Tafel', 'Datenbanktabelle', 'Tabelle', 'Tisch', 'Tischlein']
'''
```
### <a name="commons-dict"></a>Creating a grammatical information dictionary containing common nouns only
A `GermanNounEntriesDict` dictionary generated from the Wiktionary pages contains thousands of place names (*Toponym*), family and first names (*Nachname* and *Vorname*), etc. 
If you are only interested in German **common nouns**, the `make_commons_dict()` method will generate a subdictionary that only contains such nouns.  

NOTE: the `make_commons_dict()` method is defined ONLY for `GermanNounEntriesDict` objects! 
If you initiated your dictionary as a `WordEntriesDict` or `GermanNounTranslationDict` object (e.g., when populating it from an existing .json dictionary), 
Python will throw an **AttributeError** exception.
Force your object into a `GermanNounEntriesDict` type in this case before attempting to use this method. 
(Note: non-common nouns will still only be filtered out if the special dictionary entries contain the `spec_word_type` feature, which is not the case in translation-only dictionaries!)

```python
# word_entries is your grammatical information dictionary of type GermanNounEntriesDict.

# create a subdictionary containing only common noun usages (i.e., no usages with "spec_word_type" -- special word type -- feature defined):
commons = word_entries.make_commons_dict()

# save the common nouns-only dictionary:
commons.export_to_json('.\data\de_common_nouns.json')
```

## <a name="explore"></a>Exploring the dictionaries
We have also defined a couple of auxiliary functions to explore the generated dictionary with, which are imported from the module `explore.py`. Here are some examples (we are assuming in the examples that the main grammatical information dictionary is called `word_entries` and the *dewiktionary* module 
has been imported as `dw`).

Suppose we want to know what kind of values there are in the dictionary under the keyword `'spec_word_type'`. We can find them interactively by using the `leaves_under_keyword()` function which collects all the leaves under an arbitrary keyword in the dictionary:
```python
dw.leaves_under_keyword(word_entries, 'spec_word_type')
# Out: {'Nachname', 'Vorname', 'Straßenname', 'Toponym', 'Abkürzung', 'Eigenname'}
```
Having found out that these features make up the possible values for `'spec_word_type'` in the dictionary, we might want to know *exactly which entries* have the `'Nachname'` (surname) feature. We can find them by typing the following at the prompt: 
```python
surnames = dw.find_entries_by_keyword_value(word_entries, spec_word_type='Nachname')
``` 
The set `surnames` now includes all surnames, such as 'Müller', 'Nielsen', etc.

By specifying more key-value pairs, we can collect entries that have *all* of the specified key-value pairs in their tree (*anywhere* within the entry, i.e., one key-value pair may occur in a different usage than another pair). 
Thus, beware that the following does **not** collect those surnames that are neuters:
```python
nachname_and_n_in_entry = dw.find_entries_by_keyword_value(word_entries, spec_word_type='Nachname', genus='n')
```  
Instead, `nachname_and_n_in_entry` is a set of word entries that have (under at least one usage) a surname special word type specification, and (under at least one usage, *though not necessarily the same one*) a neuter gender specification; e.g., [Celsius](https://de.wiktionary.org/wiki/Celsius).

Note also that the `find_entries_by_keyword_value` method returns a subset of the *keys* of its dictionary argument, those of `word_entries` in this case. If you want to have the subset of the *dictionary* itself (i.e., of `word_entries`) that the keys in `surnames` define, 
you will have to collect them in a dictionary separately by typing, e.g.: 
```python
surnames_dict = {w:word_entries[w] for w in surnames}
```

In general, `find_entries_by_keyword_value` accepts several comma-separated keyword-value pairs, and retrieves all the entries (keys) in the dictionary that have all those keywords with the specified values. Note that `find_entries_by_keyword_value` is liberal in the sense that it collects an entry if the entry has *at least* one occurrence of the given value. Therefore 
```python
has_fem = dw.find_entries_by_keyword_value(word_entries, genus='f')
```
will collect all the words that *have* a feminine gender ('genus' in the linguistic terminology used in the German wiktionary) and perhaps other gender values as well. Most of the family names are associated with at least two gender values (feminine and masculine), so they will also be included in `has_fem` above. 

Suppose now we want to know how many and which *common nouns* have feminine gender (and no other genders) in the dictionary. First, we need to generate the appropriate common nouns dictionary as follows:
```python
commons = word_entries.make_commons_dict()
``` 
Using this common nouns dictionary as in  
```python
common_noun_has_fem = dw.find_entries_by_keyword_value(commons, genus='f')
```
is one step closer to our goal, but it will still contain (common) nouns that have at least one gender beside feminine, like the noun [*Joghurt*](https://de.wiktionary.org/wiki/Joghurt) as shown by
```python
dw.leaves_under_keyword(commons['Joghurt'], 'genus')
# Out: {'n', 'f', 'm'}
```
In order to find those entries in `commons` that have *precisely one* gender, we can use Python's comprehension mechanism for creating an appropriate dictionary:
```python
prec_one_genus = {w:commons[w] for w in commons if len(dw.leaves_under_keyword(commons[w], 'genus')) == 1}
``` 
And, finally, we can filter this dictionary `prec_one_genus` to find those common nouns that only have feminine gender, and count their number:  
```python
has_fem_only = dw.find_entries_by_keyword_value(prec_one_genus, genus='f')
len(has_fem_only)
# Out: 28108
```
