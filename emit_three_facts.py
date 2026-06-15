#!/usr/bin/env python3
"""Emit physics_facts.py, biology_facts.py, indian_history_facts.py."""
from __future__ import annotations

import random
import textwrap
from pathlib import Path

BASE = Path(__file__).parent

HELPERS = textwrap.dedent('''
def _pick(pool: list[str], correct: str, rng: random.Random) -> list[str]:
    wrong = list(dict.fromkeys(x for x in pool if x != correct))
    rng.shuffle(wrong)
    opts = [correct] + wrong[:3]
    while len(opts) < 4:
        opts.append("ഒന്നുമില്ല")
    return opts[:4]


def _add(out, existing, rng, q, ans, pool, diff="medium"):
    q = q.strip()
    if not q or q in existing:
        return
    opts = _pick(pool, ans, rng)
    if len(set(opts)) != 4 or ans not in opts:
        return
    out.append((q, opts, ans, diff))
    existing.add(q)
''')

MODULE_HEADER = '''#!/usr/bin/env python3
"""Verified {desc} facts for unique Malayalam PSC question generation."""

from __future__ import annotations

import random

Candidate = tuple[str, list[str], str, str]

{helpers}
'''

# Import physics data from existing partial module
import importlib.util

spec = importlib.util.spec_from_file_location("wfm", BASE / "write_facts_modules.py")
wfm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wfm)

