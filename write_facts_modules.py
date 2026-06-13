#!/usr/bin/env python3
"""One-shot writer for physics_facts, biology_facts, indian_history_facts modules."""

from __future__ import annotations

import inspect
import random
import textwrap
from pathlib import Path

BASE = Path(__file__).parent

Candidate = tuple[str, list[str], str, str]

# ---------------------------------------------------------------------------
# Shared helpers (mirrored in emitted modules)
# ---------------------------------------------------------------------------


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


# ===================================================================
# PHYSICS DATA
# ===================================================================

PHYSICS_SI_BASE: list[tuple[str, str, str]] = [
    ("ദൈർഘ്യം", "മീറ്റർ", "m"),
    ("പിണ്ഡം", "കിലോഗ്രാം", "kg"),
    ("സമയം", "സെക്കന്ഡ്", "s"),
    ("വൈദ്യുത പ്രവാഹം", "ആംപിയർ", "A"),
    ("താപനില", "കെൽവിൻ", "K"),
    ("പദാർത്ഥത്തിന്റെ അളവ്", "മോൾ", "mol"),
    ("പ്രകാശത്തിന്റെ തീവ്രത", "കാൻഡില", "cd"),
]

PHYSICS_SI_DERIVED: list[tuple[str, str, str]] = [
    ("ന്യൂട്ടൺ", "ബലം", "N"),
    ("ജൗൾ", "ഊർജം", "J"),
    ("വാട്ട്", "ശക്തി", "W"),
    ("പാസ്കൽ", "സമ്മർദ്ദം", "Pa"),
    ("വോൾട്ട്", "വൈദ്യുത വ്യത്യാസം", "V"),
    ("ഓം", "വൈദ്യുത പ്രതിരോധം", "Ω"),
    ("ഹെർട്സ്", "ആവൃത്തി", "Hz"),
    ("കൂളം", "വൈദ്യുത ചാർജ്", "C"),
    ("ഹെൻറി", "ഇൻഡക്ടൻസ്", "H"),
    ("ഫാരഡ്", "ധാരിത്വം", "F"),
    ("ടെസ്ല", "ചുംബക കളത്തിന്റെ തീവ്രത", "T"),
    ("വെബർ", "ചുംബക ചോരി", "Wb"),
    ("ലൂമെൻ", "പ്രകാശ ചോരി", "lm"),
    ("ലക്സ്", "പ്രകാശപ്രവാഹം", "lx"),
    ("ബെക്കറെൽ", "റേഡിയോ ആക്ടിവിറ്റി", "Bq"),
    ("ഗ്രേ", "ഗ്രഹിത ഡോസ്", "Gy"),
    ("സീവർട്", "തുല്യ ഡോസ്", "Sv"),
    ("ഡെസിബൽ", "ശബ്ദതീവ്രത", "dB"),
    ("റേഡിയൻ", "കോണീയ വ്യത്യാസം", "rad"),
    ("സ്റ്റെറാഡിയൻ", "ഘനകോൺ", "sr"),
    ("മീറ്റർ/സെക്കന്ഡ്", "വേഗം", "m/s"),
    ("മീറ്റർ/സെക്കന്ഡ്²", "ത്വരണം", "m/s²"),
    ("കിലോഗ്രാം/മീറ്റർ³", "സാന്ദ്രത", "kg/m³"),
    ("ന്യൂട്ടൺ·മീറ്റർ", "ടോർക്ക്", "N·m"),
    ("ജൗൾ/കെൽവിൻ", "എൻട്രോപ്പി", "J/K"),
    ("വാട്ട്/(മീറ്റർ·കെൽവിൻ)", "താപചാലനം", "W/(m·K)"),
    ("പാസ്കൽ·സെക്കന്ഡ്", "ശ്യാനത", "Pa·s"),
    ("കാൻഡില/മീറ്റർ²", "പ്രകാശസാന്ദ്രത", "cd/m²"),
    ("വാട്ട്/മീറ്റർ²", "പ്രകാശസംവേഗം", "W/m²"),
    ("ആംപിയർ/മീറ്റർ", "ചുംബകക്ഷേത്ര തീവ്രത", "A/m"),
    ("വെബർ/മീറ്റർ²", "ചുംബക ഫ്ലക്സ് സാന്ദ്രത", "Wb/m²"),
    ("കൂളം/വോൾട്ട്", "എലക്ട്രിക് ഫീൽഡ്", "C/V"),
    ("വാട്ട്/സെക്കന്ഡ്", "ഊർജ്ജപ്രവാഹം", "W/s"),
    ("ന്യൂട്ടൺ/മീറ്റർ", "ഉപരിതല വലിവ്", "N/m"),
    ("ജൗൾ/കിലോഗ്രാം", "നിർദ്ദിഷ്ട ഊർജം", "J/kg"),
]

