#!/usr/bin/env python3
"""Generate indian_industries_wave30_facts.py — 30 Malayalam PSC industry topic types."""

from __future__ import annotations

import ast
import importlib.util
import pprint
import random
import sys
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "indian_industries_wave30_facts.py"

HEADER = '''#!/usr/bin/env python3
"""Wave 30 Indian industries facts — 30 Malayalam PSC topic types."""

from __future__ import annotations

import random

from refill_common import Candidate
from wave30_emit import emit_category, emit_direct

'''

EMIT_FOOTER = '''

def generate_wave30_candidates(existing: set[str], rng: random.Random) -> list[Candidate]:
    out: list[Candidate] = []
{emit_body}
    emit_direct(out, existing, rng, DIRECT_FACTS)
    return out


if __name__ == "__main__":
    print(len(generate_wave30_candidates(set(), random.Random(0))))
'''

ENGLISH_CATS = frozenset({
    "ABBREVIATIONS", "PSU_SECTOR", "PSU_HQ", "DEFENCE_PSUS", "REFINERIES", "NODAL_AGENCY",
})


def blr() -> str:
    src = (ROOT / "ii_wave30_data.py").read_text(encoding="utf-8")
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Tuple) and len(node.elts) == 2:
            a, b = node.elts
            if isinstance(a, ast.Constant) and a.value == "ഐ.എസ്.ആർ.ഒ.":
                return b.value
    raise RuntimeError("ISRO HQ / Bengaluru spelling not found in ii_wave30_data.py")


def valiya() -> str:
    src = (ROOT / "continents_wave30_facts.py").read_text(encoding="utf-8")
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if node.value.startswith("ഏറ്റവും വ"):
                return node.value.split()[1]
    return "വലിയ"


