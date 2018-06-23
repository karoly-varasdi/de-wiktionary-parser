# Dokumentation über die Arten und die Struktur der Wörterbücher

* [Wörterbucharten](#dictionary-types)
* [Wörterbuchstruktur](#json-structure)
	* [Grundstruktur eines `GermanNounEntriesDict` Wörterbuchs (enthält grammatikalische Informationen)](#json-GermanNounEntriesDict)
	* [Grundstruktur eines `GermanNounEntriesTranslationDict` Wörterbuchs (enthält Übersetzungen)](#json-GermanNounEntriesTranslationDict)
* [Hinweise zu den Wörterbuch-Inhalten](#remarks)


## <a name="dictionary-types"></a>Wörterbucharten 
Wir haben drei Klassen definiert, die drei Wörterbucharten entsprechen: 
1. `GermanNounEntriesDict`: eine Art Wörterbuch, dessen Einträge grammatikalische (morphologische und verwendungsbezogene) Informationen des deutschen Wiktionary über deutsche Substantive enthalten.
2. `GermanNounEntriesTranslationDict`: eine Art Wörterbuch, dessen Einträge (vorerst nur englische) Übersetzungen deutscher Substantive enthalten, gegliedert nach Verwendungen und Lexemen.
3. `WordEntriesDict`: eine Oberklasse der beiden obenen Klassen. 

`GermanNounEntriesDict` und `GermanNounEntriesTranslationDict` Wörterbücher werden von Parser-Skripten generiert, die eine xml-Datei des deutschen Wiktionary parsen. 
Das Ergebnis der Parsing-Phase kann dann in das weit verbreitete JSON Format (siehe nächsten Abschnitt) exportiert (gespeichert) 
werden.

Neben der Möglichkeit, Wörterbücher zu generieren und zu speichern, gibt es Methoden und Funktionen, die diese Wörterbücher manipulieren, durchsuchen oder abbilden.      

## <a name="json-structure"></a>Wörterbuchstruktur 

Im Folgenden wird die Struktur der generierten Einträge beschrieben. Alle illustrativen Beispiele beziehen sich auf die *1 June 2018* Version des deutschen Wiktionary. 
Es kann also vorkommen, dass sie zu dem Zeitpunkt, an dem Sie diesen Text lesen, mittlerweile geändert wurden.
  
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

Alle Einträge sind nach hier als '**usage**' (**Verwendung**) bezeichnete Verwendungen gegliedert: diese entsprechen Überschriften der Ebene 3 im Wiktionary. Die Verwendungen stimmen nicht (unbedingt) mit Lexemen überein: zu einer Verwendung können mehrere Lexemen (Bedeutungen) gehören (s. 
z.B. 
'[Staat](https://de.wiktionary.org/wiki/Staat)'). Unterschiedliche spezielle Wortarten (worauf `spec_word_type` hinweist) benötigen aber ihre eigene Verwendungen (s. z.B. '[Hahn](https://de.wiktionary.org/wiki/Hahn)'), und dies gilt auch für dialektale Wörter, und für Fälle, in denen 
unterschiedliche 
Deklinationen unterschliedlichen Lexemen entsprechen (s. z.B. '[Reis](https://de.wiktionary.org/wiki/Reis#Reis_(Deutsch))').

Das Merkmal `'gen_case_num'` leitet Informationen ein, die sich auf das Geschlecht (`'genus'`) oder unterschliedliche deklinierte Formen beziehen. 
Freie Varianten werden zu einer Liste zusammengefasst. 
Z.B., die Genitiv-Singular-Form des Stichwortes 'Hahn' unter dessen ersten Verwendung ('u1') kann sowohl 'Hahns' als auch 'Hahnes' sein. 
 
Die `'sg'`- und `'pl'`-Ziffer legen eine Deklination fest (jeweils maximal vier). Wichtig zu beachten sind folgende Punkte:
1. Die 'sg#' und 'pl#' Bezeichner sind obligatorisch, und sie fangen stets mit '1' an (selbst wenn es keine anderen Dektlinationen gibt).
2. Obwohl alle Wortformen unter 'sg1' gehören zusammen, und ebenso die Formen unter 'sg2', usw., als auch die Formen unter 'pl1', usw., *es gibt keinerlei Verbindung zwischen den Indizes des Singulars und des Plurals*. 
Anders gesagt, es ist nicht der Fall, dass die Wortformen unter 'sg1' und 'pl1' gehören zusammen, aber nicht die Formen unter 'sg2' und 'pl1' oder 'sg1' und 'pl2'. Alle 'sg'-Deklinationen sollten mit allen 'pl'-Deklinationen unter derselben Verwendung kombinierbar sein.

<a name="specpre"></a>
Das Merkmal `'spec_pre'` taucht auf nur falls eine deklinierte Form mehrwörtig ist. In so einem Fall wird das letzte Wort unter `gen_case_num` eingetragen, 
während der Rest (der Anfangsteil) der mehrwörtigen deklinierten Form unter `spec_pre` eingetragen wird. 
('*_pre*' wird zu allen Merkmalnamen unter `spec_pre` hinzufügt.) 
Solche extra Wörter kommen typischerweise in dialektalen Wörtern wie [*Krebbelche*](https://de.wiktionary.org/wiki/Krebbelche) vor.
Die Genitiv-Singular-Form ist z.B. für dieses Stichwort als "_von demm Krebbelche_" im Wiktionary angegeben; der Wert unter `gen_case_num`>`genitiv`>`singular` ist also "_Krebbelche_", und "_von demm_" gehört unter `spec_pre`>`genitiv_pre`>`singular_pre`.

Schließlich zeigt das Merkmal `decl_type`, dass ein Substantiv in eine Klasse deutscher Substantive gehört, die speziell dekliniert werden. Insbesondere geht es hier um die adjektivische Deklination 
(in welchem Fall `decl_type` den Wert `['adj']` hat; s. z.B. '[Erwachsene](https://de.wiktionary.org/wiki/Erwachsene#Substantiv,_f,_adjektivische_Deklination)') 
und die -sch-Deklination (in welchem Fall `decl_type` den Wert `['-sch']` hat; s. z.B. '[Lateinisch](https://de.wiktionary.org/wiki/Lateinisch)').

Das Merkmal `tantum` weist darauf hin, dass die jeweilige Verwendung des Substantivs ein *Singularetantum* ("nur Singular") oder ein *Pluraletantum*  ("nur Plural") ist. Z.B. hat das Wort ['Leute'](https://de.wikipedia.org/wiki/Leute) die Spezifikation 
`'tantum': ['Pl']`, da es ausschließlich im Plural verwendet wird.

Das Merkmal `spec_word_type` weist auf eine spezielle Wortart hin, z.B. wenn ein Substantiv als Nachname oder Toponym verwendet wird.

### <a name="json-GermanNounEntriesTranslationDict"></a>Grundstruktur eines `GermanNounEntriesTranslationDict` Wörterbuchs (enthält Übersetzungen):

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
Als Beispiel, der Eintrag für ['Hahn'](https://de.wiktionary.org/wiki/Hahn) im generierten Übersetzungswörterbuch ist folgendes:
```
{'u1': {'translations': {'en': {'m1': ['cock', 'rooster'],
                                'm2': ['cock'],
                                'm4': ['tap', 'valve'],
                                'm5': ['hammer']}}}}
```
Die unterschiedlichen `m`-Indizes entsprechen unterschiedlichen Lexemen (Bedeutungen) der jeweiligen Verwendung ('usage'). Das Wort 'Hahn' (oder besser gesagt, dessen erste Verwendung) hat fünf unterschiedliche Bedeutungen, aber keine englische Übersetzungen wurden für die dritte Bedeutung
("eine Wetterfahne") von den Beiträgern vom Wiktionary eingetragen.

## <a name="remarks"></a>Hinweise zu den Wörterbuch-Inhalten

* Stichwörter (Lemmas), die Leerzeichen enthalten (z.B. [Vereinigte Staaten](https://de.wiktionary.org/wiki/Vereinigte_Staaten)) und Wörter, die ein Zeichen lang sind (z.B. [A](https://de.wiktionary.org/wiki/A)) werden **nicht** in die generierten Wörterbücher eingetragen.

* Schon ein flüchtiger Blick an die regulären Ausdrücke, die wir verwenden mussten, zeigt, dass das automatische Parsen von Wiktionary-Seiten nicht gerade einfach ist. Trotz aller Bemühungen der Redakteure des deutschen Wiktionary sind Fehler in so großen Projekten unvermeidbar. 
Zum Glück gibt es relativ wenige schwerwiegende Fehler in den Seiten, die wir verarbeitet haben (zumindest in den Teilen woran wir uns interessierten).
Grundsätzlich ignorierten wir Fehler, die Einträge in der 0,01% Größenordnung (d.h., weniger als cca. ein hundert Einträge) betreffen. Dies bedeutet, dass einige Einträge z.B. HTML-Tag-Fragmente (wie etwa "<br") enthalten können, die weniger aufmerkasame Beiträger in den Text aus Versehen 
eingegeben haben.
(Siehe, z.B., der Eintrag [*Charlie*](https://de.wiktionary.org/wiki/Charlie).)   Es gibt aber (nach unserem besten Wissen) lediglich eine kleine Menge solcher Einträge in den generierten Wörterbücher, und sie können, falls nötig, auch manuell korrigiert werden.

    Ein Beispiel: obwohl nur 'm' (Maskulinum), 'n' (Neutrum) und 'f' (Femininum) as Genus-Werte vorkommen sollten, in einer Handvoll (im 1 Juni 2018 Version, 14) der Einträge im Wiktionary wurden 
    *x* (z.B. [Everglades](https://de.wiktionary.org/wiki/Everglades)) oder 
    *pl* (z.B. [Seschellen](https://de.wiktionary.org/wiki/Seschellen)) als Genus eingetragen.

* Eine weitere kleine Menge Fehler stammen aus den automatischen Skripten, die für eine kleine Minderheit der Einträge nicht geeignet sind.
Zum Beispiel ist das Algorithmus für mehrwörtige deklinierte Forme (siehe [Beschreibeung des Merkmals `spec_pre`](#specpre)) problematisch in ein Paar speziellen Fällen, siehe z.B. das dialektale Wort [Teifi](https://de.wiktionary.org/wiki/Teifi). 