PHYSICS_SI_PREFIXES: list[tuple[str, str, str]] = [
    ("യോട്ട", "10²⁴", "Y"),
    ("സെപ്റ്റ", "10²¹", "Z"),
    ("എക്സ", "10¹⁸", "E"),
    ("പെറ്റ", "10¹⁵", "P"),
    ("ടെറ", "10¹²", "T"),
    ("ഗിഗ", "10⁹", "G"),
    ("മെഗ", "10⁶", "M"),
    ("കിലോ", "10³", "k"),
    ("ഹെക്ടോ", "10²", "h"),
    ("ഡെക", "10¹", "da"),
    ("ഡെസി", "10⁻¹", "d"),
    ("സെന്റി", "10⁻²", "c"),
    ("മില്ലി", "10⁻³", "m"),
    ("മൈക്രോ", "10⁻⁶", "μ"),
    ("നാനോ", "10⁻⁹", "n"),
    ("പികോ", "10⁻¹²", "p"),
    ("ഫെംടോ", "10⁻¹⁵", "f"),
    ("ആറ്റോ", "10⁻¹⁸", "a"),
    ("സെപ്ടോ", "10⁻²¹", "z"),
    ("യോക്ടോ", "10⁻²⁴", "y"),
]

PHYSICS_CONSTANTS: list[tuple[str, str, list[str], str]] = [
    ("ശൂന്യാവകാശത്തിലെ പ്രകാശ വേഗം", "3×10⁸ m/s", ["3×10⁶ m/s", "3×10¹⁰ m/s", "3×10⁵ m/s"], "easy"),
    ("ഗുരുത്വാകർഷണ സ്ഥിരാങ്കം G", "6.67×10⁻¹¹ N·m²/kg²", ["6.67×10⁻⁹", "9.8 N/kg", "6.02×10²³"], "hard"),
    ("പ്ലാങ്ക് സ്ഥിരാങ്കം h", "6.626×10⁻³⁴ J·s", ["6.626×10⁻²⁴", "1.6×10⁻¹⁹", "9.11×10⁻³¹"], "hard"),
    ("ഇലക്ട്രോൺ ചാർജ് e", "1.6×10⁻¹⁹ C", ["1.6×10⁻¹⁸", "6.626×10⁻³⁴", "9.11×10⁻³¹"], "hard"),
    ("അവോഗാഡ്രോ സംഖ്യ", "6.022×10²³ mol⁻¹", ["6.67×10⁻¹¹", "1.38×10⁻²³", "3×10⁸"], "medium"),
    ("ബോൾട്സ്മാൻ സ്ഥിരാങ്കം", "1.38×10⁻²³ J/K", ["6.022×10²³", "8.314", "1.6×10⁻¹⁹"], "hard"),
    ("ആദർശ വാതക സ്ഥിരാങ്കം R", "8.314 J/(mol·K)", ["1.38×10⁻²³", "6.022×10²³", "9.8"], "hard"),
    ("ഇലക്ട്രോൺ വിശ്രാമ പിണ്ഡം", "9.11×10⁻³¹ kg", ["1.67×10⁻²⁷ kg", "1.6×10⁻¹⁹ C", "6.626×10⁻³⁴"], "hard"),
    ("പ്രോട്ടോൺ വിശ്രാമ പിണ്ഡം", "1.67×10⁻²⁷ kg", ["9.11×10⁻³¹ kg", "1.6×10⁻¹⁹ C", "6.67×10⁻¹¹"], "hard"),
    ("ഭൂമിയിലെ സ്വതന്ത്ര പതന ത്വരണം g", "9.8 m/s²", ["10 m/s²", "6.67 m/s²", "3×10⁸ m/s²"], "easy"),
    ("സാധാരണ വാതകാശ്മയ സമ്മർദ്ദം", "1.013×10⁵ Pa", ["1×10³ Pa", "10⁵ Pa", "760 Pa"], "medium"),
    ("ശൂന്യതാപനില", "0 K", ["−273 K", "273 °C", "0 °C"], "easy"),
    ("കൂളോം സ്ഥിരാങ്കം", "8.99×10⁹ N·m²/C²", ["6.67×10⁻¹¹", "1.6×10⁻¹⁹", "8.314"], "hard"),
    ("സ്റ്റഫാൻ-ബോൾട്സ്മാൻ സ്ഥിരാങ്കം", "5.67×10⁻⁸ W/(m²·K⁴)", ["6.626×10⁻³⁴", "1.38×10⁻²³", "3×10⁸"], "hard"),
    ("ഭൂമിയുടെ പലായന വേഗം", "11.2 km/s", ["7.9 km/s", "3×10⁸ m/s", "42 km/s"], "medium"),
    ("ഭൂമിയുടെ പ്രദക്ഷിണ വേഗം", "≈7.9 km/s", ["11.2 km/s", "3×10⁵ km/s", "1 km/s"], "medium"),
    ("ജലത്തിന്റെ അപവർത്തന സൂചിക", "≈1.33", ["≈1.5", "≈1.0", "≈2.0"], "medium"),
    ("സാധാരണ ഗ്ലാസിന്റെ അപവർത്തന സൂചിക", "≈1.5", ["≈1.33", "≈1.0", "≈2.4"], "medium"),
    ("വജ്രത്തിന്റെ അപവർത്തന സൂചിക", "≈2.42", ["≈1.33", "≈1.5", "≈1.0"], "hard"),
    ("1 eV ജൂളുകളിൽ", "1.6×10⁻¹⁹ J", ["6.626×10⁻³⁴ J", "9.11×10⁻¹⁹ J", "8.314 J"], "hard"),
    ("വായുവിൽ ശബ്ദവേഗം (20°C)", "343 m/s", ["3300 m/s", "34.3 m/s", "3×10⁸ m/s"], "medium"),
    ("ജലത്തിന്റെ തിളുപ്പ് (1 atm)", "100 °C", ["0 °C", "273 °C", "50 °C"], "easy"),
    ("ജലത്തിന്റെ freezing point (1 atm)", "0 °C", ["100 °C", "−273 °C", "273 °C"], "easy"),
    ("absolute zero Celsius-ൽ", "−273.15 °C", ["0 °C", "−273 °C", "273 °C"], "easy"),
    ("യാന്ത്രിക-താപ ഊർജ്ജ സമതുല്യം", "4.186 J/cal", ["8.314 J/cal", "1 J/cal", "9.8 J/cal"], "hard"),
    ("കോസ്മിക് മൈക്രോവേവ് പശ്ചാത്തല താപനില", "≈2.7 K", ["≈0 K", "≈27 K", "≈270 K"], "hard"),
    ("ഹബ്ബിൾ സ്ഥിരാങ്കം (aprox)", "≈70 km/s/Mpc", ["≈300 km/s/Mpc", "≈7 km/s/Mpc", "≈7000 km/s/Mpc"], "hard"),
    ("fine structure constant (aprox)", "≈1/137", ["≈1/100", "≈1/200", "≈1/500"], "hard"),
    ("റൈഡ്ബർഗ് സ്ഥിരാങ്കം", "1.097×10⁷ m⁻¹", ["6.626×10⁻³⁴", "1.6×10⁻¹⁹", "9.11×10⁻³¹"], "hard"),
    ("ബോർ അറ്റംവ്യാസാർ (aprox)", "0.529 Å", ["1 Å", "2.18 Å", "5 Å"], "hard"),
    ("atomic mass unit", "1.66×10⁻²⁷ kg", ["9.11×10⁻³¹ kg", "1.67×10⁻²⁷ kg", "6.626×10⁻³⁴ kg"], "hard"),
    ("ജലത്തിന്റെ triple point താപനില", "0.01 °C", ["0 °C", "100 °C", "273 °C"], "hard"),
    ("standard atmospheric pressure mmHg", "760 mm Hg", ["7600 mm Hg", "76 mm Hg", "7.6 mm Hg"], "medium"),
    ("പ്രകാശ വേഗത്തിന്റെ ചിഹ്നം", "c", ["v", "λ", "f"], "easy"),
    ("പ്ലാങ്ക് സ്ഥിരാങ്കത്തിന്റെ ചിഹ്നം", "h", ["k", "G", "e"], "easy"),
    ("ഗുരുത്വാകർഷണ സ്ഥിരാങ്കത്തിന്റെ ചിഹ്നം", "G", ["g", "h", "c"], "easy"),
    ("ഇലക്ട്രോൺ ചാർജിന്റെ ചിഹ്നം", "e", ["m", "h", "c"], "easy"),
    ("അവോഗാഡ്രോ സംഖ്യയുടെ ചിഹ്നം", "N_A", ["R", "k", "G"], "medium"),
    ("ബോൾട്സ്മാൻ സ്ഥിരാങ്കത്തിന്റെ ചിഹ്നം", "k_B", ["R", "h", "G"], "hard"),
    ("ആദർശ വാതക സ്ഥിരാങ്കത്തിന്റെ ചിഹ്നം", "R", ["k", "G", "N_A"], "medium"),
]