def load_build_module():
    spec = importlib.util.spec_from_file_location("bii", ROOT / "_build_indian_industries_wave30.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_psu_rows(B: str) -> list[tuple[str, str, str]]:
    return [
        ("BHEL", "Power equipment", "New Delhi"),
        ("HAL", "Aerospace/Defence", B),
        ("SAIL", "Steel", "New Delhi"),
        ("ONGC", "Oil and gas exploration", "New Delhi"),
        ("NTPC", "Power generation", "New Delhi"),
        ("IOCL", "Oil refining/marketing", "New Delhi"),
        ("Coal India", "Coal mining", "Kolkata"),
        ("GAIL", "Natural gas", "New Delhi"),
        ("NHPC", "Hydro power", "Faridabad"),
        ("BEL", "Defence electronics", B),
        ("BEML", "Heavy equipment", B),
        ("MIDHANI", "Special metals/alloys", "Hyderabad"),
        ("NLC India", "Lignite mining/power", "Neyveli"),
        ("SCI", "Shipping", "Mumbai"),
        ("HPCL", "Oil marketing", "Mumbai"),
        ("BPCL", "Oil marketing", "Mumbai"),
        ("NALCO", "Aluminium", "Bhubaneswar"),
        ("NMDC", "Iron ore", "Hyderabad"),
        ("ECIL", "Electronics", "Hyderabad"),
        ("HCL", "Copper", "Ranchi"),
        ("MOIL", "Manganese", "Nagpur"),
        ("ITI", "Telecom equipment", B),
        ("MTNL", "Telecom", "New Delhi"),
        ("BSNL", "Telecom", "New Delhi"),
        ("Cochin Shipyard", "Shipbuilding", "Kochi"),
        ("Mazagon Dock", "Ships/submarines", "Mumbai"),
        ("GRSE", "Warships", "Kolkata"),
        ("Goa Shipyard", "Shipbuilding", "Vasco da Gama"),
        ("Hindustan Shipyard", "Shipbuilding", "Visakhapatnam"),
        ("BDL", "Guided missiles", "Hyderabad"),
    ]


def fill_remaining(d: dict[str, list[tuple[str, str]]], B: str, V: str) -> None:
    ev = f"ഏറ്റവും {V}"

    d["COMMODITY_BOARD_HQ"] = [
        ("സ്പൈസസ് ബോർഡ്", "കൊച്ചി"), ("റബ്ബർ ബോർഡ്", "കോട്ടയം"), ("ടീ ബോർഡ്", "കൊൽക്കത്ത"),
        ("കോഫി ബോർഡ്", B), ("കോയർ ബോർഡ്", "കൊച്ചി"), ("ടോബാക്കോ ബോർഡ്", "ഗുണ്ടൂർ"),
        ("സെൻട്രൽ സിൽക് ബോർഡ്", B), ("ചവറുക ബോർഡ്", "കൊൽക്കത്ത"), ("പരുത്തി ഉപദേശക ബോർഡ്", "മുംബൈ"),
        ("തേങ്ങാ വികസന ബോർഡ്", "കൊച്ചി"), ("എണ്ണക്കുരു & പയർ ബോർഡ്", "ഇന്ദോർ"),
        ("ദേശീയ ഉദ്യാന ബോർഡ്", "ഗുരുഗ്രാം"), ("കാഷ്യൂ എക്സ്പോർട്ട് പ്രമോഷൻ കൗൺസിൽ", "കൊച്ചി"),
        ("മത്സ്യ ഉൽപ്പന്ന എക്സ്പോർട്ട് വികസന അതോറിറ്റി", "കൊച്ചി"),
        ("കാർഷിക-പ്രോസസ്ഡ് ഫുഡ് എക്സ്പോർട്ട്", "ന്യൂ ഡൽഹി"),
        ("കരകുശല കയറ്റുമതി പ്രമോഷൻ കൗൺസിൽ", "ന്യൂ ഡൽഹി"),
        ("കയറ്റുമതി പരിശോധന കൗൺസിൽ", "ന്യൂ ഡൽഹി"),
        ("എല്ലാ ഇന്ത്യ കരകുശല ബോർഡ്", "ന്യൂ ഡൽഹി"),
        ("സ്പൈസസ് ബോർഡ്", "എറണാകുളം"), ("റബ്ബർ ബോർഡ്", "കോട്ടയം ജില്ല"),
        ("ടീ ബോർഡ്", "പശ്ചിമബംഗാൾ"), ("കോഫി ബോർഡ്", "കർണാടക"),
        ("കോയർ ബോർഡ്", "കേരളം"), ("ടോബാക്കോ ബോർഡ്", "ആന്ധ്രപ്രദേശ്"),
        ("സെൻട്രൽ സിൽക് ബോർഡ്", "കർണാടക"), ("ചവറുക ബോർഡ്", "പശ്ചിമബംഗാൾ"),
        ("പരുത്തി ഉപദേശക ബോർഡ്", "മഹാരാഷ്ട്ര"), ("തേങ്ങാ വികസന ബോർഡ്", "കേരളം"),
        ("എണ്ണക്കുരു & പയർ ബോർഡ്", "മധ്യപ്രദേശ്"), ("ദേശീയ ഉദ്യാന ബോർഡ്", "ഹരിയാന"),
    ]

    d["COMMODITY_PRODUCT"] = [
        ("സ്പൈസസ് ബോർഡ്", "സുഗന്ധവ്യഞ്ജനങ്ങൾ"), ("റബ്ബർ ബോർഡ്", "റബ്ബർ"),
        ("ടീ ബോർഡ്", "ചായ"), ("കോഫി ബോർഡ്", "കാപ്പി"), ("കോയർ ബോർഡ്", "കയർ"),
        ("ടോബാക്കോ ബോർഡ്", "പുകയില"), ("സെൻട്രൽ സിൽക് ബോർഡ്", "പട്ട്"),
        ("ചവറുക ബോർഡ്", "ചവറുക"), ("പരുത്തി ഉപദേശക ബോർഡ്", "പരുത്തി"),
        ("തേങ്ങാ വികസന ബോർഡ്", "തേങ്ങ"), ("എണ്ണക്കുരു & പയർ ബോർഡ്", "എണ്ണക്കുരു & പയർ"),
        ("ദേശീയ ഉദ്യാന ബോർഡ്", "പൂതോട്ടം"), ("കാഷ്യൂ എക്സ്പോർട്ട് പ്രമോഷൻ കൗൺസിൽ", "Malabar nut"),
        ("മത്സ്യ ഉൽപ്പന്ന എക്സ്പോർട്ട് വികസന അതോറിറ്റി", "മത്സ്യം"),
        ("കാർഷിക-പ്രോസസ്ഡ് ഫുഡ് എക്സ്പോർട്ട്", "കാർഷിക-പ്രോസസ്ഡ്"),
        ("കരകുശല കയറ്റുമതി പ്രമോഷൻ കൗൺസിൽ", "കരകുശല വസ്തുക്കൾ"),
        ("കയറ്റുമതി പരിശോധന കൗൺസിൽ", "കയറ്റുമതി നിയന്ത്രണം"),
        ("എല്ലാ ഇന്ത്യ കരകുശല ബോർഡ്", "കരകുശലം"),
        ("സ്പൈസസ് ബോർഡ്", "മസാലകൾ"), ("റബ്ബർ ബോർഡ്", "ലാറ്റക്സ്"),
        ("ടീ ബോർഡ്", "ചായ ഉൽപ്പന്നം"), ("കോഫി ബോർഡ്", "റോബസ്റ്റ"),
        ("കോയർ ബോർഡ്", "കയർ നിർമ്മാണം"), ("ടോബാക്കോ ബോർഡ്", "വിറ്റുപുകയില"),
        ("സെൻട്രൽ സിൽക് ബോർഡ്", "രേഷ്മ"), ("ചവറുക ബോർഡ്", "ചവറുപ്പിർ"),
        ("പരുത്തി ഉപദേശക ബോർഡ്", "പരുത്തി നൂൽ"), ("തേങ്ങാ വികസന ബോർഡ്", "തേങ്ങാപ്പം"),
        ("എണ്ണക്കുരു & പയർ ബോർഡ്", "എണ്ണക്കുരു"), ("ദേശീയ ഉദ്യാന ബോർഡ്", "പൂക്കൾ"),
        ("കാഷ്യൂ എക്സ്പോർട്ട് പ്രമോഷൻ കൗൺസിൽ", "Malabar nut"),
    ]

    d["REFINERIES"] = [
        ("Jamnagar Refinery", "Reliance"), ("Jamnagar Refinery", ev),
        ("Panipat Refinery", "IOCL"), ("Panipat Refinery", "Haryana"),
        ("Kochi Refinery", "BPCL"), ("Kochi Refinery", "Kerala"),
        ("Vadinar Refinery", "Nayara Energy"), ("Vadinar Refinery", "Gujarat"),
        ("Digboi Refinery", "First refinery"), ("Digboi Refinery", "Assam"),
        ("Numaligarh Refinery", "NRL"), ("Numaligarh Refinery", "Assam"),
        ("Paradip Refinery", "IOCL"), ("Paradip Refinery", "Odisha"),
        ("Barauni Refinery", "IOCL"), ("Barauni Refinery", "Bihar"),
        ("Haldia Refinery", "IOC"), ("Haldia Refinery", "West Bengal"),
        ("Mangalore Refinery", "MRPL"), ("Mangalore Refinery", "Karnataka"),
        ("Visakh Refinery", "HPCL"), ("Visakh Refinery", "Andhra Pradesh"),
        ("Mathura Refinery", "IOCL"), ("Mathura Refinery", "Uttar Pradesh"),
        ("Bina Refinery", "BPCL"), ("Bina Refinery", "Madhya Pradesh"),
        ("Tatipaka Refinery", "ONGC"), ("Tatipaka Refinery", "Andhra Pradesh"),
        ("Manali Refinery", "CPCL"), ("Manali Refinery", "Tamil Nadu"),
    ]

    d["MAJOR_PORTS"] = [
        ("ജെ.എൻ.പി.ടി.", f"{ev} കണ്ടെയ്\u200cനർ തുറമുഖം"), ("ജെ.എൻ.പി.ടി.", "മഹാരാഷ്ട്ര"),
        ("മുണ്ട്ര തുറമുഖം", f"{ev} സ്വകാര്യ തുറമുഖം"), ("മുണ്ട്ര തുറമുഖം", "ഗുജറാത്ത്"),
        ("ചെന്നൈ തുറമുഖം", "തമിഴ്നാട്"), ("കൊച്ചി തുറമുഖം", "കേരളം"),
        ("വിശാഖ തുറമുഖം", "ആന്ധ്രപ്രദേശ്"), ("കൊൽക്കത്ത തുറമുഖം", "പശ്ചിമബംഗാൾ"),
        ("പാരദീപ് തുറമുഖം", "ഒഡിഷ"), ("കാന്ദ്ല തുറമുഖം", "ഗുജറാത്ത്"),
        ("മുംബൈ തുറമുഖം", "മഹാരാഷ്ട്ര"), ("എന്നോർ തുറമുഖം", "തമിഴ്നാട്"),
        ("തൂത്തുക്കുദി തുറമുഖം", "തമിഴ്നാട്"), ("മോർമുഗാവോ തുറമുഖം", "ഗോവ"),
        ("ന്യൂ മംഗലൂർ തുറമുഖം", "കർണാടക"), ("ഹാൽദിയ തുറമുഖം", "പശ്ചിമബംഗാൾ"),
        ("ദീൻദയാൽ തുറമുഖം", "കാന്ദ്ല"), ("വി.ഒ. ചിദമ്പരനാർ", "തൂത്തുക്കുദി"),
        ("കൊച്ചി പോർട്ട് ട്രസ്റ്റ്", "കേരളം"), ("ചെന്നൈ പോർട്ട് ട്രസ്റ്റ്", "തമിഴ്നാട്"),
        ("ജawaharlal Nehru Port", "മഹാരാഷ്ട്ര"), ("മundra Port", "ഗുജറാത്ത്"),
        ("വിശാഖപട്ടണം പോർട്ട്", "കിഴക്കൻ തീരം"), ("കolkata Port", "ഹൂഗ്ലി"),
        ("പaradip Port", "ഒഡിഷ"), ("കandla Port", "ഗുജറാത്ത്"),
        ("മumbai Port", "മഹാരാഷ്ട്ര"), ("എnnore Port", "തമിഴ്നാട്"),
        ("തuticorin Port", "തമിഴ്നാട്"), ("മormugao Port", "ഗോവ"),
    ]

    d["CLUSTER_NICKNAME"] = [
        (B, "ഇന്ത്യയുടെ സിലിക്കൺ വാലി"), ("ചെന്നൈ", "ഇന്ത്യയുടെ ഡിട്രോയിറ്റ്"),
        ("മുംബൈ", "വാണിജ്യ തലസ്ഥാനം"), ("സൂറത്ത്", "വജ്ര നഗരം"),
        ("ജയ്പൂർ", "പിങ്ക് സിറ്റി"), ("ഹൈദരാബാദ്", "ബൾക്ക് ഡ്രഗ് തൽസ്ഥാനം"),
        ("കാൻപൂർ", "ലെതർ സിറ്റി"), ("തിരുപ്പൂർ", "നിറ്റ്വെയർ നഗരം"),
        ("മോറാദാബാദ്", "പിത്തള നഗരം"), ("ഫരീദാബാദ്", "ഓട്ടോമൊബൈൽ ഹബ്"),
        ("പുണെ", "ഓട്ടോമൊബൈൽ & IT"), ("അഹമദാബാദ്", "ടെക്സ്റ്റൈൽ & ഡയമണ്ട്"),
        ("ലുധിയാന", "മെഷീൻ ടൂൾസ്"), ("കൊച്ചി", "സുഗന്ധവ്യഞ്ജന ഹബ്"),
        ("കൊൽക്കത്ത", "കിഴക്കൻ ഇന്ത്യ ഹബ്"), ("നോയിഡ", "ഇലക്ട്രോണിക്സ് ഹബ്"),
        ("ഗurgaon", "IT & BPO"), ("വിശാഖപട്ടണം", "ഉരുക്ക് & തുറമുഖ നഗരം"),
        ("രourkela", "ഉരുക്ക് നഗരം"), ("ഭilai", "ഉരുക്ക് പ്ലാന്റ് നഗരം"),
        ("ജamshedpur", "ഉരുക്ക് നഗരം"), ("കanpur", "ലെതർ ക്ലസ്റ്റർ"),
        (B, "IT തലസ്ഥാനം"), ("ചennai", "ഓട്ടോ ഹബ്"), ("സurat", "വജ്രം മുറിക്കൽ"),
        ("ഹyderabad", "ഫാർമ തലസ്ഥാനം"), ("തiruppur", "നിറ്റ്വെയർ കയറ്റുമതി"),
        ("മoradabad", "പിത്തള കരകുശലം"), ("പune", "ഓട്ടോമൊബൈൽ നിർമ്മാണം"),
        ("അhmedabad", "ടെക്സ്റ്റൈൽ ഹബ്"),
    ]

    d["CLUSTER_SPECIALTY"] = [
        ("തിരുപ്പൂർ", "നിറ്റ്വെയർ"), ("സൂറത്ത്", "വജ്രം"), ("മോറാദാബാദ്", "പിത്തള"),
        ("കാൻപൂർ", "തുകൽ"), ("വാരanasi", "പട്ട്"), ("ഭopal", "ഭാരമുള്ള ഇലക്ട്രിക്കൽസ്"),
        ("രourkela", "ഉരുക്ക്"), ("ഭilai", "ഉരുക്ക്"), ("ജamshedpur", "ഉരുക്ക്"),
        ("ഹൈദരാബാദ്", "ബൾക്ക് ഡ്രഗ്"), ("ബaddi", "ഫാർമ"), ("അhmedabad", "ടെക്സ്റ്റൈൽ"),
        ("ലudhiana", "സൈക്കിളുകൾ"), ("അgra", "പാദരക്ഷ"), ("ഫirozabad", "ഗ്ലാസ് ബാങ്ങിളുകൾ"),
        ("കolhapur", "കോലhapuri ചappal"), ("പanipat", "ടെക്സ്റ്റൈൽ"), ("ഇndore", "ഓട്ടോമൊബൈൽ"),
        ("ചandigarh", "ലൈറ്റ് എഞ്ചിനീയറിംഗ്"), ("കochi", "കപ്പൽ നിർമ്മാണം"),
        ("വisakhapatnam", "ഉരുക്ക് & കപ്പൽ"), ("നagpur", "ഓറഞ്ച് & ടെക്സ്റ്റൈൽ"),
        ("കanpur", "ലെതർ ഉൽപ്പന്നങ്ങൾ"), ("മoradabad", "പിത്തള കരകുശലം"),
        ("തiruppur", "നിറ്റ്വെയർ കയറ്റുമതി"), ("സurat", "സിന്തetic ടെക്സ്റ്റൈൽ"),
        ("ജodhpur", "കരകുശലം"), ("കashmir", "പരിപ്പുകൾ"), ("അhmedabad", "ഡെനിം"),
        ("പune", "ഓട്ടോമൊബൈൽ"), ("ചennai", "ഓട്ടോമൊബൈൽ അസംബ്ലി"),
    ]

    d["HANDICRAFTS"] = [
        ("മോറാദാബാദ്", "പിത്തള"), ("വാരanasi", "പട്ട്"), ("ജodhpur", "തുകൽ"),
        ("കashmir", "പരിപ്പുകൾ"), ("അgra", "മാർബിൾ ഇൻലേ"), ("ഫirozabad", "ഗ്ലാസ്"),
        ("സaharanpur", "മരം കൊത്ത്"), ("കutch", "എംബroidery"), ("പuri", "അപ്ലിക്ക്"),
        ("ഭubaneswar", "പattachitra"), ("കonark", "കല്ല് കൊത്ത്"),
        ("മadhubani", "ചിത്രങ്ങൾ"), ("ബardhaman", "Dokra"), ("മanipur", "Kauna craft"),
        ("നagaland", "Naga shawls"), ("മizoram", "Bamboo"), ("അssam", "പട്ട്"),
        ("കerala", "കയർ ഉൽപ്പന്നങ്ങൾ"), ("തamil Nadu", "വെങ്കല പ്രതിമകൾ"),
        ("രajasthan", "Blue pottery"), ("Gujarat", "Bandhani"), ("Punjab", "Phulkari"),
        ("West Bengal", "Kantha"), ("Odisha", "Silver filigree"),
        ("Uttar Pradesh", "Chikan work"), ("Himachal", "Woolen shawls"),
        ("Karnataka", "Sandalwood"), ("Maharashtra", "Warli art"),
        ("Bihar", "Sujini embroidery"), ("Tripura", "Cane & bamboo"),
    ]

    d["TEXTILES"] = [
        ("തിരുപ്പൂർ", "നിറ്റ്വെയർ"), ("സൂറത്ത്", "സynthetics"), ("കanpur", "Cotton"),
        ("അhmedabad", "Denim"), ("പanipat", "Home textiles"), ("ഭagalpur", "Silk"),
        ("ഇchalkaranji", "Powerloom"), ("Coimbatore", "Spinning"), ("Erode", "Turmeric & textiles"),
        ("Tirupur", "Knitwear exports"), ("Ludhiana", "Woolen"), ("Bhiwandi", "Powerloom"),
        ("Solapur", "Chaddar"), ("Kolhapur", "Cotton"), ("Malwa", "Cotton belt"),
        ("Surat", "Man-made fibre"), ("Varanasi", "Banarasi silk"),
        ("Kanchipuram", "Silk sarees"), ("Pochampally", "Ikat"), ("Chanderi", "Silk-cotton"),
        ("Maheshwar", "Handloom"), ("Balarampur", "Jute"), ("Kolkata", "Jute mills"),
        ("Mumbai", "Cotton mills legacy"), ("Ahmedabad", "Textile mills"),
        ("Coimbatore", "Yarn"), ("Madurai", "Handloom"), ("Rajasthan", "Block print"),
        ("Gujarat", "Patola"), ("West Bengal", "Muslin heritage"),
    ]

    d["PHARMA"] = [
        ("ഹൈദരാബാദ്", "Bulk drugs"), ("ബaddi", "Formulations"), ("അhmedabad", "API"),
        ("വisakhapatnam", "Pharma SEZ"), ("പune", "Formulations"), ("മumbai", "Pharma HQ"),
        ("Chennai", "Vaccines"), ("Goa", "Pharma units"), ("Indore", "Pharma park"),
        ("Hyderabad", "Vaccine hub"), ("Telangana", "Pharma policy"), ("Gujarat", "Pharma cluster"),
        ("Maharashtra", "Pharma exports"), ("Karnataka", "Biotech"), ("Tamil Nadu", "Pharma"),
        ("Uttarakhand", "Pharma hub"), ("Himachal", "Tax incentives"), ("Sikkim", "Pharma units"),
        ("Delhi NCR", "Pharma marketing"), ("Ankleshwar", "API"), ("Vapi", "Bulk drugs"),
        ("Baddi", "Contract manufacturing"), ("Hyderabad", "Genome Valley"),
        ("Ahmedabad", "Pharma formulations"), ("Visakh", "Pharma city"),
        ("Mumbai", "Pharma R&D"), ("Pune", "Vaccine manufacturing"),
        ("Bangalore", "Biotech"), ("Chennai", "Pharma exports"),
        ("India", "Pharmacy of the world"),
    ]

    d["DEFENCE_PSUS"] = [
        ("HAL", "Aircraft"), ("BEL", "Defence electronics"), ("BDL", "Missiles"),
        ("BEML", "Earth movers"), ("MDL", "Submarines"), ("GRSE", "Warships"),
        ("GSL", "Patrol vessels"), ("HSL", "Ship repair"), ("DDPD", "Ordnance factories"),
        ("Mazagon Dock", "Warships"), ("Cochin Shipyard", "Aircraft carrier"),
        ("Bharat Forge", "Artillery"), ("HAL", "Tejas"), ("BEL", "Radars"),
        ("BDL", "Akash missile"), ("BEML", "Tatra vehicles"), ("MDL", "Scorpene subs"),
        ("GRSE", "Frigates"), ("GSL", "Offshore patrol"), ("HSL", "Visakhapatnam"),
        ("HAL", "Dhruv helicopter"), ("BEL", "Sonar systems"), ("BDL", "Pinaka"),
        ("BEML", "Rail coaches"), ("MDL", "Mumbai"), ("GRSE", "Kolkata"),
        ("HAL", "Bangalore HQ"), ("BEL", "Bangalore"), ("BDL", "Hyderabad"),
    ]

    d["FIRST_MILLS"] = [
        ("ആദ്യ കോട്ടൺ മിൽ", "1854"), ("ആദ്യ കോട്ടൺ മിൽ", "മുംബൈ"),
        ("ആദ്യ ജൂട് മിൽ", "1855"), ("ആദ്യ ജൂട് മിൽ", "റിശ്ര"),
        ("ടാറ്റാ സ്റ്റീൽ", "1907"), ("ടാറ്റാ സ്റ്റീൽ", "ജാംഷേഡ്പൂർ"),
        ("ആദ്യ റിഫൈനറി", "ഡിഗ്ബോയ്"), ("ആദ്യ റിഫൈനറി", "1901"),
        ("ആദ്യ IT പാർക്ക്", "SEEPZ"), ("ആദ്യ IT പാർക്ക്", "മുംബൈ"),
        ("ആദ്യ EPZ", "കാന്ദ്ല"), ("ആദ്യ EPZ", "1965"),
        ("ആദ്യ സ്റ്റീൽ പ്ലാന്റ്", "ടാറ്റാ"), ("ആദ്യ സ്റ്റീൽ പ്ലാന്റ്", "1907"),
        ("ആദ്യ ഓട്ടോമൊബൈൽ", "ഹിന്ദുസ്ഥാൻ മോട്ടോഴ്സ്"), ("ആദ്യ ഓട്ടോമൊബൈൽ", "1942"),
        ("ആദ്യ ടെക്സ്റ്റൈൽ മിൽ", "മumbai"), ("ആദ്യ സarkar steel", "ഭilai"),
        ("ആദ്യ സarkar steel", "1959"), ("SAIL", "1954"),
        ("BHEL", "1964"), ("NTPC", "1975"), ("ONGC", "1956"),
        ("Indian Oil", "1959"), ("HMT", "1953"), ("BEL", "1954"),
        ("HAL", "1940"), ("Maruti", "1983"), ("TISCO", "Jamshedpur"),
        ("First jute mill", "Rishra"), ("First cotton mill", "Mumbai"),
    ]

    d["COOPERATIVE"] = [
        ("ആമുൽ", "പാലുൽപ്പന്നങ്ങൾ"), ("ആമുൽ", "ആനന്ദ്"), ("IFFCO", "വളം"),
        ("NAFED", "കാർഷിക മാർക്കറ്റിംഗ്"), ("KRIBHCO", "വളം"), ("NCUI", "സഹകരണ സംഘടന"),
        ("NDDB", "Dairy development"), ("GCMMF", "Amul federation"),
        ("Kerala Co-op Bank", "Banking"), ("Uralungal LAB", "Construction co-op"),
        ("Indian Coffee House", "Coffee co-op"), ("Lijjat Papad", "Women co-op"),
        ("SEWA", "Self-employed women"), ("Sahakar Bharati", "Co-op movement"),
        ("Amul", "White Revolution"), ("IFFCO", "Kalol Gujarat"),
        ("NAFED", "Oilseeds marketing"), ("KRIBHCO", "Fertilizer co-op"),
        ("NDDB", "Operation Flood"), ("GCMMF", "Anand model"),
        ("Cooperative sugar", "Maharashtra"), ("Milk co-ops", "Gujarat"),
        ("Fishermen co-ops", "Kerala"), ("Handloom co-ops", "Tamil Nadu"),
        ("Urban co-op banks", "Maharashtra"), ("Credit co-ops", "Karnataka"),
        ("Amul", "Dr Verghese Kurien"), ("IFFCO", "Farmers co-op"),
        ("NAFED", "Central nodal agency"), ("KRIBHCO", "Krishak Bharati"),
    ]

    d["ODOP"] = [
        ("One District One Product", "2018"), ("ODOP", "Commerce Ministry"),
        ("Varanasi", "Banarasi silk"), ("Moradabad", "Brassware"),
        ("Bhadohi", "Carpets"), ("Kanpur", "Leather"), ("Agra", "Footwear"),
        ("Lucknow", "Chikan"), ("Saharanpur", "Wood craft"), ("Meerut", "Sports goods"),
        ("Kerala", "Coir"), ("Tamil Nadu", "Brass"), ("Gujarat", "Bandhani"),
        ("Rajasthan", "Blue pottery"), ("Odisha", "Pattachitra"),
        ("West Bengal", "Kantha"), ("Assam", "Muga silk"), ("Kashmir", "Pashmina"),
        ("Punjab", "Phulkari"), ("Himachal", "Shawls"), ("Uttarakhand", "Handicrafts"),
        ("ODOP", "Export promotion"), ("ODOP", "District branding"),
        ("ODOP", "MSME linkage"), ("ODOP", "GI products focus"),
        ("ODOP", "State participation"), ("ODOP", "E-commerce linkage"),
        ("ODOP", "Skill development"), ("ODOP", "Marketing support"),
        ("ODOP", "District specific product"), ("ODOP", "2018 launch"),
    ]

    d["RENEWABLE_ENERGY"] = [
        ("SECI", "Solar trading"), ("IREDA", "Green finance"), ("NTPC Renewable", "Solar/wind"),
        ("NHPC", "Hydro power"), ("SJVN", "Hydro"), ("Green Energy Corridor", "Grid integration"),
        ("National Solar Mission", "2010"), ("National Wind Mission", "Wind power"),
        ("PM-KUSUM", "Solar pumps"), ("FAME", "EV adoption"), ("PLI solar", "PV modules"),
        ("Green Hydrogen Mission", "2023"), ("Offshore wind policy", "Coastal wind"),
        ("RPO", "Renewable purchase obligation"), ("CERC", "Tariff regulation"),
        ("MNRE", "Nodal ministry"), ("SECI", "Central nodal agency"),
        ("IREDA", "1987 establishment"), ("Solar park scheme", "Large solar"),
        ("Wind-solar hybrid", "Hybrid parks"), ("Biomass power", "Rural energy"),
        ("Small hydro", "Below 25 MW"), ("Rooftop solar", "Urban solar"),
        ("Koyna", "Maharashtra hydro"), ("Tehri", "Uttarakhand hydro"),
        ("Sardar Sarovar", "Gujarat hydro"), ("NHPC", "Faridabad HQ"),
        ("SJVN", "Shimla HQ"), ("SECI", "New Delhi"),
        ("IREDA", "New Delhi"),
    ]

    d["SHIPYARDS"] = [
        ("Cochin Shipyard", "Kochi"), ("Mazagon Dock", "Mumbai"),
        ("GRSE", "Kolkata"), ("Goa Shipyard", "Vasco da Gama"),
        ("Hindustan Shipyard", "Visakhapatnam"), ("Cochin Shipyard", "Aircraft carrier"),
        ("Mazagon Dock", "Destroyers"), ("GRSE", "Frigates"),
        ("Goa Shipyard", "Offshore patrol"), ("HSL", "Ship repair"),
        ("Cochin Shipyard", "PSU"), ("Mazagon Dock", "Submarines"),
        ("GRSE", "PSU Kolkata"), ("Goa Shipyard", "PSU Goa"),
        ("Hindustan Shipyard", "PSU Vizag"), ("Cochin Shipyard", "1981"),
        ("Mazagon Dock", "1934"), ("GRSE", "1934"),
        ("Goa Shipyard", "1957"), ("Hindustan Shipyard", "1952"),
        ("Cochin Shipyard", "Largest PSU shipyard"), ("MDL", "Mumbai submarines"),
        ("CSL", "IAC Vikrant"), ("GRSE", "Anti-submarine warfare"),
        ("GSL", "Goa patrol vessels"), ("HSL", "Visakh repair"),
        ("Shipbuilding financial aid", "2016"), ("Make in India ships", "Defence"),
        ("Sagarmala", "Port-led development"), ("Cochin Shipyard", "Export ships"),
    ]

    d["STEEL_PLANTS"] = [
        ("Bhilai Steel Plant", "SAIL"), ("Bokaro Steel Plant", "SAIL"),
        ("Rourkela Steel Plant", "SAIL"), ("Durgapur Steel Plant", "SAIL"),
        ("Burnpur IISCO", "SAIL"), ("Tata Steel Jamshedpur", "Private"),
        ("Vizag Steel (RINL)", "PSU"), ("JSW Steel", "Private"),
        ("Essar Steel", "Private"), ("Bhilai", "Chhattisgarh"),
        ("Bokaro", "Jharkhand"), ("Rourkela", "Odisha"),
        ("Durgapur", "West Bengal"), ("Jamshedpur", "Jharkhand"),
        ("Visakhapatnam", "Andhra Pradesh"), ("SAIL", "1954"),
        ("TISCO", "1907"), ("RINL", "1982"), ("Bhilai", "USSR collaboration"),
        ("Bokaro", "Soviet help"), ("Rourkela", "German collaboration"),
        ("Durgapur", "British collaboration"), ("Steel Authority", "Maharatna"),
        ("National Steel Policy", "2017"), ("Domestic steel capacity", "150 MT target"),
        ("Pellet plants", "Iron ore"), ("Coking coal import", "Steel input"),
        ("Jamshedpur", "First integrated plant"), ("Visakh", "Coastal plant"),
        ("SAIL", "New Delhi HQ"),
    ]

    d["AUTOMOBILE"] = [
        ("Maruti Suzuki", "Gurgaon/Manesar"), ("Hyundai", "Chennai"),
        ("Tata Motors", "Pune/Jamshedpur"), ("Mahindra", "Chennai/Pune"),
        ("Honda", "Rajasthan"), ("Toyota", "Karnataka"),
        ("Ford (legacy)", "Chennai"), ("Renault-Nissan", "Chennai"),
        ("Ashok Leyland", "Chennai"), ("TVS", "Hosur"),
        ("Bajaj Auto", "Pune"), ("Hero", "Gurgaon"),
        ("Royal Enfield", "Chennai"), ("Force Motors", "Pune"),
        ("Chennai", "Detroit of India"), ("Pune", "Auto hub"),
        ("Gurgaon", "Maruti hub"), ("Sanand", "Gujarat auto"),
        ("Hosur", "Two-wheeler"), ("Pantnagar", "Uttarakhand"),
        ("Automotive PLI", "2020"), ("FAME II", "EV subsidy"),
        ("National Automotive Policy", "Draft"), ("Auto components", "Chennai cluster"),
        ("EV manufacturing", "Tamil Nadu"), ("Battery PLI", "2021"),
        ("Maruti", "1983 JV"), ("Hyundai", "1996"), ("Tata Nano", "Sanand"),
        ("Auto export hub", "Chennai port"), ("Make in India auto", "FDI"),
    ]

    d["PETROCHEMICAL"] = [
        ("Panipat", "Haryana hub"), ("Dahej", "Gujarat"), ("Hazira", "Gujarat"),
        ("Haldia", "West Bengal"), ("Vadodara", "Gujarat"), ("Nagapattinam", "Tamil Nadu"),
        ("Paradip", "Odisha"), ("Mangalore", "Karnataka"), ("Bongaigaon", "Assam"),
        ("Auraiya", "Uttar Pradesh"), ("GAIL", "Gas pipeline"), ("ONGC petro", "Dahej"),
        ("Reliance Jamnagar", "Integrated refinery-petrochemical"), ("IOCL Panipat", "Naphtha cracker"),
        ("BPCL Kochi", "Propylene derivatives"), ("Haldia Petrochemicals", "West Bengal"),
        ("Gujarat PCPIR", "Dahej-Vadodara"), ("Visakh PCPIR", "Andhra"), ("Paradip PCPIR", "Odisha"),
        ("CMTC", "Chemicals ministry"), ("Petrochemical industry", "Import substitution"),
        ("Polymer production", "Reliance leader"), ("Fertilizer from petrochemical", "Ammonia"),
        ("LPG bottling", "IOCL/HPCL"), ("Bitumen", "Road construction"),
        ("Lubricants", "IOCL"), ("Synthetic rubber", "Petrochemical"),
        ("PTA/PET", "Polyester chain"), ("Methanol", "Chemical feedstock"),
        ("Panipat refinery", "Northern hub"),
    ]

    d["NODAL_AGENCY"] = [
        ("Make in India", "DPIIT"), ("PLI scheme", "DPIIT"),
        ("NICDP", "DPIIT"), ("Industrial corridors", "NICDC"),
        ("SEZ policy", "DPIIT"), ("Startup India", "DPIIT"),
        ("MSME policy", "Ministry of MSME"), ("Udyam registration", "MSME Ministry"),
        ("National Manufacturing Policy", "DPIIT"), ("FAME", "Heavy Industries"),
        ("National Steel Policy", "Steel Ministry"), ("Coal India", "Coal Ministry"),
        ("ONGC", "Petroleum Ministry"), ("NTPC", "Power Ministry"),
        ("Renewable energy", "MNRE"), ("Green Hydrogen Mission", "MNRE"),
        ("ODOP", "Commerce Ministry"), ("Export promotion", "DGFT"),
        ("STPI", "Electronics & IT"), ("Software exports", "MEITY"),
        ("Pharma policy", "Chemicals & Fertilizers"), ("Textile policy", "Textile Ministry"),
        ("Defence production", "Defence Ministry"), ("Shipbuilding policy", "Shipping Ministry"),
        ("Automotive policy", "Heavy Industries"), ("Food processing", "Food Processing Ministry"),
        ("Khadi & Village", "MSME Ministry"), ("Coir board", "MSME Ministry"),
        ("National Industrial Corridor", "DPIIT"), ("Invest India", "DPIIT"),
    ]

    d["ABBREVIATIONS"] = [
        ("DPIIT", "Department for Promotion of Industry and Internal Trade"),
        ("MSME", "Micro Small and Medium Enterprises"),
        ("SEZ", "Special Economic Zone"),
        ("PLI", "Production Linked Incentive"),
        ("PSU", "Public Sector Undertaking"),
        ("SAIL", "Steel Authority of India Limited"),
        ("BHEL", "Bharat Heavy Electricals Limited"),
        ("HAL", "Hindustan Aeronautics Limited"),
        ("ONGC", "Oil and Natural Gas Corporation"),
        ("NTPC", "National Thermal Power Corporation"),
        ("IOCL", "Indian Oil Corporation Limited"),
        ("GAIL", "Gas Authority of India Limited"),
        ("NIMZ", "National Investment and Manufacturing Zone"),
        ("NICDC", "National Industrial Corridor Development Corporation"),
        ("NICDP", "National Industrial Corridor Development Programme"),
        ("DMIC", "Delhi Mumbai Industrial Corridor"),
        ("EPZ", "Export Processing Zone"),
        ("STPI", "Software Technology Parks of India"),
        ("KVIC", "Khadi and Village Industries Commission"),
        ("SIDBI", "Small Industries Development Bank of India"),
        ("NSIC", "National Small Industries Corporation"),
        ("MUDRA", "Micro Units Development and Refinance Agency"),
        ("ODOP", "One District One Product"),
        ("SECI", "Solar Energy Corporation of India"),
        ("IREDA", "Indian Renewable Energy Development Agency"),
        ("MRPL", "Mangalore Refinery and Petrochemicals Limited"),
        ("HPCL", "Hindustan Petroleum Corporation Limited"),
        ("BPCL", "Bharat Petroleum Corporation Limited"),
        ("NRL", "Numaligarh Refinery Limited"),
        ("RINL", "Rashtriya Ispat Nigam Limited"),
    ]


def build_direct_facts(B: str, V: str) -> list[tuple[str, str, list[str], str]]:
    ev = f"ഏറ്റവും {V}"
    return [
        ("മേക്ക് ഇൻ ഇന്ത്യ ലോഗോയിലെ മൃഗം?", "സിംഹം", ["പുലി", "ആന", "മയിൽ"], "easy"),
        ("ദില്ലി-മുംബൈ വ്യവസായി കോറിഡോറിന്റെ ഏകദേശ ദൈർഘ്യം?", "1500 കി.മീ.", ["500 കി.മീ.", "3000 കി.മീ.", "200 കി.മീ."], "hard"),
        (f"ചെന്നൈ-{B} വ്യവസായി കോറിഡോർ ഏതിന്റെ ഭാഗമാണ്?", "ഈസ്റ്റ് കോസ്റ്റ് ഇക്കണോമിക് കോറിഡോർ", ["DMIC മാത്രം", "ഒന്നുമില്ല", "ഹിമാലയൻ കോറിഡോർ"], "hard"),
        ("അമൃത്സർ-കൊൽക്കത്ത വ്യവസായി കോറിഡോർ ഏതിനൊപ്പം വിന്യസിച്ചിരിക്കുന്നു?", "ഈസ്റ്റേൺ ഡെഡിക്കേറ്റഡ് ഫ്രൈറ്റ് കോറിഡോർ", ["വെസ്റ്റേൺ DFC മാത്രം", "കോസ്റ്റൽ റോഡ്", "ഒന്നുമില്ല"], "hard"),
        ("വിശാഖപട്ടണം-ചെന്നൈ വ്യവസായി കോറിഡോർ പ്രധാനമായും ഏത് സംസ്ഥാനത്തിൽ?", "ആന്ധ്രപ്രദേശ്", ["പഞ്ചാബ്", "രാജസ്ഥാൻ", "കേരളം"], "hard"),
        (f"{B}-മുംബൈ വ്യവസായി കോറിഡോർ ഏത് സംസ്ഥാനങ്ങൾ ഉൾക്കൊള്ളുന്നു?", "കർണാടകയും മഹാരാഷ്ട്രയും", ["കേരളം മാത്രം", "അസം മാത്രം", "പഞ്ചാബ് മാത്രം"], "hard"),
        ("ദേശീയ നിർമ്മാണ നയത്തിന്റെ ജിഡിപി ലക്ഷ്യം?", "25%", ["10%", "50%", "5%"], "hard"),
        ("ഫാർമ മേഖല 'ലോകത്തിന്റെ ഫാർമസി' എന്ന് ഏത് രാജ്യത്തെ സൂചിപ്പിക്കുന്നു?", "ഇന്ത്യ", ["അമേരിക്ക", "ജപ്പാൻ", "ബ്രസീൽ"], "medium"),
        (f"{B} ഐടി നാഗരികതയുടെ വിളിപ്പേര്?", "ഇന്ത്യയുടെ സിലിക്കൺ വാലി", ["ഇന്ത്യയുടെ ഡിട്രോയിറ്റ്", "സ്റ്റീൽ നഗരം", "പിങ്ക് നഗരം"], "easy"),
        ("ഇന്ത്യയുടെ ഡിട്രോയിറ്റ് എന്ന് സാധാരണയായി ഏതിനെ സൂചിപ്പിക്കുന്നു?", "ചെന്നൈ (ഓട്ടോമൊബൈൽ)", ["ജയ്പൂർ", "ഷിമ്ല", "പണാജി"], "medium"),
        (f"ഇന്ത്യയിലെ {ev} റിഫൈനറി (ജാംനഗർ) ഉടമസ്ഥൻ?", "റിലയൻസ്", ["ONGC മാത്രം", "SAIL", "HAL"], "medium"),
        ("സ്റ്റീൽ അതോറിറ്റി ഓഫ് ഇന്ത്യ ആസ്ഥാനം?", "ന്യൂ ഡൽഹി", ["മുംബൈ", "കൊൽക്കത്ത", "ചെന്നൈ"], "hard"),
        (f"ഹിന്ദുസ്ഥാൻ ഏരോനോട്ടിക്സ് ലിമിറ്റഡ് (HAL) ആസ്ഥാനം?", B, ["മുംബൈ", "ഡൽഹി", "കൊൽക്കത്ത"], "medium"),
        (f"ഭാരത് ഇലക്ട്രോണിക്സ് ലിമിറ്റഡ് (BEL) ആസ്ഥാനം?", B, ["മുംബൈ", "ചെന്നൈ", "കൊൽക്കത്ത"], "hard"),
        ("നാഷണൽ അൽമിനിയം കമ്പനി (NALCO) ആസ്ഥാനം?", "ഭുവനേശ്വർ", ["ഡൽഹി", "മുംബൈ", "ചെന്നൈ"], "hard"),
        ("ഹിന്ദുസ്ഥാൻ പെട്രോളിയം ആസ്ഥാന നഗരം?", "മുംബൈ", ["ഡൽഹി", "ചെന്നൈ", "കൊൽക്കത്ത"], "hard"),
        ("മാരുതി സുസുക്കി നിർമ്മാണം പ്രധാനമായും എവിടെ?", "ഹരിയാന/ഗുജറാത്ത്", ["കേരളം", "അസം മാത്രം", "ഗോവ മാത്രം"], "medium"),
        ("ടാറ്റാ സ്റ്റീൽ പ്രധാന പ്ലാന്റ് എവിടെ?", "ജാംഷേഡ്പൂർ", ["ജയ്പൂർ", "ഷിമ്ല", "പണാജി"], "medium"),
        ("തിരുപ്പൂർ ഏതിന് പ്രസിദ്ധമാണ്?", "നിറ്റ്വെയർ കയറ്റുമതി", ["കൽക്കരി", "എണ്ണ ശുദ്ധീകരണം", "അന്തരീക്ഷം"], "hard"),
        ("ഇന്ത്യയിലെ വജ്രം മുറിക്കൽ കേന്ദ്രം?", "സൂറത്ത്", ["ജയ്പൂർ മാത്രം", "ഷിമ്ല", "പണാജി"], "hard"),
        ("തുകൽ വ്യവസായി കേന്ദ്രം?", "കാൻപൂർ/ചെന്നൈ", ["ഷിമ്ല", "ഗംഗ്ടോക്", "പണാജി"], "hard"),
        ("SEZ നയം ഇന്ത്യയിൽ പ്രഖ്യാപിച്ച വർഷം?", "2000", ["1990", "2010", "1985"], "hard"),
        ("PLI പദ്ധതിയുടെ ആദ്യ മേഖള?", "മൊബൈൽ നിർമ്മാണം", ["കൽക്കരി", "മത്സ്യബന്ധനം", "സിനിമ"], "hard"),
        ("ദേശീയ വ്യവസായി കോറിഡോർ വികസന പരിപാടിയുടെ നോഡൽ?", "DPIIT", ["പ്രതിരോധ മന്ത്രാലയം", "വിദേശകാര്യം", "ആഭ്യന്തരം"], "hard"),
        ("ഖാദി & വില്ലേജ് ഇൻഡസ്ട്രി കമ്മീഷൻ (KVIC) എന്തിനാണ്?", "ഗ്രാമീണ വ്യവസായി", ["പ്രതിരോധം", "അന്തരീക്ഷം", "സിനിമ മാത്രം"], "medium"),
        ("കയർ വ്യവസായി പ്രധാന സംസ്ഥാനം?", "കേരളം", ["പഞ്ചാബ്", "രാജസ്ഥാൻ", "ഹിമാചൽ"], "easy"),
        ("സ്പൈസസ് ബോർഡ് ആസ്ഥാനം?", "കൊച്ചി", ["ഡൽഹി", "മുംബൈ", "ചെന്നൈ"], "hard"),
        ("റബ്ബർ ബോർഡ് ആസ്ഥാനം?", "കോട്ടയം", ["ഡൽഹി", "മുംബൈ", "ചെന്നൈ"], "hard"),
        ("ടീ ബോർഡ് ആസ്ഥാനം?", "കൊൽക്കത്ത", ["കൊച്ചി", "ഡൽഹി", "ചെന്നൈ"], "hard"),
        (f"കോഫി ബോർഡ് ആസ്ഥാനം?", B, ["കൊച്ചി", "ഡൽഹി", "മുംബൈ"], "hard"),
        ("കരകുശല വസ്തുക്കളുടെ പ്രധാന കയറ്റുമതി വസ്തു?", "കൈത്തെയ്യുന്ന പരിപ്പുകൾ/വസ്ത്രങ്ങൾ", ["കൽക്കരി", "എണ്ണ മാത്രം", "ഇരുമ്പ് അയിര് മാത്രം"], "hard"),
        ("കപ്പൽ നിർമ്മാണ പ്രധാന പി.എസ്.യു.?", "കൊച്ചി ഷിപ്പ്യാർഡ്", ["SAIL", "Coal India", "NTPC"], "hard"),
        ("ഭാരത് ഹെവി ഇലക്ട്രിക്കൽസിന്റെ പ്രധാന ഉൽപ്പന്നം?", "വിദ്യുത് നിലയ ഉപകരണങ്ങൾ", ["വിമാനവാഹിനികൾ മാത്രം", "മൊബൈൽ ഫോണുകൾ മാത്രം", "കാറുകൾ മാത്രം"], "medium"),
        ("ഇന്ത്യയിലെ ആദ്യ എക്സ്പോർട്ട് പ്രോസസ്സിംഗ് സോൺ?", "കാന്ദ്ല", ["കൊച്ചി", "ഡൽഹി", "ചെന്നൈ"], "hard"),
        ("ഹൈദരാബാദ് ഫാർമ ക്ലസ്റ്ററിന്റെ വിളിപ്പേര്?", "ബൾക്ക് ഡ്രഗ് തൽസ്ഥാനം", ["സ്റ്റീൽ നഗരം", "പിങ്ക് നഗരം", "നീല നഗരം"], "hard"),
        ("SIDBI എന്തിനാണ്?", "എം.എസ്.എം.ഇ ധനസഹായി", ["പ്രതിരോധം മാത്രം", "അന്തരീക്ഷം മാത്രം", "സിനിമ മാത്രം"], "medium"),
        ("മേക്ക് ഇൻ ഇന്ത്യ ആരംഭിച്ച വർഷം?", "2014", ["2013", "2015", "2016"], "easy"),
        ("ഇന്ത്യയിലെ ആദ്യ കോട്ടൺ മിൽ സ്ഥാപിതമായ സ്ഥലം?", "മുംബൈ", ["കൊൽക്കത്ത", "ചെന്നൈ", "അഹമദാബാദ്"], "hard"),
        ("ഇന്ത്യയിലെ ആദ്യ ജൂട് മിൽ സ്ഥാപിതമായ സ്ഥലം?", "റിശ്ര", ["മുംബൈ", "കാൻപൂർ", "അഹമദാബാദ്"], "hard"),
        ("ടാറ്റാ സ്റ്റീൽ (TISCO) സ്ഥാപിതമായ വർഷം?", "1907", ["1854", "1947", "1956"], "hard"),
        ("ആമുൽ സഹകരണ സംഘടനയുടെ സ്ഥലം?", "ആനന്ദ്", ["അഹമദാബാദ്", "മുംബൈ", "പുണെ"], "medium"),
        ("ODOP പദ്ധതി ആരംഭിച്ച വർഷം?", "2018", ["2014", "2020", "2016"], "hard"),
        ("ODOP പദ്ധതിയുടെ നോഡൽ മന്ത്രാലയം?", "വാണിജ്യ & വ്യവസായി മന്ത്രാലയം", ["കൃഷി", "പ്രതിരോധം", "ആരോഗ്യം"], "hard"),
        ("SECI എന്തിനാണ്?", "സോളാർ ഊർജ വ്യാപാരം", ["കൽക്കരി ഖനനം", "ഉരുക്ക്", "ടെക്സ്റ്റൈൽ"], "hard"),
        ("IREDA എന്തിനാണ്?", "പുതുനവീകരണ ഊർജ ധനസഹായി", ["കൽക്കരി", "എണ്ണ", "ഫാർമ"], "hard"),
        ("മോറാദാബാദ് ഏതിന് പ്രസിദ്ധമാണ്?", "പിത്തള കരകുശല വസ്തുക്കൾ", ["വജ്രം", "നിറ്റ്വെയർ", "ഫാർമ"], "hard"),
        ("സൂറത്ത് ഏതിന് പ്രസിദ്ധമാണ്?", "വജ്രം മുറിക്കൽ", ["ഉരുക്ക്", "കപ്പൽ", "ഫാർമ"], "hard"),
        ("പണിപ്പൂർ ഏതിന് പ്രസിദ്ധമാണ്?", "പെട്രോകെമിക്കൽ", ["കയർ", "ടീ", "കാപ്പി"], "hard"),
        ("ജെ.എൻ.പി.ടി. (നവാ ഷേവ) ഏത് സംസ്ഥാനത്തിൽ?", "മഹാരാഷ്ട്ര", ["ഗുജറാത്ത്", "കേരളം", "തമിഴ്നാട്"], "medium"),
        ("മുണ്ട്ര തുറമുഖം ഏത് സംസ്ഥാനത്തിൽ?", "ഗുജറാത്ത്", ["മഹാരാഷ്ട്ര", "കേരളം", "ആന്ധ്രപ്രദേശ്"], "medium"),
        ("STPI സ്ഥാപിതമായ വർഷം?", "1991", ["1980", "2005", "2015"], "hard"),
        ("NIMZ നയ വർഷം?", "2011", ["2000", "2015", "1990"], "hard"),
        ("ഇന്ത്യൻ ഓയിൽ റിഫൈനറികളുടെ എണ്ണം (ഏകദേശം)?", "10+", ["2", "50", "100"], "hard"),
        ("പൂണെ/ചെന്നൈ ഓട്ടോമൊബൈൽ ക്ലസ്റ്റർ ബന്ധപ്പെട്ട വ്യവസായി?", "ഓട്ടോമൊബൈൽ നിർമ്മാണം", ["കയർ", "ടീ മാത്രം", "സുഗന്ധവ്യഞ്ജനങ്ങൾ മാത്രം"], "easy"),
        ("ഇന്ത്യയിലെ ആദ്യ EPZ/SEZ?", "കാന്ദ്ല", ["കൊച്ചി", "ചെന്നൈ", "നോയിഡ"], "hard"),
        (f"ഇന്ത്യയിലെ {ev} സിംഗിൾ-സൈറ്റ് റിഫൈനറി?", "ജാംനഗർ (റിലയൻസ്)", ["പണിപ്പൂർ", "കൊച്ചി", "വഡിനാർ"], "medium"),
        ("ചിറ്റaranjan ലോക്കോമോട്ടീവ് വർക്ക്സ് എന്ത് നിർമ്മിക്കുന്നു?", "ലോക്കോമോട്ടീവുകൾ", ["വിമാനങ്ങൾ", "കപ്പലുകൾ മാത്രം", "മൊബൈൽ ഫോണുകൾ"], "hard"),
        ("ഇന്ത്യയുടെ ആദ്യ സ്റ്റീൽ പ്ലാന്റ്?", "ജാംഷേഡ്പൂർ (ടാറ്റാ)", ["ഭിലായി", "രൗർക്കെൽ", "ദുർഗാപൂർ"], "hard"),
        ("അമുൽ സംബന്ധിച്ച വിപ്ലവം?", "വെള്ള വിപ്ലവം", ["പച്ച വിപ്ലവം", "നീല വിപ്ലവം", "സ്വർണ്ണ വിപ്ലവം"], "medium"),
        ("ഇന്ത്യയിലെ ആദ്യ കോട്ടൺ മിൽ സ്ഥാപിത വർഷം?", "1854", ["1907", "1947", "1956"], "hard"),
        ("ഇന്ത്യയിലെ ആദ്യ ജൂട് മിൽ സ്ഥാപിത വർഷം?", "1855", ["1854", "1907", "1947"], "hard"),
        ("ഇന്ത്യയിലെ ആദ്യ റിഫൈനറി?", "ഡിഗ്ബോയ് (അസാം)", ["ജാംനഗർ", "പണിപ്പൂർ", "കൊച്ചി"], "hard"),
        ("ഇന്ത്യയിലെ ആദ്യ ഓട്ടോമൊബൈൽ ഫാക്ടറി?", "ഹിന്ദുസ്ഥാൻ മോട്ടോഴ്സ് (പോംപെ)", ["മാരുതി", "ടാറ്റാ", "മഹീന്ദ്ര"], "hard"),
        ("ഇന്ത്യയിലെ ആദ്യ സ്റ്റീൽ പ്ലാന്റ് സ്ഥാപകൻ?", "ജംശേദ്ജി ടാറ്റാ", ["ജവാഹർലാൽ നെഹ്റു", "ദാമോദർ", "ബിർള"], "hard"),
        ("ഇന്ത്യയുടെ ആദ്യ IT പാർക്ക്?", "SEEPZ (മുംബൈ)", ["ഇലക്ട്രോണിക് സിറ്റി", "HITEC സിറ്റി", "ഐ.ടി.പി.എൽ"], "hard"),
    ]


def build_all_data() -> dict[str, list[tuple[str, str]]]:
    B, V = blr(), valiya()
    bii = load_build_module()
    data: dict[str, list[tuple[str, str]]] = dict(bii.DATA)

    psus = build_psu_rows(B)
    data["PSU_SECTOR"] = [(a, s) for a, s, _ in psus]
    data["PSU_HQ"] = [(a, h) for a, _, h in psus]

    from ii_wave30_ind_data import fill_data

    fill_data(data, B)
    fill_remaining(data, B, V)
    return data


def write_output() -> int:
    bii = load_build_module()
    data = build_all_data()
    direct = build_direct_facts(blr(), valiya())

    missing = [m[0] for m in bii.CATEGORY_META if m[0] not in data]
    if missing:
        raise RuntimeError(f"Missing categories: {missing}")

    lines = [HEADER]
    for var, _comment, _fwd, _rev in bii.CATEGORY_META:
        lines.append(f"{var}: list[tuple[str, str]] = {pprint.pformat(data[var], width=120, sort_dicts=False)}\n")

    lines.append(
        f"DIRECT_FACTS: list[tuple[str, str, list[str], str]] = "
        f"{pprint.pformat(direct, width=120, sort_dicts=False)}\n"
    )

    emit_lines: list[str] = []
    for var, comment, fwd, rev in bii.CATEGORY_META:
        kw = ", english=True" if var in ENGLISH_CATS else ""
        emit_lines.append(f"    # {comment}")
        emit_lines.append(f"    emit_category(out, existing, rng, {var},")
        emit_lines.append(f"        {pprint.pformat(fwd, width=120)},")
        emit_lines.append(f"        {pprint.pformat(rev, width=120)},")
        emit_lines.append(f"        [a for a, _ in {var}], [b for _, b in {var}]{kw})")
        emit_lines.append("")

    lines.append(EMIT_FOOTER.format(emit_body="\n".join(emit_lines)))
    OUT.write_text("".join(lines), encoding="utf-8")

    spec = importlib.util.spec_from_file_location("outmod", OUT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return len(mod.generate_wave30_candidates(set(), random.Random(0)))


def main() -> None:
    count = write_output()
    print(f"Wrote {OUT}")
    print(f"Candidate count: {count}")
    if count < 800:
        sys.exit(1)


if __name__ == "__main__":
    main()