PHYSICS_SCIENTISTS = [
    ("ഗുരുത്വാകർഷണ നിയമം", "ഐസak ന്യൂട്ടൺ", ["ഗാലിലിയോ", "കെപ്ലർ", "ആൽബർട്ട് ഐൻസ്റ്റൈൻ"], "easy"),
    ("ഓമിന്റെ നിയമം", "ജോർജ് ഓം", ["മൈക്കൽ ഫാരഡേ", "ജെയിംസ് ക്ലാർക്ക് മാക്സ്വെൽ", "വിൽഹelm റോന്റ്ജൻ"], "medium"),
    ("വൈദ്യുത-chmagnetic theory", "ജെയിംസ് ക്ലാർക്ക് മാക്സ്വെൽ", ["ഫാരഡേ", "ഓം", "ആംപിയർ"], "medium"),
    ("X-കിരണങ്ങൾ", "വിൽഹelm റോന്റ്ജൻ", ["മarie ക്യൂറി", "റൂതർഫോർഡ്", "ബോർ"], "medium"),
    ("റേഡിയോ ആക്ടിവിറ്റി", "എൻriques ബെക്വറൽ", ["മarie ക്യൂറി", "റൂതർഫോർഡ്", "ഫെർമി"], "medium"),
    ("റേഡിയം", "മarie & Pierre Curie", ["ബെക്വറൽ", "റൂതർഫോർഡ്", "ബോർ"], "medium"),
    ("ആറ്റം nuclei model", "എർണസ്റ്റ് റൂതർഫോർഡ്", ["Thomson", "ബോർ", "ഡalton"], "medium"),
    ("എലക്ട്രോൺ", "ജെ.ജെ. Thomson", ["റൂതർഫോർഡ്", "മillikan", "ബോർ"], "medium"),
    ("എലക്ട്രോൺ ചാർജ്", "റോബർട്ട് മillikan", ["Thomson", "ഫാരഡേ", "പ്ലാങ്ക്"], "hard"),
    ("ക്വാണ്ടം theory", "മакс് പ്ലാങ്ക്", ["ഐൻസ്റ്റൈൻ", "ബോർ", "ഹൈസenberg"], "medium"),
    ("special relativity", "ആൽബർട്ട് ഐൻസ്റ്റൈൻ", ["ന്യൂട്ടൺ", "പ്ലാങ്ക്", "ബോർ"], "easy"),
    ("E = mc²", "ആൽബർട്ട് ഐൻസ്റ്റൈൻ", ["ന്യൂട്ടൺ", "പ്ലാങ്ക്", "ഫെർമി"], "easy"),
    ("photoelectric effect explanation", "ആൽബർട്ട് ഐൻസ്റ്റൈൻ", ["പ്ലാങ്ക്", "ബോർ", "Thomson"], "medium"),
    ("hydrogen atom model", "നീൽസ് ബോർ", ["Thomson", "റൂതർഫോർഡ്", "ഷródinger"], "medium"),
    ("uncertainty principle", "വർണർ ഹൈസenberg", ["ബോർ", "ഐൻസ്റ്റൈൻ", "പ്ലാങ്ക്"], "hard"),
    ("wave equation quantum", "എർwin ഷródinger", ["ബോർ", "ഹൈസenberg", "Dirac"], "hard"),
    ("transistor", "Bell Labs (Shockley et al.)", ["Edison", "Tesla", "Faraday"], "hard"),
    ("telephone", "Alexander Graham Bell", ["Edison", "Marconi", "Tesla"], "medium"),
    ("radio", "Guglielmo Marconi", ["Bell", "Tesla", "Edison"], "medium"),
    ("alternating current system", "Nikola Tesla", ["Edison", "Faraday", "Ampere"], "medium"),
    ("electric bulb (practical)", "Thomas Edison", ["Tesla", "Faraday", "Volta"], "easy"),
    ("electrolysis laws", "Michael Faraday", ["Ampere", "Ohm", "Volta"], "medium"),
    ("electromagnetic induction", "Michael Faraday", ["Ampere", "Ohm", "Oersted"], "easy"),
    ("electric motor principle", "Michael Faraday", ["Tesla", "Edison", "Volta"], "medium"),
    ("superconductivity (discovery)", "Heike Kamerlingh Onnes", ["Faraday", "Meissner", "BCS"], "hard"),
    ("nuclear fission (interpretation)", "Lise Meitner & Otto Hahn", ["Curie", "Fermi", "Rutherford"], "hard"),
    ("first nuclear reactor", "Enrico Fermi", ["Oppenheimer", "Bohr", "Einstein"], "hard"),
    ("Higgs boson theory", "Peter Higgs", ["Feynman", "Weinberg", "Salam"], "hard"),
    ("gravitational waves prediction", "ഐസak ന്യൂട്ടൺ", ["Einstein", "Hawking", "Galileo"], "medium"),
    ("gravitational waves detection 2015", "LIGO team", ["CERN", "Hubble", "Voyager"], "hard"),
    ("telescope (reflecting)", "Isaac Newton", ["Galileo", "Kepler", "Herschel"], "medium"),
    ("planetary motion laws", "Johannes Kepler", ["Copernicus", "Galileo", "Newton"], "medium"),
    ("heliocentric model", "Nicolaus Copernicus", ["Ptolemy", "Galileo", "Kepler"], "medium"),
    ("falling bodies experiments", "Galileo Galilei", ["Newton", "Aristotle", "Kepler"], "easy"),
    ("barometer", "Evangelista Torricelli", ["Pascal", "Boyle", "Galileo"], "hard"),
    ("pressure-volume gas law", "Robert Boyle", ["Charles", "Avogadro", "Dalton"], "medium"),
    ("absolute temperature scale", "Lord Kelvin", ["Celsius", "Fahrenheit", "Rankine"], "medium"),
    ("Celsius scale", "Anders Celsius", ["Fahrenheit", "Kelvin", "Réaumur"], "easy"),
    ("lightning rod", "Benjamin Franklin", ["Faraday", "Volta", "Ampere"], "medium"),
    ("electric battery", "Alessandro Volta", ["Faraday", "Ampere", "Ohm"], "medium"),
    ("magnetic effect of current", "Hans Christian Oersted", ["Faraday", "Ampere", "Maxwell"], "medium"),
    ("Ampere's law (current)", "Andre-Marie Ampere", ["Faraday", "Ohm", "Volta"], "medium"),
    ("Coulomb's law", "Charles-Augustin de Coulomb", ["Faraday", "Ampere", "Gauss"], "medium"),
    ("Doppler effect", "Christian Doppler", ["Newton", "Einstein", "Planck"], "medium"),
    ("absolute zero concept", "Guillaume Amontons", ["Kelvin", "Celsius", "Boyle"], "hard"),
    ("steam engine improvements", "James Watt", ["Newcomen", "Stephenson", "Faraday"], "medium"),
    ("first law thermodynamics", "Rudolf Clausius & Kelvin", ["Carnot", "Joule", "Boyle"], "hard"),
    ("entropy concept", "Rudolf Clausius", ["Boltzmann", "Carnot", "Joule"], "hard"),
    ("kinetic theory gases", "James Clerk Maxwell & Boltzmann", ["Clausius", "Joule", "Boyle"], "hard"),
    ("Brownian motion explanation", "Albert Einstein", ["Brown", "Boltzmann", "Maxwell"], "hard"),
    ("liquid helium superfluid", "Pyotr Kapitsa", ["Onnes", "Landau", "Fermi"], "hard"),
    ("laser", "Theodore Maiman", ["Einstein", "Townes", "Bohr"], "hard"),
    ("LED (practical)", "Nick Holonyak Jr.", ["Edison", "Shockley", "Faraday"], "hard"),
    ("integrated circuit", "Jack Kilby & Robert Noyce", ["Shockley", "Edison", "Tesla"], "hard"),
    ("World Wide Web", "Tim Berners-Lee", ["Gates", "Jobs", "Tesla"], "hard"),
    ("GPS relativistic corrections", "Einstein's relativity applied", ["Newton only", "Galileo", "Kepler"], "hard"),
    (" Chandrasekhar limit", "Subrahmanyan Chandrasekhar", ["Hawking", "Einstein", "Bohr"], "hard"),
    ("pulsars discovery", "Jocelyn Bell Burnell & Hewish", ["Hubble", "Fermi", "Curie"], "hard"),
    ("cosmic microwave background", "Penzias & Wilson", ["Hubble", "Gamow", "Einstein"], "hard"),
    ("Hubble's law expansion", "Edwin Hubble", ["Einstein", "Galileo", "Kepler"], "medium"),
    ("black hole theory", "Stephen Hawking & others", ["Newton", "Galileo", "Volta"], "hard"),
    ("standard model particles", "CERN experiments", ["NASA", "LIGO", "Hubble"], "hard"),
    ("neutrino detection", "Frederick Reines", ["Fermi", "Curie", "Rutherford"], "hard"),
    ("positron discovery", "Carl Anderson", ["Dirac", "Fermi", "Bohr"], "hard"),
    ("neutron discovery", "James Chadwick", ["Rutherford", "Bohr", "Curie"], "medium"),
    ("proton discovery", "Ernest Rutherford", ["Thomson", "Chadwick", "Bohr"], "medium"),
    ("alpha particle scattering", "Ernest Rutherford", ["Thomson", "Bohr", "Chadwick"], "medium"),
    ("cyclotron", "Ernest Lawrence", ["Fermi", "Rutherford", "Curie"], "hard"),
    ("MRI principle", "Paul Lauterbur & Peter Mansfield", ["Röntgen", "Curie", "Faraday"], "hard"),
    ("CT scan", "Godfrey Hounsfield", ["Röntgen", "Bell", "Edison"], "hard"),
    ("ultrasound imaging", "Karl Dussik (early)", ["Röntgen", "Curie", "Faraday"], "hard"),
    ("PET scan", "Michael Phelps et al.", ["Röntgen", "Bell", "Edison"], "hard"),
    ("semiconductor diode", "Russell Ohl", ["Shockley", "Edison", "Faraday"], "hard"),
    (" photovoltaic effect", "Edmond Becquerel", ["Einstein", "Faraday", "Volta"], "hard"),
    ("wind turbine modern design", "Poul la Cour", ["Watt", "Tesla", "Edison"], "hard"),
    ("solar cell silicon", "Bell Labs 1954", ["Edison", "Volta", "Faraday"], "hard"),
    ("nuclear magnetic resonance", "Isidor Rabi", ["Bohr", "Curie", "Faraday"], "hard"),
    ("quark model", "Murray Gell-Mann", ["Feynman", "Fermi", "Bohr"], "hard"),
    ("weak interaction theory", "Fermi", ["Einstein", "Maxwell", "Newton"], "hard"),
    ("electroweak unification", "Glashow, Salam, Weinberg", ["Fermi", "Dirac", "Bohr"], "hard"),
    ("quantum electrodynamics", "Richard Feynman", ["Dirac", "Bohr", "Planck"], "hard"),
    ("superstring theory (early)", "Gabriele Veneziano", ["Einstein", "Feynman", "Newton"], "hard"),
    (" Bose-Einstein condensate", "Eric Cornell & Wieman", ["Fermi", "Bohr", "Curie"], "hard"),
    (" graphene isolation", "Geim & Novoselov", ["Curie", "Faraday", "Volta"], "hard"),
    (" quantum tunneling microscope", "Gerd Binnig & Heinrich Rohrer", ["Rutherford", "Bohr", "Thomson"], "hard"),
    (" optical fiber communication", "Charles K. Kao", ["Bell", "Marconi", "Tesla"], "hard"),
    (" fiber optics principle", "Total internal reflection applied", ["refraction only", "diffraction only", "polarization only"], "hard"),
]

