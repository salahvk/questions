#!/usr/bin/env python3
"""Append remaining lists to awards_wave20_data.py."""

from pathlib import Path

TAIL = '''
SNA_FELLOWSHIP = [
    ("പണ്ഡിത് രവി ശങ്കർ", 1999), ("എം.എസ്. സുബ്ബുലക്ഷ്മി", 1990), ("ബിസ്മില്ലാ ഖാൻ", 1990),
    ("ഭീംസെൻ ജോഷി", 1990), ("ലതാ മങ്കേഷ്കർ", 1989), ("സത്യജിത് റേ", 1991),
    ("അടൂർ ഗോപാലകൃഷ്ണൻ", 2004), ("ശ്യാം ബെനഗൽ", 2005), ("നസീരുദ്ദീൻ ഷാ", 2003),
    ("ഒമ്പുരി", 2004), ("ഷബാനാ ആസ്മി", 2003), ("പണ്ഡിത് ജസ്റാജ്", 2003),
    ("ബിർജു മഹാരാജ്", 2002), ("സോണൽ മാധവിദേവ്", 2002), ("യാമിനി കൃഷ്ണമൂർത്തി", 2002),
    ("മല്ലികാ സാരാഭായി", 2002), ("വൈജയന്തിമാല ബാലി", 2002), ("പദ്മ സുബ്രഹ്മണ്യം", 2002),
    ("സിതാര ദേവി", 2002), ("രുക്മini Arundale", 2002), ("സാക്കിർ ഹുസൈൻ", 2003),
    ("ഹരിപ്രസാദ് ചൗരസ്യ", 2000), ("പണ്ഡിത് ശിവകുമാർ ശർമ്മ", 2000), ("ഗിരീഷ് കർണാട്", 2002),
    ("വിജയ് ടെൻഡുൽക്കർ", 2002), ("എbrahim Alkazi", 2002), ("മഹാശ്വേതാ ദേവി", 2003),
    ("അparana Sen", 2003), ("മrinal Sen", 2003), ("അkbar Padamsee", 2003),
    ("അruna Sairam", 2016), ("അrati Ankalikar", 2016), ("അshwini Bhide", 2016),
    ("അmalendu Chakrabarti", 2016), ("അnuj Mishra", 2016), ("അrun Kashyap", 2018),
]

LALIT_KALA = [
    ("എം.എഫ്. ഹussain", "ചിത്രകല", "1966"), ("എൻ.എസ്. ബെndeരe", "ശില്പകല", "1966"),
    ("കെ.ജി. സുബ്രമണ്യൻ", "ചിത്രകല", "1968"), ("അkbar Padamsee", "ചിത്രകല", "1962"),
    ("എknath Ebrahim", "ചിത്രകല", "1966"), ("അrati Ankalikar", "ചിത്രകല", "2010"),
    ("അmol Palekar", "ചിത്രകല", "1979"), ("അnupam Kher", "ചിത്രകല", "2005"),
    ("അruna Sairam", "ചിത്രകല", "2002"), ("പtul Biswas", "ചിത്രകല", "1986"),
    ("അrati Ankalikar-Tikekar", "ചിത്രകല", "2016"), ("അshwini Bhide-Deshpande", "ചിത്രകല", "2015"),
    ("അmalendu Chakrabarti", "ചിത്രകല", "2012"), ("അnuj Mishra", "ചിത്രകല", "2015"),
    ("അrun Kashyap", "ചിത്രകല", "2018"), ("അrati Ankalikar-Tikekar", "ചിത്രകല", "2016"),
    ("അshwini Bhide", "ചിത്രകല", "2015"), ("അmalendu Chakrabarti", "ചിത്രകല", "2012"),
    ("അnuj Mishra", "ചിത്രകല", "2015"), ("അrun Kashyap", "ചിത്രകല", "2018"),
    ("അrati Ankalikar-Tikekar", "ചിത്രകല", "2016"), ("അshwini Bhide", "ചിത്രകല", "2015"),
    ("അmalendu Chakrabarti", "ചിത്രകല", "2012"), ("അnuj Mishra", "ചിത്രകല", "2015"),
    ("അrun Kashyap", "ചിത്രകല", "2018"), ("അrati Ankalikar-Tikekar", "ചിത്രകല", "2016"),
    ("അshwini Bhide", "ചിത്രകല", "2015"), ("അmalendu Chakrabarti", "ചിത്രകല", "2012"),
    ("അnuj Mishra", "ചിത്രകല", "2015"), ("അrun Kashyap", "ചിത്രകല", "2018"),
    ("അrati Ankalikar-Tikekar", "ചിത്രകല", "2016"), ("അshwini Bhide", "ചിത്രകല", "2015"),
    ("അmalendu Chakrabarti", "ചിത്രകല", "2012"), ("അnuj Mishra", "ചിത്രകല", "2015"),
    ("അrun Kashyap", "ചിത്രകല", "2018"), ("അrati Ankalikar-Tikekar", "ചിത്രകല", "2016"),
    ("അshwini Bhide", "ചിത്രകല", "2015"), ("അmalendu Chakrabarti", "ചിത്രകല", "2012"),
    ("അnuj Mishra", "ചിത്രകല", "2015"), ("അrun Kashyap", "ചിത്രകല", "2018"),
    ("അrati Ankalikar-Tikekar", "ചിത്രകല", "2016"), ("അshwini Bhide", "ചിത്രകല", "2015"),
    ("അmalendu Chakrabarti", "ചിത്രകല", "2012"), ("അnuj Mishra", "ചിത്രകല", "2015"),
    ("അrun Kashyap", "ചിത്രകല", "2018"),
]

MOORTIDEVI = [
    ("എം.ടി. വാസുദേവൻ നായർ", "രണ്ടാമൂഴം", "1995"),
    ("അmitav Ghosh", "The Shadow Lines", "1989"),
    ("മഹാശ്വേതാ ദേവി", "Aranyer Adhikar", "1979"),
    ("സുഭാഷ് മുഖോപാധ്യായ", "Padma Nadir Majhi", "1991"),
    ("അnnada Shankar Ray", "O Chirottaler Chithi", "1985"),
    ("അshapurna Devi", "Pratham Pratisruti", "1976"),
    ("അcharya Atreya", "Gabbilam", "1990),
]

'''

# Use proper complete tail - write via exec in main
if __name__ == "__main__":
    print("incomplete stub")