PHYSICS_LAWS: list[tuple[str, str, list[str], str]] = [
    ("ന്യൂട്ടന്റെ ആദ്യ നിയമം", "ജഡത്വ നിയമം", ["F = ma", "പ്രതികരണ-പ്രതികരണം", "PV = nRT"], "easy"),
    ("ന്യൂട്ടന്റെ രണ്ടാം നിയമം", "F = ma", ["F = mv", "F = m/a", "F = mgh"], "easy"),
    ("ന്യൂട്ടന്റെ മൂന്നാം നിയമം", "പ്രതികരണം സമാനവും വിപരീതവും", ["F = ma", "ജഡത്വം", "PV = nRT"], "easy"),
    ("ഓം നിയമം", "V = IR", ["P = VI", "F = ma", "PV = nRT"], "easy"),
    ("ബോയിൽ നിയമം", "PV = സ്ഥിരം", ["V/T = സ്ഥിരം", "P/T = സ്ഥിരം", "F = ma"], "medium"),
    ("ചാൾസ് നിയമം", "V/T = സ്ഥിരം", ["PV = സ്ഥിരം", "P/T = സ്ഥിരം", "V = IR"], "medium"),
    ("ഗേ-ലുസാക്ക് നിയമം", "P/T = സ്ഥിരം", ["PV = സ്ഥിരം", "V/T = സ്ഥിരം", "F = ma"], "medium"),
    ("ആദർശ വാതക നിയമം", "PV = nRT", ["PV = സ്ഥիրം", "F = ma", "V = IR"], "medium"),
    ("പാസ്കൽ നിയമം", "ദ്രാവകത്തിൽ സമ്മർദ്ദം സമമായി передается", ["ഉയർച്ച മാത്രം", "F = ma", "PV = nRT"], "medium"),
    ("ആർക്കിമിഡീസ് തത്ത്വം", "പ്ലാവനബലം = Displaced fluid weight", ["F = ma", "PV = nRT", "V = IR"], "medium"),
    ("ബർണോളി തത്ത്വം", "വേഗം കൂടുമ്പോൾ സമ്മർദ്ദം കുറയുന്നു", ["സമ്മർദ്ദം എപ്പോഴും സ്ഥിരം", "F = ma", "PV = nRT"], "medium"),
    ("ഹുക്ക് നിയമം", "F = −kx", ["F = ma", "PV = nRT", "V = IR"], "medium"),
    ("സ്നെൽ നിയമം", "n₁ sin θ₁ = n₂ sin θ₂", ["n sin θ = 0", "F = ma", "PV = nRT"], "hard"),
    ("ഫാരadays感应", "flux മാറ്റത്തിന്റെ നിരക്കിൽ EMF", ["V = IR", "F = ma", "PV = nRT"], "hard"),
    ("ലെൻസ് നിയമം", "感应电流 flux മാറ്റത്തിനെ എതിർക്കുന്നു", ["flux മാറ്റത്തെ സഹായിക്കുന്നു", "F = ma", "V = IR"], "hard"),
    ("കൂളോം നിയമം", "F ∝ q₁q₂/r²", ["F ∝ r²", "F ∝ 1/r", "F = ma"], "medium"),
    ("ഗുരുത്വാകർഷണ നിയമം", "F = Gm₁m₂/r²", ["F = Gm₁m₂/r", "F = ma", "V = IR"], "medium"),
    ("കെപ്ലർ ഒന്നാം നിയമം", "ഗ്രഹങ്ങൾ ദീർഘവൃത്തത്തിൽ", ["വൃത്തത്തിൽ മാത്രം", "നേർരേഖയിൽ", "F = ma"], "hard"),
    ("കെപ്ലർ രണ്ടാം നിയമം", "സമാന സമയം സമാന വിസ്തീർണ്ണം", ["സമാന ദൂരം", "F = ma", "V = IR"], "hard"),
    ("കെപ്ലർ മൂന്നാം നിയമം", "T² ∝ a³", ["T ∝ a", "T² ∝ a", "T ∝ a²"], "hard"),
    ("ജൗൾ ചൂട് നിയമം", "H = I²Rt", ["H = IVt", "F = ma", "PV = nRT"], "medium"),
    ("ഫോട്ടോഇലക്ട്രിക് സമീകരണം", "K_max = hf − φ", ["E = mc²", "F = ma", "PV = nRT"], "hard"),
    ("ഡി ബ്രോഗ്ലി ബന്ധം", "λ = h/p", ["λ = hf", "E = mc²", "F = ma"], "hard"),
    ("ഹൈസൻബർഗ് അനിശ്ചിതത്വം", "ΔxΔp ≥ ℏ/2", ["ΔxΔp = 0", "F = ma", "V = IR"], "hard"),
    ("ഐൻസ്റ്റീൻ ദ്രവ്യ-ഊർജം", "E = mc²", ["E = hf", "F = ma", "PV = nRT"], "medium"),
    ("ഡോപpler effect", "relative motion-ൽ frequency shift", ["frequency മാറില്ല", "F = ma", "V = IR"], "medium"),
    ("പ്രതിഫലന നിയമം", "ആപതന കോൺ = പ്രതിഫലന കോൺ", ["refraction", "F = ma", "PV = nRT"], "easy"),
    ("thermodynamics ഒന്നാം നിയമം", "ΔU = Q − W", ["ΔU = Q + W", "F = ma", "V = IR"], "hard"),
    ("thermodynamics രണ്ടാം നിയമം", "isolated system entropy വർദ്ധിക്കുന്നു", ["entropy കുറയുന്നു", "F = ma", "V = IR"], "hard"),
    ("thermodynamics മൂന്നാം നിയമം", "T → 0 K entropy → 0", ["entropy ∞", "F = ma", "V = IR"], "hard"),
    ("Stefan-Boltzmann", "P = σAT⁴", ["P ∝ T²", "P ∝ T", "F = ma"], "hard"),
    ("Wien displacement", "λ_max T = constant", ["λ_max/T = constant", "F = ma", "V = IR"], "hard"),
    ("momentum സംരക്ഷണം", "external force ഇല്ലെങ്കിൽ momentum സ്ഥിരം", ["momentum എപ്പോഴും വർദ്ധിക്കുന്നു", "F = ma", "V = IR"], "medium"),
    ("energy സംരക്ഷണം", "energy സൃഷ്ടിയോ നശനമോ ഇല്ല", ["energy സൃഷ്ടിക്കാം", "F = ma", "V = IR"], "easy"),
    ("charge സംരക്ഷണം", "isolated system-ൽ net charge സ്ഥിരം", ["charge സൃഷ്ടിക്കാം", "F = ma", "PV = nRT"], "medium"),
    ("simple pendulum period", "T = 2π√(l/g)", ["T = 2π√(m/k)", "T = l/g", "V = IR"], "medium"),
    ("spring SHM period", "T = 2π√(m/k)", ["T = 2π√(l/g)", "T = 1/f", "F = ma"], "hard"),
    ("wave relation", "v = fλ", ["v = f/λ", "v = λ/f", "F = ma"], "easy"),
    ("intensity inverse square", "I ∝ 1/r²", ["I ∝ r²", "I constant", "F = ma"], "medium"),
    ("capacitor energy", "U = ½CV²", ["U = CV", "U = ½CV", "F = ma"], "hard"),
    ("inductor energy", "U = ½LI²", ["U = LI", "U = ½LI", "F = ma"], "hard"),
    ("transformer", "V_p/V_s = N_p/N_s", ["V_p = V_s", "F = ma", "PV = nRT"], "medium"),
    ("photon energy", "E = hf", ["E = mc", "F = ma", "V = IR"], "medium"),
    ("mirror formula", "1/f = 1/v + 1/u", ["f = u+v", "F = ma", "PV = nRT"], "medium"),
    ("thin lens formula", "1/f = 1/v + 1/u", ["f = uv", "F = ma", "PV = nRT"], "medium"),
    ("magnification", "m = v/u", ["m = u/v", "F = ma", "V = IR"], "medium"),
    ("beat frequency", "f_beat = |f₁ − f₂|", ["f₁ + f₂", "F = ma", "V = IR"], "hard"),
    ("resonance", "natural frequency-ൽ amplitude maximum", ["minimum amplitude", "F = ma", "V = IR"], "medium"),
    ("half-life", "activity പകുതിയാകാൻ വേണ്ട സമയം", ["double", "quarter", "F = ma"], "medium"),
    ("Pauli exclusion", "fermions same quantum state-ൽ രണ്ടും അല്ല", ["bosons only", "F = ma", "V = IR"], "hard"),
    ("total internal reflection", "n₁ > n₂, angle > critical", ["n₁ < n₂", "any angle", "F = ma"], "hard"),
    ("critical angle", "sin θ_c = n₂/n₁", ["n₁/n₂", "n₁+n₂", "F = ma"], "hard"),
    ("RMS AC", "V_rms = V_peak/√2", ["V_rms = V_peak", "V_rms = √2 V_peak", "F = ma"], "hard"),
    ("LC oscillation", "f = 1/(2π√(LC))", ["f = 2π√(LC)", "f = √(LC)", "F = ma"], "hard"),
    ("Kirchhoff current", "junction-ൽ ΣI_in = ΣI_out", ["V = IR only", "F = ma", "PV = nRT"], "hard"),
    ("Kirchhoff voltage", "loop-ൽ ΣV = 0", ["ΣI = 0 only", "F = ma", "PV = nRT"], "hard"),
    ("Ampere circuital", "∮B·dl = μ₀I_enc", ["V = IR", "F = ma", "PV = nRT"], "hard"),
    ("Gauss electric", "closed surface flux ∝ enclosed charge", ["magnetic monopole", "F = ma", "V = IR"], "hard"),
    ("Tyndall effect", "colloidal particles scatter light", ["refraction only", "F = ma", "V = IR"], "medium"),
    ("Malus law", "I = I₀ cos²θ", ["I = I₀ sin θ", "F = ma", "V = IR"], "hard"),
    ("Compton effect", "photon wavelength increases", ["decreases", "unchanged", "F = ma"], "hard"),
    ("binding energy", "mass defect × c²", ["E = hf only", "F = ma", "V = IR"], "hard"),
    ("Zeeman effect", "magnetic field-ൽ spectral lines split", ["merge", "F = ma", "V = IR"], "hard"),
    ("Stark effect", "electric field-ൽ split", ["magnetic only", "F = ma", "V = IR"], "hard"),
    ("Hall effect", "carrier density and sign measure", ["temperature only", "F = ma", "PV = nRT"], "hard"),
    ("Seebeck effect", "temperature gradient thermoelectric EMF", ["photoelectric", "F = ma", "V = IR"], "hard"),
    ("Lorentz contraction", "high speed-ൽ length shortens", ["lengthens", "F = ma", "V = IR"], "hard"),
    ("time dilation", "moving clocks slow", ["fast", "F = ma", "PV = nRT"], "hard"),
    ("SHM acceleration", "a = −ω²x", ["a = ωx", "F = ma only", "V = IR"], "hard"),
    ("power pure resistor AC", "P = I²R = V²/R", ["P = VI only", "F = ma", "PV = nRT"], "medium"),
    ("work-energy theorem", "W = ΔKE", ["W = PE only", "F = ma", "V = IR"], "medium"),
    ("impulse-momentum", "FΔt = Δp", ["FΔt = ΔE", "F = ma only", "V = IR"], "medium"),
    ("centripetal force", "F = mv²/r", ["F = mr²/v", "F = ma only", "V = IR"], "medium"),
    ("angular momentum", "L = Iω", ["L = m/v", "F = ma", "V = IR"], "hard"),
    ("torque", "τ = r × F", ["τ = r/F", "F = ma", "V = IR"], "medium"),
    ("Young modulus", "stress/strain", ["strain/stress", "F = ma", "V = IR"], "hard"),
    ("Poiseuille flow", "flow ∝ r⁴", ["flow ∝ r²", "F = ma", "V = IR"], "hard"),
    ("Bernoulli equation", "P + ½ρv² + ρgh = constant", ["P = constant only", "F = ma", "V = IR"], "hard"),
    ("Doppler light", "moving source frequency shift", ["no shift", "F = ma", "V = IR"], "hard"),
    ("Brewster angle", "reflected light polarized", ["always unpolarized", "F = ma", "V = IR"], "hard"),
    ("Fraunhofer lines", "solar absorption spectrum", ["emission only", "F = ma", "V = IR"], "hard"),
    ("blackbody peak Wien", "λ_max inversely proportional T", ["directly proportional", "F = ma", "V = IR"], "hard"),
    ("Planck quantum", "E = hf", ["E = mc only", "F = ma", "V = IR"], "hard"),
    ("de Broglie matter waves", "particles have wavelength", ["only photons", "F = ma", "V = IR"], "hard"),
    ("Schrodinger equation", "quantum state evolution", ["classical only", "F = ma", "V = IR"], "hard"),
    ("Bose-Einstein statistics", "indistinguishable bosons", ["fermions only", "F = ma", "V = IR"], "hard"),
    ("pair production threshold", "≥ 1.022 MeV", ["0.511 MeV", "1 MeV", "F = ma"], "hard"),
    ("Rutherford model", "small dense nucleus", ["plum pudding", "F = ma", "V = IR"], "medium"),
    ("Bohr model", "quantized orbits hydrogen", ["continuous orbits", "F = ma", "V = IR"], "medium"),
    ("Franck-Hertz", "discrete atomic energy levels", ["continuous only", "F = ma", "V = IR"], "hard"),
    ("Davisson-Germer", "electron diffraction", ["photoelectric only", "F = ma", "PV = nRT"], "hard"),
    ("Michelson-Morley", "no ether drift", ["confirmed ether", "F = ma", "V = IR"], "hard"),
    ("Millikan oil drop", "electron charge measured", ["proton mass", "F = ma", "V = IR"], "hard"),
    ("Cathode rays", "electrons are particles", ["protons only", "F = ma", "PV = nRT"], "hard"),
    ("Edison thermionic", "heated filament emits electrons", ["photons only", "F = ma", "V = IR"], "hard"),
    ("gravitational waves LIGO", "2015 detection", ["1905", "1919", "1998"], "hard"),
    ("Higgs boson discovery", "CERN 2012", ["Fermilab 1980", "2000", "2019"], "hard"),
]