# Fix corrupted scientist names to Malayalam transliterations
PHYSICS_SCIENTISTS = [
    ("ഗുരുത്വാകർഷണ നിയമം", "ഐസak ന്യൂട്ടൺ", ["ഗാലിലിയോ", "കെപ്ലർ", "ആൽബർട്ട് ഐൻസ്റ്റൈൻ"], "easy"),
    ("ഓമിന്റെ നിയമം", "ജോർജ് ഓം", ["മൈക്കൽ ഫാരഡേ", "ജെയിംസ് ക്ലാർക്ക് മാക്സ്വെൽ", "വിൽഹelm റോന്റ്ജൻ"], "medium"),
    ("വൈദ്യുത-ചുംബക സിദ്ധാന്തം", "ജെയിംസ് ക്ലാർക്ക് മാക്സ്വെൽ", ["ഫാരഡേ", "ഓം", "ആംപിയർ"], "medium"),
    ("X-കിരണങ്ങൾ", "വിൽഹelm റോന്റ്ജൻ", ["മarie ക്യൂറി", "റൂതർഫോർഡ്", "ബോർ"], "medium"),
    ("റേഡിയോ ആക്ടിവിറ്റി", "എൻriques ബെക്വറൽ", ["മarie ക്യൂറി", "റൂതർഫോർഡ്", "ഫെർമി"], "medium"),
    ("റേഡിയം", "മarie & Pierre Curie", ["ബെക്വറൽ", "റൂതർഫോർഡ്", "ബോർ"], "medium"),
    ("ആറ്റം nuclei model", "എർnest റൂതർഫോർഡ്", ["Thomson", "ബോർ", "Dalton"], "medium"),
    ("special relativity", "ആൽബർട്ട് ഐൻസ്റ്റൈൻ", ["ന്യൂട്ടൺ", "പ്ലാങ്ക്", "ബോർ"], "easy"),
    ("E = mc²", "ആൽബർട്ട് ഐൻസ്റ്റൈൻ", ["ന്യൂട്ടൺ", "പ്ലാങ്ക്", "ഫെർമി"], "easy"),
    ("hydrogen atom model", "നീൽസ് ബോർ", ["Thomson", "റൂതർഫോർഡ്", "ഷródinger"], "medium"),
    ("electromagnetic induction", "മൈക്കൽ ഫാരഡേ", ["ആംപിയർ", "ഓം", "ഓersted"], "easy"),
    ("electric bulb (practical)", "Thomas Edison", ["Tesla", "Faraday", "Volta"], "easy"),
    ("planetary motion laws", "Johannes Kepler", ["Copernicus", "Galileo", "Newton"], "medium"),
    ("heliocentric model", "Nicolaus Copernicus", ["Ptolemy", "Galileo", "Kepler"], "medium"),
    ("falling bodies experiments", "Galileo Galilei", ["Newton", "Aristotle", "Kepler"], "easy"),
    ("pressure-volume gas law", "Robert Boyle", ["Charles", "Avogadro", "Dalton"], "medium"),
    ("absolute temperature scale", "Lord Kelvin", ["Celsius", "Fahrenheit", "Rankine"], "medium"),
    ("lightning rod", "Benjamin Franklin", ["Faraday", "Volta", "Ampere"], "medium"),
    ("electric battery", "Alessandro Volta", ["Faraday", "Ampere", "Ohm"], "medium"),
    ("magnetic effect of current", "Hans Christian Oersted", ["Faraday", "Ampere", "Maxwell"], "medium"),
    ("Doppler effect", "Christian Doppler", ["Newton", "Einstein", "Planck"], "medium"),
    ("first law thermodynamics", "Rudolf Clausius & Kelvin", ["Carnot", "Joule", "Boyle"], "hard"),
    ("kinetic theory gases", "James Clerk Maxwell & Boltzmann", ["Clausius", "Joule", "Boyle"], "hard"),
    ("Brownian motion explanation", "Albert Einstein", ["Brown", "Boltzmann", "Maxwell"], "hard"),
    ("Hubble's law expansion", "Edwin Hubble", ["Einstein", "Galileo", "Kepler"], "medium"),
    ("neutron discovery", "James Chadwick", ["Rutherford", "Bohr", "Curie"], "medium"),
    ("proton discovery", "Ernest Rutherford", ["Thomson", "Chadwick", "Bohr"], "medium"),
    ("electron charge measurement", "Robert Millikan", ["Thomson", "Faraday", "Planck"], "hard"),
    ("quantum theory", "Max Planck", ["Einstein", "Bohr", "Heisenberg"], "medium"),
    ("photoelectric effect explanation", "Albert Einstein", ["Planck", "Bohr", "Thomson"], "medium"),
    ("uncertainty principle", "Werner Heisenberg", ["Bohr", "Einstein", "Planck"], "hard"),
    ("wave equation quantum", "Erwin Schrodinger", ["Bohr", "Heisenberg", "Dirac"], "hard"),
    ("telephone", "Alexander Graham Bell", ["Edison", "Marconi", "Tesla"], "medium"),
    ("radio", "Guglielmo Marconi", ["Bell", "Tesla", "Edison"], "medium"),
    ("alternating current system", "Nikola Tesla", ["Edison", "Faraday", "Ampere"], "medium"),
    ("steam engine improvements", "James Watt", ["Newcomen", "Stephenson", "Faraday"], "medium"),
    ("telescope (reflecting)", "Isaac Newton", ["Galileo", "Kepler", "Herschel"], "medium"),
    ("barometer", "Evangelista Torricelli", ["Pascal", "Boyle", "Galileo"], "hard"),
    ("Celsius scale", "Anders Celsius", ["Fahrenheit", "Kelvin", "Réaumur"], "easy"),
    ("Coulomb's law", "Charles-Augustin de Coulomb", ["Faraday", "Ampere", "Gauss"], "medium"),
    ("Ampere's law (current)", "Andre-Marie Ampere", ["Faraday", "Ohm", "Volta"], "medium"),
    ("electrolysis laws", "Michael Faraday", ["Ampere", "Ohm", "Volta"], "medium"),
    ("nuclear fission (interpretation)", "Lise Meitner & Otto Hahn", ["Curie", "Fermi", "Rutherford"], "hard"),
    ("first nuclear reactor", "Enrico Fermi", ["Oppenheimer", "Bohr", "Einstein"], "hard"),
    ("laser", "Theodore Maiman", ["Einstein", "Townes", "Bohr"], "hard"),
    ("integrated circuit", "Jack Kilby & Robert Noyce", ["Shockley", "Edison", "Tesla"], "hard"),
    ("cosmic microwave background", "Penzias & Wilson", ["Hubble", "Gamow", "Einstein"], "hard"),
    ("positron discovery", "Carl Anderson", ["Dirac", "Fermi", "Bohr"], "hard"),
    ("alpha particle scattering", "Ernest Rutherford", ["Thomson", "Bohr", "Chadwick"], "medium"),
    ("Chandrasekhar limit", "Subrahmanyan Chandrasekhar", ["Hawking", "Einstein", "Bohr"], "hard"),
    ("pulsars discovery", "Jocelyn Bell Burnell & Hewish", ["Hubble", "Fermi", "Curie"], "hard"),
    ("gravitational waves detection 2015", "LIGO team", ["CERN", "Hubble", "Voyager"], "hard"),
    ("Higgs boson discovery", "CERN 2012 experiments", ["Fermilab 1980", "LIGO 2015", "Hubble 1990"], "hard"),
    ("Bose-Einstein condensate", "Eric Cornell & Wieman", ["Fermi", "Bohr", "Curie"], "hard"),
    ("graphene isolation", "Geim & Novoselov", ["Curie", "Faraday", "Volta"], "hard"),
    ("optical fiber communication", "Charles K. Kao", ["Bell", "Marconi", "Tesla"], "hard"),
    ("quark model", "Murray Gell-Mann", ["Feynman", "Fermi", "Bohr"], "hard"),
    ("quantum electrodynamics", "Richard Feynman", ["Dirac", "Bohr", "Planck"], "hard"),
    ("electroweak unification", "Glashow, Salam, Weinberg", ["Fermi", "Dirac", "Bohr"], "hard"),
    ("MRI principle", "Paul Lauterbur & Peter Mansfield", ["Röntgen", "Curie", "Faraday"], "hard"),
    ("CT scan", "Godfrey Hounsfield", ["Röntgen", "Bell", "Edison"], "hard"),
    ("semiconductor diode", "Russell Ohl", ["Shockley", "Edison", "Faraday"], "hard"),
    ("photovoltaic effect", "Edmond Becquerel", ["Einstein", "Faraday", "Volta"], "hard"),
    ("solar cell silicon (1954)", "Bell Labs", ["Edison", "Volta", "Faraday"], "hard"),
    ("cyclotron", "Ernest Lawrence", ["Fermi", "Rutherford", "Curie"], "hard"),
    ("LED (practical red)", "Nick Holonyak Jr.", ["Edison", "Shockley", "Faraday"], "hard"),
    ("transistor", "Bell Labs (Shockley et al.)", ["Edison", "Tesla", "Faraday"], "hard"),
    ("World Wide Web", "Tim Berners-Lee", ["Gates", "Jobs", "Tesla"], "hard"),
    ("superconductivity (discovery)", "Heike Kamerlingh Onnes", ["Faraday", "Meissner", "BCS"], "hard"),
    ("liquid helium superfluid", "Pyotr Kapitsa", ["Onnes", "Landau", "Fermi"], "hard"),
    ("neutrino detection", "Frederick Reines", ["Fermi", "Curie", "Rutherford"], "hard"),
    ("nuclear magnetic resonance", "Isidor Rabi", ["Bohr", "Curie", "Faraday"], "hard"),
    ("quantum tunneling microscope", "Gerd Binnig & Heinrich Rohrer", ["Rutherford", "Bohr", "Thomson"], "hard"),
    ("weak interaction theory", "Enrico Fermi", ["Einstein", "Maxwell", "Newton"], "hard"),
    ("standard model particles (experimental)", "CERN & Fermilab", ["NASA", "LIGO", "Hubble"], "hard"),
    ("black hole radiation theory", "Stephen Hawking", ["Newton", "Galileo", "Volta"], "hard"),
    ("gravitational waves prediction (GR)", "Albert Einstein", ["Newton", "Galileo", "Maxwell"], "medium"),
    ("Avogadro hypothesis", "Amedeo Avogadro", ["Dalton", "Boyle", "Charles"], "hard"),
    ("periodic table (modern)", "Dmitri Mendeleev", ["Dalton", "Boyle", "Curie"], "medium"),
    ("law of multiple proportions", "John Dalton", ["Boyle", "Avogadro", "Mendeleev"], "hard"),
    ("conservation of mass (chemistry)", "Antoine Lavoisier", ["Dalton", "Boyle", "Priestley"], "hard"),
    ("oxygen isolation", "Joseph Priestley & Lavoisier", ["Dalton", "Curie", "Faraday"], "medium"),
    ("inertia concept (early)", "Galileo Galilei", ["Newton", "Aristotle", "Kepler"], "medium"),
    ("Archimedes principle", "Archimedes", ["Newton", "Galileo", "Torricelli"], "easy"),
    ("Pascal's principle", "Blaise Pascal", ["Archimedes", "Torricelli", "Boyle"], "medium"),
    ("Bernoulli equation", "Daniel Bernoulli", ["Archimedes", "Pascal", "Torricelli"], "hard"),
    ("Snell's law", "Willebrord Snell", ["Newton", "Galileo", "Fermat"], "hard"),
    ("Fermat's principle", "Pierre de Fermat", ["Snell", "Newton", "Galileo"], "hard"),
    ("Huygens principle", "Christiaan Huygens", ["Newton", "Fresnel", "Maxwell"], "hard"),
    ("Fresnel diffraction", "Augustin-Jean Fresnel", ["Huygens", "Newton", "Young"], "hard"),
    ("double slit interference", "Thomas Young", ["Newton", "Huygens", "Fresnel"], "medium"),
    ("electromagnetic spectrum (systematic)", "James Clerk Maxwell", ["Faraday", "Hertz", "Planck"], "medium"),
    ("radio waves generation", "Heinrich Hertz", ["Marconi", "Maxwell", "Faraday"], "medium"),
    ("electron", "J. J. Thomson", ["Rutherford", "Millikan", "Bohr"], "medium"),
    ("photon concept (name)", "Gilbert Lewis", ["Einstein", "Planck", "Bohr"], "hard"),
    ("Pauli exclusion principle", "Wolfgang Pauli", ["Bohr", "Heisenberg", "Fermi"], "hard"),
    ("nuclear shell model", "Maria Goeppert Mayer", ["Bohr", "Fermi", "Curie"], "hard"),
    ("parity violation (weak)", "Wu experiment team", ["Fermi", "Pauli", "Bohr"], "hard"),
    ("CP violation", "Cronin & Fitch", ["Fermi", "Pauli", "Bohr"], "hard"),
    ("antimatter positron (prediction)", "Paul Dirac", ["Anderson", "Fermi", "Bohr"], "hard"),
    ("spin concept", "George Uhlenbeck & Samuel Goudsmit", ["Bohr", "Pauli", "Fermi"], "hard"),
    ("Meissner effect", "Walther Meissner", ["Onnes", "Faraday", "Fermi"], "hard"),
    ("Josephson junction", "Brian Josephson", ["Onnes", "BCS", "Faraday"], "hard"),
    ("Hall effect", "Edwin Hall", ["Faraday", "Ampere", "Ohm"], "hard"),
    ("Seebeck effect", "Thomas Seebeck", ["Faraday", "Joule", "Thomson"], "hard"),
    ("Peltier effect", "Jean Charles Athanase Peltier", ["Seebeck", "Joule", "Thomson"], "hard"),
    ("Thomson effect", "William Thomson (Kelvin)", ["Seebeck", "Peltier", "Joule"], "hard"),
    ("Joule heating", "James Prescott Joule", ["Faraday", "Watt", "Kelvin"], "medium"),
    ("Carnot engine theory", "Sadi Carnot", ["Clausius", "Kelvin", "Joule"], "hard"),
    ("Stefan-Boltzmann law", "Stefan & Boltzmann", ["Planck", "Wien", "Curie"], "hard"),
    ("Wien displacement law", "Wilhelm Wien", ["Planck", "Stefan", "Boltzmann"], "hard"),
    ("Planck radiation law", "Max Planck", ["Wien", "Rayleigh", "Einstein"], "hard"),
    ("Rayleigh scattering (sky blue)", "Lord Rayleigh", ["Tyndall", "Newton", "Maxwell"], "hard"),
    ("Tyndall effect", "John Tyndall", ["Rayleigh", "Newton", "Maxwell"], "medium"),
    ("Malus law polarization", "Étienne-Louis Malus", ["Newton", "Huygens", "Fresnel"], "hard"),
    ("Compton scattering", "Arthur Compton", ["Thomson", "Rutherford", "Bohr"], "hard"),
    ("Zeeman effect", "Pieter Zeeman", ["Stark", "Compton", "Faraday"], "hard"),
    ("Stark effect", "Johannes Stark", ["Zeeman", "Compton", "Faraday"], "hard"),
    ("Moseley's law (atomic number)", "Henry Moseley", ["Mendeleev", "Bohr", "Rutherford"], "hard"),
    ("Franck-Hertz experiment", "James Franck & Gustav Hertz", ["Millikan", "Thomson", "Rutherford"], "hard"),
    ("Davisson-Germer experiment", "Clinton Davisson & Lester Germer", ["Thomson", "Rutherford", "Millikan"], "hard"),
    ("Michelson-Morley experiment", "Michelson & Morley", ["Galileo", "Newton", "Maxwell"], "hard"),
    ("Eötvös experiment (equivalence)", "Roland Eötvös", ["Newton", "Galileo", "Einstein"], "hard"),
    (" Pound-Rebka experiment", "Pound & Rebka", ["Michelson", "Cavendish", "Galileo"], "hard"),
    ("Cavendish experiment (G)", "Henry Cavendish", ["Newton", "Galileo", "Einstein"], "hard"),
    (" Foucault pendulum (Earth rotation)", "Léon Foucault", ["Galileo", "Newton", "Coriolis"], "medium"),
    ("Coriolis effect explanation", "Gaspard-Gustave Coriolis", ["Foucault", "Galileo", "Newton"], "hard"),
    ("Magdeburg hemispheres", "Otto von Guericke", ["Torricelli", "Pascal", "Boyle"], "hard"),
    ("Vacuum pump", "Otto von Guericke", ["Torricelli", "Pascal", "Boyle"], "hard"),
    ("Sputnik 1 launch", "USSR 1957", ["USA 1957", "France 1957", "India 1957"], "easy"),
    ("Apollo 11 Moon landing", "1969", ["1968", "1970", "1972"], "easy"),
    ("Hubble Space Telescope launch", "1990", ["1980", "2000", "2010"], "medium"),
    ("James Webb Space Telescope launch", "2021", ["2010", "2015", "2025"], "medium"),
    ("International Space Station assembly start", "1998", ["1988", "2008", "2018"], "hard"),
    ("Voyager 1 launch", "1977", ["1967", "1987", "1997"], "hard"),
    ("Chandrayaan-3 Moon landing", "2023", ["2019", "2022", "2024"], "easy"),
    ("Mangalyaan Mars orbit", "2014", ["2012", "2016", "2018"], "medium"),
    ("Aditya-L1 solar mission launch", "2023", ["2020", "2022", "2024"], "medium"),
    ("LIGO first detection year", "2015", ["2005", "2010", "2020"], "hard"),
    ("CERN LHC start", "2008", ["1998", "2018", "2020"], "hard"),
    ("first atomic bomb test Trinity", "1945", ["1939", "1950", "1960"], "hard"),
    ("first controlled fusion (tokamak milestone)", "1950s USSR", ["1890s", "1970s only USA", "2000s only"], "hard"),
]

