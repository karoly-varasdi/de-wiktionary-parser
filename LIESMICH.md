# Deutscher Wiktionary xml Parser
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Ein Python-Programm für das Parsen von einer [.xml Datei des deutschen Wiktionary](https://dumps.wikimedia.org/dewiktionary), mit der Möglichkeit, die Ergebnisse in eine .json Datei zu exportieren.

Die aktuelle Version kann ausgewählte Merkmale deutscher Substantive (wie etwa Informationen über Geschlecht, Deklination, spezielle Wortarten) und Adjektive (hauptsächlich die gesteigerten Formen), sowie die englische Übersetzung deutscher Substantive, Abkürzungen und Adjektive extrahieren.

## Inhaltsverzeichnis

* [Die Ressourcen](#resources)
* [Wörterbucharten](#dictionary-types)
* [Wörterbuchstruktur](#json-structure)
	* [Grundstruktur eines `GermanNounEntriesDict` Wörterbuchs (enthält grammatikalische Informationen über Substantive)](#json-GermanNounEntriesDict)
	* [Grundstruktur eines `GermanAdjEntriesDict` Wörterbuchs (enthält grammatikalische Informationen über Adjektive)](#json-GermanAdjEntriesDict)
	* [Grundstruktur eines Übersetzungswörterbuchs (`GermanNounTranslationDict` und `GermanAdjTranslationDict`)](#json-German-TranslationDict)
* [Hinweise zu den Wörterbuch-Inhalten](#remarks)
* [Installation](#installation)
* [Ein Musterskript](#sample)
* [Autoren und Lizenz](#authors-and-license)

## <a name="resources"></a>Die Ressourcen
In diesem Paket befinden sich zwei Ressourcen: 
1. die Wörterbuch-Dateien (JSON) unter dem **[data](./data/)** Ordner;
2. die Python-Skripte unter dem **[src](./src/)** Ordner, mit denen diese Wörterbücher generiert wurden.

Falls Sie nur die Wörterbücher brauchen, die wir vom Wiktionary .xml generiert haben, *dann brauchen Sie das Python-Paket nicht zu installieren*: 
nehmen Sie einfach das Wörterbuch aus dem **[data](./data/)** Ordner, das Sie brauchen. (Siehe [LIESMICH](./data/LIESMICH.md) im **data** Ordner für eine Beschreibung der Wörterbücher im Ordner.) 

Nur falls Sie selbst die Wörterbücher generieren möchten, oder mit dem Skript experimentieren möchten, müssen Sie das Python-Paket [installieren](#installation).

Für eine detaillierte Dokumentation, siehe bitte die folgenden Dateien im *[docs](./docs/)* Ordner:
1. Die Dokumentationsdateien [**hilfe_worterbucher.md**](./docs/hilfe_worterbucher.md) (auf Deutsch) und [**help_dictionaries.md**](./docs/help_dictionaries.md) (auf Englisch) beschreiben die Wörterbücher und deren Struktur.
2. Die englisch-sprachige Dokumentationsdatei [**help_python_modules.md**](./docs/help_python_modules.md) beschreibt die Funktionalitäten der Python-Module.


## <a name="dictionary-types"></a>Wörterbucharten 
Wir haben unterschiedliche Klassen von Wörterbücher definiert, die unterschiedlichen Wörterbucharten entsprechen:
1. Substantiv-bezogene Wörterbücher:
    1. `GermanNounEntriesDict`: eine Art Wörterbuch, dessen Einträge grammatikalische (morphologische und verwendungsbezogene) Informationen über deutsche Substantive aus dem deutschen Wiktionary enthalten.
    2. `GermanNounTranslationDict`: eine Art Wörterbuch, dessen Einträge (vorerst nur englische) Übersetzungen deutscher Substantive enthalten, gegliedert nach Verwendungen und Lexemen.
    
2. Adjektiv-bezogene Wörterbücher:
    1. `GermanAdjEntriesDict`: eine Art Wörterbuch, dessen Einträge grammatikalische Informationen (hauptsächlich über gesteigerte Formen) über deutsche Adjektive aus dem deutschen Wiktionary enthalten.
    2. `GermanAdjTranslationDict`: eine Art Wörterbuch, dessen Einträge (vorerst nur englische) Übersetzungen deutscher Adjektive enthalten, gegliedert nach Verwendungen und Lexemen.
    
3. `WordEntriesDict`: eine Oberklasse der obenen Klassen. 

Die Wörterbücher werden von Parser-Skripten mit Informationen aufgeladen, die eine xml-Datei des deutschen Wiktionary parsen. 
Das Ergebnis der Parsing-Phase kann dann in das weit verbreitete JSON Format exportiert (gespeichert) werden.

Neben der Möglichkeit, Wörterbücher zu generieren und zu speichern, gibt es Methoden und Funktionen, die diese Wörterbücher manipulieren, durchsuchen oder abbilden.  

## <a name="json-structure"></a>Wörterbuchstruktur 

Im Folgenden wird die Struktur der generierten Einträge beschrieben. Für eine etwas mehr detaillierte Beschreibung, 
s. die Dokumentationsdatei [*hilfe_worterbucher.md*](./docs/hilfe_worterbucher.md) (auf Deutsch) oder [*help_dictionaries.md*](./docs/help_dictionaries.md) (auf Englisch) im *docs* Ordner.
  
### <a name="json-GermanNounEntriesDict"></a>Grundstruktur eines `GermanNounEntriesDict` Wörterbuchs (enthält grammatikalische Informationen):

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

### <a name="json-GermanAdjEntriesDict"></a>Grundstruktur eines `GermanAdjEntriesDict` Wörterbuchs (enthält grammatikalische Informationen über Adjektive):

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

### <a name="json-GermanNounTranslationDict"></a>Grundstruktur eines Übersetzungswörterbuchs (`GermanNounTranslationDict` und `GermanAdjTranslationDict`):

```
{
 <noun_headword>: 
	{'u<usage_#>': 
		{'translations':
			{'en': 
				{'m<lexeme_#>': [<EN-translation1>,]},
			},
		},
	},
}
```


## <a name="remarks"></a>Hinweise zu den Wörterbuch-Inhalten

* Substantive, die ein Leerzeichen enthalten (z.B. [Vereinigte Staaten](https://de.wiktionary.org/wiki/Vereinigte_Staaten)) und Wörter, die ein Zeichen lang sind (z.B. [A](https://de.wiktionary.org/wiki/A)) werden **nicht** in die generierten Wörterbücher eingetragen.

* Schon ein flüchtiger Blick an die regulären Ausdrücke, die wir verwenden mussten, zeigt, dass das automatische Parsen von Wiktionary-Seiten nicht gerade einfach ist. Trotz aller Bemühungen der Redakteure des deutschen Wiktionary sind Fehler in so großen Projekten unvermeidbar. 
Zum Glück gibt es relativ wenige schwerwiegende Fehler in den Seiten, die wir verarbeitet haben (zumindest in den Teilen woran wir uns interessierten).
Grundsätzlich ignorierten wir Fehler, die Einträge in der 0,01% Größenordnung (d.h., weniger als cca. ein hundert Einträge) betreffen. Dies bedeutet, dass einige Einträge z.B. HTML-Tag-Fragmente (wie etwa "<br") enthalten können, die weniger aufmerkasame Beiträger in den Text aus Versehen 
eingegeben haben.
(Siehe, z.B., der Eintrag [*Charlie*](https://de.wiktionary.org/wiki/Charlie).)   Es gibt aber (nach unserem besten Wissen) lediglich eine kleine Menge solcher Einträge in den generierten Wörterbücher, und sie können, falls nötig, auch manuell korrigiert werden.

* Eine weitere kleine Menge Fehler stammen aus den automatischen Skripten, die für eine kleine Minderheit der Einträge nicht geeignet sind.
Zum Beispiel ist das Algorithmus für mehrwörtige deklinierte Forme der Substantive 
(siehe [Beschreibeung des Merkmals `spec_pre` im Dokumentation](./docs/hilfe_worterbucher.md#specpre)) problematisch in ein Paar speziellen Fällen, 
siehe z.B. das dialektale Wort [Teifi](https://de.wiktionary.org/wiki/Teifi). 

## <a name="installation"></a>Installation

Um dewiktionaryparser zu installieren, navigieren Sie zum **[dist](./dist/)** Ordner dieses Pakets und geben Sie folgenden Befehl in Ihr Terminalfenster ein (wo `TAR-GZ-DATEI` ist der Dateiname der .tar.gz Datei, z.B., `dewiktionaryparser-1.0.tar.gz`):

`pip install TAR-GZ-DATEI`

Bitte beachten Sie, dass eine Version von  [**Python 3**](https://www.python.org/downloads/) zuvor auf Ihrem Recnher installiert werden muss.  (Die Skripte wurden bisher auf Python 3.5 und 3.6 in einer Windows-Umgebung getestet.)

## <a name="sample"></a>Ein Musterskript
Für eine detaillierte Beschreibung der Nutzung der Python-Module siehe die englisch-sprachige Dokumentationsdatei [*help_python_modules.md*](./docs/help_python_modules.md) im *docs* Ordner.

Das folgende Skript generiert und speichert jeweils ein Wörterbuch deutscher Substantive mit grammatikalischer Informationen und ein Wörterbuch mit 
(englischen) Übersetzungen, und dann erweitert ersteres mit Informationen aus letzteres. 


```python
# Parser-Modul importieren:
import dewiktionaryparser as dw

#################################################################################
# Wörterbuch mit grammatikalischen Informationen aus einer xml-Datei generieren #
#################################################################################

# Wörterbuch grammatikalischer Informationen initialisieren:
word_entries = dw.GermanNounEntriesDict()

# Einträge generieren aus dewiktionary-20180601-pages-meta-current.xml im "data" Ordner des aktuellen Arbeitsverzeichnisses:
word_entries.generate_entries('.\data\dewiktionary-20180601-pages-meta-current.xml')

# Wörterbuch speichern im "data" Ordner des aktuellen Arbeitsverzeichnisses:
word_entries.export_to_json('.\data\de_noun_entries.json')


################################################################
# Wörterbuch mit Übersetzungen aus einer xml-Datei generieren #
################################################################

# Wörterbuch für Übersetzungen initialisieren:
translations = dw.GermanNounTranslationDict()

# Einträge generieren aus dewiktionary-20180601-pages-meta-current.xml im "data" Ordner des aktuellen Arbeitsverzeichnisses:
translations.generate_translations('.\data\dewiktionary-20180601-pages-meta-current.xml')

# Wörterbuch speichern im "data" Ordner des aktuellen Arbeitsverzeichnisses:
translations.export_to_json('.\data\de_noun_translations.json')


###########################################################################
# Wörterbuch grammatikalischer Informationen mit Übersetzungen erweitern  #
###########################################################################

word_entries.enhance_usages(translations)

# Kombiniertes Wörterbuch speichern im "data" Ordner des aktuellen Arbeitsverzeichnisses:
word_entries.export_to_json('.\data\de_noun_entries_with_translations.json')
```

Für Beispiele siehe auch das Skript **[sample_script.py](./src/sample_script.py)** unter dem Ordner *src*.

## <a name="authors-and-license"></a>Autoren und Lizenz

### Das Programm

Copyright (C) 2018 Zsófia Gyarmathy und Károly Varasdi

    Dieses Programm ist freie Software. Sie können es unter den Bedingungen der 
    GNU General Public License, wie von der Free Software Foundation veröffentlicht, 
    weitergeben und/oder modifizieren, entweder gemäß Version 3 der Lizenz oder 
    (nach Ihrer Option) jeder späteren Version.

    Die Veröffentlichung dieses Programms erfolgt in der Hoffnung, daß es Ihnen von 
    Nutzen sein wird, aber OHNE IRGENDEINE GARANTIE, sogar ohne die implizite Garantie 
    der MARKTREIFE oder der VERWENDBARKEIT FÜR EINEN BESTIMMTEN ZWECK. 
    Details finden Sie in der GNU General Public License.

    Sie sollten ein Exemplar der GNU General Public License zusammen mit diesem 
    Programm erhalten haben. Falls nicht, siehe <http://www.gnu.org/licenses/>.

### Wiktionary-Daten

Die Daten aus Wiktionary (https://de.wiktionary.org/) stehen unter der Dual-Lizenz von Creative Commons Namensnennung-Weitergabe unter gleichen Bedingungen 3.0 Unported (CC-BY-SA) und GNU Free Documentation License (GFDL).

 * Für den vollen Text von CC BY-SA, siehe [LICENSE-CC-BY-SA](./data/LICENSE-CC-BY-SA) (auf Englisch) im "data" Ordner oder besuchen Sie <https://creativecommons.org/licenses/by-sa/3.0/deed.de>
 * Für den vollen Text von GFDL, siehe [LICENSE-GFDL](./data/LICENSE-GFDL) (auf Englisch) im "data" Ordner oder besuchen Sie <https://www.gnu.org/copyleft/fdl.html>
 