# Import extended lists from emit helper if present
try:
    from emit_three_facts import PHYSICS_SCIENTISTS, PHYSICS_INSTRUMENTS, SI_EXTRA_SYMBOLS
except ImportError:
    PHYSICS_SCIENTISTS = [
        ("ഗുരുത്വാകർഷണ നിയമം", "ഐസak ന്യൂട്ടൺ", ["ഗാലിലിയോ", "കെപ്ലർ", "ആൽബർട്ട് ഐൻസ്റ്റൈൻ"], "easy"),
        ("ഓമിന്റെ നിയമം", "ജോർജ് ഓം", ["മൈക്കൽ ഫാരഡേ", "ജെയിംസ് ക്ലാർക്ക് മാക്സ്വെൽ", "വിൽഹelm റോന്റ്ജൻ"], "medium"),
        ("special relativity", "ആൽബർട്ട് ഐൻസ്റ്റൈൻ", ["ന്യൂട്ടൺ", "പ്ലാങ്ക്", "ബോർ"], "easy"),
        ("electromagnetic induction", "മൈക്കൽ ഫാരഡേ", ["ആംപിയർ", "ഓം", "ഓersted"], "easy"),
    ]
    PHYSICS_INSTRUMENTS = [
        ("വോൾട്ട് മീറ്റർ", "വോൾട്ടേജ് അളക്കുന്നു", ["പ്രവാഹം", "പ്രതിരോധം", "ശക്തി"], "easy"),
        ("ആം മീറ്റർ", "പ്രവാഹം അളക്കുന്നു", ["വോൾട്ടേജ്", "പ്രതിരോധം", "ധാരിത്വം"], "easy"),
        ("ഓം മീറ്റർ", "പ്രതിരോധം അളക്കുന്നു", ["വോൾട്ടേജ്", "പ്രവാഹം", "ശക്തി"], "easy"),
    ]
    SI_EXTRA_SYMBOLS = [
        ("ധാരിത്വം", "F", ["H", "V", "W"]),
        ("ചുംബക കളത്തിന്റെ തീവ്രത", "T", ["Wb", "A/m", "H"]),
    ]