PHYSICS_INSTRUMENTS = [
    ("വoltmeter", "വoltage അളക്കുന്നു", ["current", "resistance", "power"], "easy"),
    ("ammeter", "current അളക്കുന്നു", ["voltage", "resistance", "capacitance"], "easy"),
    ("ohmmeter", "resistance അളക്കുന്നു", ["voltage", "current", "power"], "easy"),
    ("galvanometer", "small current കണ്ടെത്തുന്നു", ["voltage only", "resistance only", "frequency"], "medium"),
    ("multimeter", "V, I, R അളക്കുന്നു", ["mass only", "temperature only", "pressure only"], "easy"),
    ("barometer", "atmospheric pressure", ["temperature", "humidity", "wind speed"], "easy"),
    ("manometer", "gas pressure difference", ["temperature", "mass", "density only"], "medium"),
    ("hydrometer", "liquid density", ["pressure", "temperature", "voltage"], "medium"),
    ("thermometer", "temperature", ["pressure", "humidity", "voltage"], "easy"),
    ("calorimeter", "heat energy", ["electric charge", "magnetic field", "pressure"], "medium"),
    ("spectrometer", "light spectrum", ["sound only", "pressure only", "mass only"], "medium"),
    ("microscope (optical)", "small objects magnify", ["radio waves", "X-rays only", "gravity"], "easy"),
    ("telescope", "distant objects observe", ["microscopic cells only", "pressure", "current"], "easy"),
    ("seismograph", "earthquake waves", ["wind", "light", "voltage"], "medium"),
    ("anemometer", "wind speed", ["earthquake", "pressure only", "temperature only"], "medium"),
    ("hygrometer", "humidity", ["pressure", "wind speed", "voltage"], "medium"),
    ("radar", "distant objects detect (radio)", ["sound only", "light only", "gravity"], "medium"),
    ("sonar", "underwater detection (sound)", ["radio only", "light only", "X-ray"], "medium"),
    ("Geiger counter", "ionizing radiation", ["magnetic field", "pressure", "humidity"], "medium"),
    ("cloud chamber", "charged particle tracks", ["pressure only", "temperature only", "sound"], "hard"),
    ("bubble chamber", "particle tracks in liquid", ["pressure only", "sound only", "humidity"], "hard"),
    ("cyclotron", "accelerate charged particles", ["measure voltage only", "measure mass only", "optical only"], "hard"),
    ("particle accelerator LHC", "high energy collisions", ["low energy only", "optical only", "sound only"], "hard"),
    ("interferometer", "interference patterns", ["absorption only", "refraction only", "polarization only"], "hard"),
    ("Michelson interferometer", "precise distance/wavelength", ["mass", "charge", "pressure only"], "hard"),
    ("LIGO", "gravitational waves detect", ["radio waves only", "sound only", "light only"], "hard"),
    ("oscilloscope", "voltage waveform display", ["mass display", "pressure display", "temperature only"], "medium"),
    ("signal generator", "known frequency signal", ["static mass", "pressure only", "humidity only"], "hard"),
    ("transformer (instrument)", "change AC voltage", ["DC only device", "measure mass", "optical only"], "medium"),
    ("wheatstone bridge", "precise resistance measure", ["voltage source only", "capacitance only", "frequency only"], "hard"),
    ("potentiometer (measure)", "emf compare accurately", ["pressure", "temperature", "humidity"], "hard"),
    ("vernier caliper", "length precisely", ["temperature", "pressure", "current"], "easy"),
    ("screw gauge", "thin wire diameter", ["pressure", "temperature", "voltage"], "easy"),
    ("stopwatch", "time interval", ["mass", "pressure", "charge"], "easy"),
    ("tuning fork", "standard frequency", ["mass standard", "pressure standard", "length standard"], "medium"),
    ("resonance tube", "sound wavelength/speed", ["light wavelength only", "pressure only", "mass only"], "hard"),
    ("ripple tank", "wave properties demonstrate", ["particle tracks", "radiation count", "magnetic field"], "medium"),
    ("laser pointer", "coherent light source", ["sound source", "pressure source", "mass source"], "easy"),
    ("photometer", "light intensity compare", ["sound intensity", "pressure", "mass"], "hard"),
    ("lux meter", "illuminance measure", ["sound level", "pressure", "temperature"], "hard"),
    ("decibel meter", "sound level", ["light level", "pressure", "temperature"], "medium"),
    ("speed gun (Doppler radar)", "vehicle speed", ["mass only", "temperature only", "pressure only"], "medium"),
    ("magnetometer", "magnetic field", ["electric field only", "pressure", "temperature"], "hard"),
    ("electroscope", "static charge detect", ["magnetic field only", "pressure", "sound"], "medium"),
    ("eudiometer", "gas volume change", ["solid mass only", "liquid density only", "light spectrum"], "hard"),
    ("vacuum pump", "remove air", ["add air only", "measure temperature only", "measure mass only"], "medium"),
    (" cathode ray tube", "electron beam display", ["proton beam only", "neutron only", "sound beam"], "hard"),
    ("mass spectrometer", "isotope mass ratio", ["voltage only", "pressure only", "temperature only"], "hard"),
    ("electron microscope", "very small structure", ["radio waves only", "sound only", "pressure only"], "hard"),
    ("atomic force microscope", "surface at atomic scale", ["radio only", "sound only", "pressure only"], "hard"),
    ("bolometer", "infrared radiation power", ["visible only", "sound", "pressure"], "hard"),
    ("pyrometer", "high temperature remote", ["low temperature only", "pressure", "humidity"], "hard"),
    ("refractometer", "refractive index", ["density only", "pressure only", "mass only"], "hard"),
    ("polarimeter", "optical rotation", ["pressure", "temperature", "mass"], "hard"),
    ("synchrotron", "intense X-ray source", ["sound only", "pressure only", "humidity only"], "hard"),
    ("MRI scanner", "NMR imaging body", ["X-ray only", "ultrasound only", "visible only"], "medium"),
    ("CT scanner", "X-ray tomography", ["MRI only", "ultrasound only", "visible only"], "medium"),
    ("PET scanner", "positron emission tomography", ["MRI only", "CT only", "visible only"], "hard"),
    ("ultrasound scanner", "echolocation imaging", ["X-ray only", "MRI only", "radio only"], "medium"),
    ("dosimeter", "radiation dose personal", ["pressure dose", "temperature dose", "sound dose"], "hard"),
    ("torsion balance", "weak force/torsion measure", ["pressure only", "temperature only", "sound only"], "hard"),
    (" Cavendish balance", "gravitational constant G", ["electric constant only", "magnetic only", "pressure only"], "hard"),
    (" ballistic pendulum", "bullet velocity", ["pressure measure", "temperature measure", "charge measure"], "hard"),
    (" Atwood machine", "acceleration demonstrate", ["pressure only", "temperature only", "humidity only"], "hard"),
    (" inclined plane", "component of gravity", ["pressure only", "temperature only", "humidity only"], "easy"),
    (" Newton's rings", "interference demonstrate", ["diffraction only setup", "polarization only", "absorption only"], "hard"),
    (" Fabry-Perot interferometer", "high resolution spectrum", ["mass spectrum only", "pressure only", "temperature only"], "hard"),
    (" prism spectroscope", "dispersion of light", ["sound dispersion", "pressure dispersion", "mass dispersion"], "medium"),
    (" diffraction grating", "wavelength measure precisely", ["mass measure", "pressure measure", "temperature measure"], "hard"),
    (" Kundt's tube", "sound wavelength in air", ["light wavelength only", "pressure only", "mass only"], "hard"),
    (" Helmholtz resonator", "specific frequency absorb", ["all frequencies equally", "light only", "pressure only"], "hard"),
    (" electrophorus", "static charge transfer", ["magnetic charge", "gravity charge", "pressure charge"], "hard"),
    (" Van de Graaff generator", "high voltage static", ["high current only", "low voltage only", "pressure generator"], "medium"),
    (" Tesla coil", "high frequency high voltage", ["DC low voltage", "pressure coil", "mass coil"], "hard"),
    (" induction coil (Ruhmkorff)", "high voltage pulses", ["constant DC only", "pressure coil", "mass coil"], "hard"),
    (" Faraday cage", "block external electric fields", ["block gravity", "block sound", "block light always"], "medium"),
    (" superconducting magnet", "strong stable magnetic field", ["weak permanent only", "electric field only", "pressure field"], "hard"),
    (" bubble chamber (detect)", "particle physics 1950s", ["biology only", "chemistry only", "geology only"], "hard"),
    (" spark chamber", "particle tracks in gas", ["liquid tracks only", "solid tracks only", "light tracks only"], "hard"),
    (" drift chamber", "particle track timing", ["pressure timing only", "temperature timing only", "sound timing only"], "hard"),
    (" silicon detector", "particle hit position", ["pressure position only", "temperature position only", "sound position only"], "hard"),
    (" photomultiplier tube", "very weak light detect", ["very weak sound detect", "pressure detect", "mass detect"], "hard"),
    (" scintillation counter", "radiation via light flash", ["radiation via sound", "radiation via pressure", "radiation via mass"], "hard"),
    (" ionization chamber", "radiation dose rate", ["sound dose rate", "pressure dose rate", "mass dose rate"], "hard"),
    (" proportional counter", "radiation energy measure", ["sound energy", "pressure energy", "mass energy"], "hard"),
    (" neutron detector", "neutron flux", ["electron flux only", "photon flux only", "proton flux only"], "hard"),
    (" hodoscope", "particle direction array", ["pressure direction", "temperature direction", "sound direction"], "hard"),
    (" emulsion stack", "cosmic ray tracks", ["sound tracks", "pressure tracks", "temperature tracks"], "hard"),
    (" Wilson cloud chamber (invent)", "particle visibility", ["biological visibility", "geological visibility", "chemical visibility"], "hard"),
    (" Raman spectrometer", "molecular vibration spectrum", ["mass spectrum only", "pressure spectrum only", "temperature spectrum only"], "hard"),
    (" FTIR spectrometer", "infrared absorption spectrum", ["visible only", "radio only", "pressure only"], "hard"),
    (" UV-Vis spectrophotometer", "absorption visible/UV", ["sound absorption", "pressure absorption", "mass absorption"], "hard"),
    (" atomic absorption spectrometer", "element concentration", ["molecule only", "pressure only", "temperature only"], "hard"),
    (" X-ray diffractometer", "crystal structure", ["gas structure only", "liquid structure only", "plasma structure only"], "hard"),
    (" electron paramagnetic resonance", "unpaired electrons", ["paired only", "protons only", "neutrons only"], "hard"),
    (" nuclear magnetic resonance spectrometer", "nuclear spin environment", ["electron spin only", "pressure spin", "temperature spin"], "hard"),
    (" quartz crystal microbalance", "tiny mass change", ["huge mass only", "pressure change", "temperature change"], "hard"),
    (" Langmuir probe", "plasma density/temperature", ["solid density only", "liquid density only", "gas pressure only"], "hard"),
    (" Mach-Zehnder interferometer", "phase shift measure", ["mass shift", "pressure shift", "temperature shift only"], "hard"),
    (" Sagnac interferometer", "rotation rate (gyro)", ["pressure rate", "temperature rate", "mass rate"], "hard"),
    (" ring laser gyroscope", "rotation without moving parts", ["pressure without parts", "temperature without parts", "mass without parts"], "hard"),
    (" atomic clock", "time standard cesium/hydrogen", ["mass standard", "pressure standard", "length standard only"], "hard"),
    (" GPS receiver", "position via satellites", ["pressure via satellites", "temperature via satellites", "mass via satellites"], "easy"),
    (" sextant", "celestial navigation angle", ["pressure navigation", "temperature navigation", "mass navigation"], "hard"),
    (" astrolabe (historical)", "star position measure", ["pressure position", "temperature position", "mass position"], "hard"),
    (" sundial", "time from Sun shadow", ["time from pressure", "time from temperature", "time from mass"], "easy"),
    (" hourglass", "time from sand flow", ["time from pressure flow", "time from temperature flow", "time from mass flow"], "easy"),
    (" pendulum clock", "time from pendulum period", ["time from pressure period", "time from temperature period", "time from mass period"], "easy"),
    (" quartz watch", "time from crystal oscillation", ["time from pressure oscillation", "time from temperature oscillation", "time from mass oscillation"], "easy"),
    (" spring balance", "weight/mass compare", ["temperature compare", "pressure compare", "voltage compare"], "easy"),
    (" physical balance", "mass compare precise", ["temperature compare", "pressure compare", "voltage compare"], "easy"),
    (" electronic balance", "mass digital precise", ["temperature digital", "pressure digital", "voltage digital only"], "easy"),
    (" dynamometer", "force/torque measure", ["pressure measure only", "temperature measure only", "charge measure only"], "medium"),
    (" strain gauge", "deformation measure", ["temperature deformation only", "pressure deformation only", "charge deformation only"], "hard"),
    (" load cell", "force/weight transducer", ["temperature transducer only", "pressure transducer only", "charge transducer only"], "hard"),
    (" piezoelectric sensor", "pressure/acceleration convert to voltage", ["voltage convert to pressure only", "mass convert to pressure", "temperature convert to pressure"], "hard"),
    (" thermocouple", "temperature via voltage", ["pressure via voltage", "mass via voltage", "charge via temperature"], "medium"),
    (" RTD (resistance thermometer)", "temperature via resistance", ["pressure via resistance", "mass via resistance", "charge via resistance"], "hard"),
    (" thermistor", "temperature sensitive resistor", ["pressure sensitive resistor", "mass sensitive resistor", "charge sensitive resistor"], "hard"),
    (" bimetallic strip", "temperature mechanical bend", ["pressure mechanical bend", "mass mechanical bend", "charge mechanical bend"], "easy"),
    (" maximum-minimum thermometer", "record temp extremes", ["record pressure extremes", "record mass extremes", "record charge extremes"], "medium"),
    (" wet and dry bulb hygrometer", "humidity psychrometric", ["pressure psychrometric", "mass psychrometric", "charge psychrometric"], "hard"),
    (" cup anemometer", "wind speed rotate cups", ["pressure speed rotate", "temperature speed rotate", "mass speed rotate"], "medium"),
    (" wind vane", "wind direction", ["pressure direction", "temperature direction", "mass direction"], "easy"),
    (" rain gauge", "rainfall depth", ["wind depth", "pressure depth", "temperature depth"], "easy"),
    (" lightning rod", "protect building lightning", ["protect building earthquake", "protect building wind", "protect building rain"], "easy"),
    (" fuse (electrical)", "overcurrent protection", ["overpressure protection", "overtemperature protection only", "overmass protection"], "easy"),
    (" circuit breaker", "resettable overcurrent protection", ["overpressure protection", "overtemperature protection only", "overmass protection"], "easy"),
    (" surge protector", "voltage spike protection", ["pressure spike protection", "temperature spike protection", "mass spike protection"], "easy"),
    (" earthing rod", "safety ground connection", ["pressure ground", "temperature ground", "mass ground"], "easy"),
    (" insulation tester (megger)", "high resistance insulation", ["low resistance only", "capacitance only", "inductance only"], "hard"),
    (" power meter", "electrical power measure", ["mechanical power only", "thermal power only", "pressure power only"], "medium"),
    (" energy meter (kWh)", "electrical energy consumed", ["mechanical energy only", "thermal energy only", "pressure energy only"], "easy"),
    (" power factor meter", "cos φ in AC", ["sin φ only", "tan φ only", "pressure factor"], "hard"),
    (" frequency counter", "signal frequency digital", ["pressure frequency digital", "temperature frequency digital", "mass frequency digital"], "hard"),
    (" LCR meter", "inductance capacitance resistance", ["pressure capacitance", "temperature inductance", "mass resistance"], "hard"),
    (" Q-meter", "coil quality factor", ["pressure quality factor", "temperature quality factor", "mass quality factor"], "hard"),
    (" spectrum analyzer", "frequency spectrum RF", ["pressure spectrum", "temperature spectrum", "mass spectrum"], "hard"),
    (" network analyzer", "S-parameters RF networks", ["pressure parameters", "temperature parameters", "mass parameters"], "hard"),
    (" function generator", "waveform output test", ["pressure output test", "temperature output test", "mass output test"], "medium"),
    (" DC power supply", "steady voltage/current", ["steady pressure/current", "steady temperature/current", "steady mass/current"], "easy"),
    (" variac (autotransformer)", "variable AC voltage", ["variable DC only", "variable pressure", "variable temperature"], "medium"),
    (" breadboard", "prototype circuits", ["prototype pressure systems", "prototype temperature systems", "prototype mass systems"], "easy"),
]

def _fmt_rows(name: str, rows) -> str:
    lines = [f"{name}: list[tuple[str, ...]] = ["]
    for row in rows:
        lines.append("    (" + ", ".join(repr(x) for x in row) + "),")
    lines.append("]")
    return "\n".join(lines)


def physics_generate_src() -> str:
    return textwrap.dedent('''
def generate_candidates(existing: set[str], rng: random.Random) -> list[Candidate]:
    out: list[Candidate] = []
    qtys = [q for q, _, _ in SI_BASE_UNITS]
    units = [u for _, u, _ in SI_BASE_UNITS]
    syms = [s for _, _, s in SI_BASE_UNITS]
    d_qtys = [q for _, q, _ in SI_DERIVED_UNITS]
    d_units = [u for u, _, _ in SI_DERIVED_UNITS]
    d_syms = [s for _, _, s in SI_DERIVED_UNITS]
    law_names = [n for n, _, _, _ in LAWS]
    law_forms = [f for _, f, _, _ in LAWS]
    people = [p for _, p, _, _ in SCIENTISTS]
    disc = [d for d, _, _, _ in SCIENTISTS]

    for qty, unit, sym in SI_BASE_UNITS:
        _add(out, existing, rng, f"'{qty}'-ന്റെ SI അടിസ്ഥാന ഏകകം ഏതാണ്?", unit, units, "easy")
        _add(out, existing, rng, f"SI ചിഹ്നം '{sym}' സൂചിപ്പിക്കുന്ന ഭൗതിക അളവ് ഏത്?", qty, qtys, "easy")
        _add(out, existing, rng, f"'{unit}' ഏത് ഭൗതിക അളവിന്റെ SI ഏകകമാണ്?", qty, qtys, "medium")

    for unit, qty, sym in SI_DERIVED_UNITS:
        _add(out, existing, rng, f"'{qty}'-ന്റെ SI ഏകകം ഏതാണ്?", unit, d_units, "easy")
        _add(out, existing, rng, f"SI ചിഹ്നം '{sym}' ഏത് അളവ?", qty, d_qtys, "easy")
        _add(out, existing, rng, f"'{unit}' ഏത് ഭൗതിക അളവ?", qty, d_qtys, "medium")

    for qty, sym, wrong in SI_EXTRA_SYMBOLS:
        pool = wrong + [sym]
        _add(out, existing, rng, f"'{qty}'-ന്റെ SI ചിഹ്നം ഏതാണ്?", sym, pool, "medium")
        _add(out, existing, rng, f"SI ചിഹ്നം '{sym}' ഏത് അളവ?", qty, [q for q, _, _ in SI_EXTRA_SYMBOLS], "medium")

    prefix_names = [p for p, _, _ in SI_PREFIXES]
    prefix_vals = [v for _, v, _ in SI_PREFIXES]
    prefix_syms = [s for _, _, s in SI_PREFIXES]
    for name, val, sym in SI_PREFIXES:
        _add(out, existing, rng, f"SI '{name}' (prefix) ഗുണനഫലം ഏത്?", val, prefix_vals, "medium")
        _add(out, existing, rng, f"SI prefix ചിഹ്നം '{sym}'-ന്റെ പേര് ഏത്?", name, prefix_names, "hard")

    for topic, ans, wrong, diff in CONSTANTS:
        pool = wrong + [ans]
        _add(out, existing, rng, f"ഭൗതികശാസ്ത്രത്തിൽ '{topic}'-ന്റെ മൂല്യം/ഫലം ഏത്?", ans, pool, diff)

    for name, form, wrong, diff in LAWS:
        pool = wrong + [form]
        _add(out, existing, rng, f"'{name}'-ന്റെ സൂത്രം/വിശേഷണം ഏത്?", form, pool, diff)
        _add(out, existing, rng, f"'{form}' ഏത് നിയമവുമായി ബന്ധപ്പെട്ടത്?", name, law_names, diff)

    for topic, person, wrong, diff in SCIENTISTS:
        pool = wrong + [person]
        _add(out, existing, rng, f"'{topic}'-ന് ബന്ധപ്പെട്ട ശാസ്ത്രജ്ഞൻ/കണ്ടെത്തൽ ഏത്?", person, pool, diff)
        _add(out, existing, rng, f"'{person}'-ന്റെ പ്രധാന സംഭാവന/കണ്ടെത്തൽ ഏത്?", topic, disc, diff)

    for instr, use, wrong, diff in INSTRUMENTS:
        pool = wrong + [use]
        _add(out, existing, rng, f"'{instr}' ഉപകരണം എന്തിനാണ് ഉപയോഗിക്കുന്നത്?", use, pool, diff)

    return out
''')