SI_BASE_UNITS = PHYSICS_SI_BASE
SI_DERIVED_UNITS = PHYSICS_SI_DERIVED
SI_PREFIXES = PHYSICS_SI_PREFIXES
CONSTANTS = PHYSICS_CONSTANTS
LAWS = PHYSICS_LAWS
SCIENTISTS = PHYSICS_SCIENTISTS
INSTRUMENTS = PHYSICS_INSTRUMENTS


def generate_candidates(existing: set[str], rng: random.Random) -> list[Candidate]:
    out: list[Candidate] = []
    qtys = [q for q, _, _ in SI_BASE_UNITS]
    units = [u for _, u, _ in SI_BASE_UNITS]
    d_qtys = [q for _, q, _ in SI_DERIVED_UNITS]
    d_units = [u for u, _, _ in SI_DERIVED_UNITS]
    law_names = [n for n, _, _, _ in LAWS]
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
        _add(out, existing, rng, f"'{qty}'-ന്റെ SI ചിഹ്നം ഏതാണ്?", sym, wrong + [sym], "medium")
        eqty = [q for q, _, _ in SI_EXTRA_SYMBOLS]
        _add(out, existing, rng, f"SI ചിഹ്നം '{sym}' ഏത് അളവ?", qty, eqty, "medium")

    pnames = [p for p, _, _ in SI_PREFIXES]
    pvals = [v for _, v, _ in SI_PREFIXES]
    for name, val, sym in SI_PREFIXES:
        _add(out, existing, rng, f"SI ഉപസർഗ്ഗം '{name}'-ന്റെ ഗുണിതം ഏത്?", val, pvals, "medium")
        _add(out, existing, rng, f"SI prefix ചിഹ്നം '{sym}'-ന്റെ പേര് ഏത്?", name, pnames, "hard")

    for topic, ans, wrong, diff in CONSTANTS:
        _add(out, existing, rng, f"ഭൗതികശാസ്ത്രത്തിൽ '{topic}'-ന്റെ മൂല്യം/ഫലം ഏത്?", ans, wrong + [ans], diff)

    for name, form, wrong, diff in LAWS:
        _add(out, existing, rng, f"'{name}'-ന്റെ സൂത്രം/വിശേഷണം ഏത്?", form, wrong + [form], diff)
        _add(out, existing, rng, f"'{form}' ഏത് നിയമവുമായി ബന്ധപ്പെട്ടത്?", name, law_names, diff)

    for topic, person, wrong, diff in SCIENTISTS:
        _add(out, existing, rng, f"'{topic}'-ന് ബന്ധപ്പെട്ട ശാസ്ത്രജ്ഞൻ ഏത്?", person, wrong + [person], diff)
        _add(out, existing, rng, f"'{person}'-ന്റെ പ്രധാന സംഭാവന ഏത്?", topic, disc, diff)

    for instr, use, wrong, diff in INSTRUMENTS:
        _add(out, existing, rng, f"'{instr}' ഉപകരണം എന്തിനാണ് ഉപയോഗിക്കുന്നത്?", use, wrong + [use], diff)

    return out