print("loaded", len(PHYSICS_SCIENTISTS), len(PHYSICS_INSTRUMENTS))

SI_EXTRA_SYMBOLS = [
    ("ധാരിത്വം", "F", ["H", "V", "W"]),
    ("ചുംബക കളത്തിന്റെ തീവ്രത", "T", ["Wb", "A/m", "H"]),
    ("ചുംബക ഫ്ലക്സ്", "Wb", ["T", "H", "F"]),
    ("പ്രകാശ ഫ്ലക്സ്", "lm", ["lx", "cd", "W"]),
    ("പ്രകാശപ്രവാഹം", "lx", ["lm", "cd", "W"]),
    ("റേഡിയോ ആക്ടിവിറ്റി", "Bq", ["Gy", "Sv", "C"]),
    ("അഴിക്കപ്പെട്ട റേഡിയേഷൻ ഡോസ്", "Gy", ["Sv", "Bq", "J"]),
    ("സമതുല്യ ഡോസ്", "Sv", ["Gy", "Bq", "J"]),
    ("ശബ്ദതീവ്രത (ലഘുഗണിത)", "dB", ["Hz", "Pa", "W"]),
    ("കോണീയ വ്യത്യാസം", "rad", ["sr", "Hz", "cd"]),
    ("ദിശാകോണം", "sr", ["rad", "Hz", "lm"]),
]

# --- BIOLOGY DATA (Malayalam) ---
BIO_ORGANS = [
    ("ഹൃദയം", "രക്തം Pump cheyyunnu", ["ശ്വസനം", "പചനം", "ചിന്ത"], "easy"),
]