BASE = Path(__file__).parent


def _module_header(desc: str) -> str:
    return f'''#!/usr/bin/env python3
"""Verified {desc} facts for unique Malayalam PSC question generation."""

from __future__ import annotations

import random

Candidate = tuple[str, list[str], str, str]

'''


def _emit_physics() -> None:
    import inspect
    src = inspect.getsource(generate_candidates)
    body = []
    for name, val in [
        ("SI_BASE_UNITS", SI_BASE_UNITS),
        ("SI_DERIVED_UNITS", SI_DERIVED_UNITS),
        ("SI_EXTRA_SYMBOLS", SI_EXTRA_SYMBOLS),
        ("SI_PREFIXES", SI_PREFIXES),
        ("CONSTANTS", CONSTANTS),
        ("LAWS", LAWS),
        ("SCIENTISTS", SCIENTISTS),
        ("INSTRUMENTS", INSTRUMENTS),
    ]:
        body.append(f"{name}: list = {val!r}\n")
    helpers = inspect.getsource(_pick) + "\n" + inspect.getsource(_add)
    text = _module_header("physics") + helpers + "\n".join(body) + "\n" + src
    (BASE / "physics_facts.py").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    _emit_physics()
    rng = random.Random(42)
    import importlib
    import physics_facts as pf
    importlib.reload(pf)
    n = len(pf.generate_candidates(set(), rng))
    print("physics_facts.py candidates:", n)

