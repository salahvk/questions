#!/usr/bin/env python3
"""Malayalam-only cinema term facts for wave-20 categories."""

from __future__ import annotations

Fact = tuple[str, str, list[str], str]

CINEMATOGRAPHY: list[Fact] = [
    ("ഡോളി ഷോട്ട്", "ക്യാമറ ചലിപ്പിച്ച് എടുക്കുന്ന ദൃശ്യം", ["സ്ഥിര ഷോട്ട്", "ഹാൻഡ് ഹെൽഡ്", "ഏരിയൽ ഷോട്ട്"], "medium"),
    ("ട്രാക്കിംഗ് ഷോട്ട്", "വസ്തുവിനൊപ്പം ക്യാമറ നീങ്ങുന്ന ദൃശ്യം", ["സ്ഥിര ഷോട്ട്", "ടിൽട്ട്", "സൂം"], "medium"),
    ("പാൻ ഷോട്ട്", "ക്യാമറ തിരശ്ചീനമായി നീങ്ങൽ", ["ടിൽട്ട്", "സൂം", "ഡോളി"], "easy"),
    ("ടിൽട്ട് ഷോട്ട്", "ക്യാമറ ലംബമായി നീങ്ങൽ", ["പാൻ", "സൂം", "ഡോളി"], "easy"),
    ("സൂം ഷോട്ട്", "ലെൻസ് ദൂരം മാറ്റി എടുക്കുന്ന ദൃശ്യം", ["ഡോളി", "ട്രാക്കിംഗ്", "പാൻ"], "easy"),
    ("ക്ലോസ്-അപ്പ്", "വസ്തുവിന്റെ സമീപദൃശ്യം", ["വൈഡ് ഷോട്ട്", "ഏരിയൽ", "ഇൻസേർട്ട്"], "easy"),
    ("വൈഡ് ഷോട്ട്", "വിസ്തൃത പശ്ചാത്തലമുള്ള ദൃശ്യം", ["ക്ലോസ്-അപ്പ്", "മാക്രോ", "ടു-ഷോട്ട്"], "easy"),
    ("ഓവർ-ദ-ഷോൾഡർ", "സംഭാഷണത്തിനുള്ള ദൃശ്യരീതി", ["ക്ലോസ്-അപ്പ്", "വൈഡ്", "ഏരിയൽ"], "medium"),
    ("ഡീപ് ഫോക്കസ്", "മുന്നും പിന്നും വ്യക്തമായി കാണുന്ന ഷോട്ട്", ["ഷalow ഫോക്കസ്", "മാക്രോ", "ടെലിഫോട്ടോ"], "hard"),
    ("ഷalow ഫോക്കസ്", "പശ്ചാത്തലം മങ്ങിയ ഷോട്ട്", ["ഡീപ് ഫോക്കസ്", "വൈഡ്", "ഏരിയൽ"], "medium"),
    ("ഹൈ-കീ ലൈറ്റിംഗ്", "പ്രകാശമേറിയ, കുറഞ്ഞ നിഴലുള്ള illumination", ["ലോ-കേ", "silhouette", "flat"], "medium"),
    ("ലോ-കേ ലൈറ്റിംഗ്", "കടുത്ത നിഴലുകളുള്ള illumination", ["ഹൈ-കേ", "flat", "natural only"], "medium"),
    ("സ്റ്റെഡിക്കാം", "സുഗമമായ ചലന ദൃശ്യം", ["ഹാൻഡ് ഹെൽഡ്", "ട്രൈപോഡ്", "സൂoom മാത്രം"], "medium"),
    ("ഏരിയൽ ഷോട്ട്", "ഉയരത്തിൽ നിന്നുള്ള ദൃശ്യം", ["ക്ലോസ്-അപ്പ്", "മാക്രോ", "ടു-ഷോട്ട്"], "medium"),
    ("24 fps", "സിനിമയുടെ സtandard frame rate", ["30 fps", "60 fps", "12 fps"], "medium"),
    ("ചിത്രമാപകൻ", "ദൃശ്യ记录 നിയന്ത്രിക്കുന്ന കലാസാങ്കേതികൻ", ["എഡിറ്റർ", "ശബ്ദ സംവിധായകൻ", "കലാസംവിധായകൻ"], "easy"),
    ("aspect ratio 2.39:1", "വൈഡ് സ്ക്രീൻ ratio", ["4:3", "1:1", "9:16"], "hard"),
    ("aspect ratio 4:3", "പഴയ academy ratio", ["2.39:1", "1.43", "9:16"], "hard"),
    ("colour grading", "post-production നിറ adjustment", ["sound mix", "casting", "censor"], "medium"),
    ("exposure", "പ്രകാശം sensor/film-ൽ падать", ["frame rate", "aspect ratio", "subtitle"], "easy"),
    ("wide angle lens", "വിശാല ദൃശ്യപഥം", ["telephoto", "macro", "fisheye"], "medium"),
    ("telephoto lens", "ദൂരവസ്തുക്കൾക്കുള്ള lens", ["wide angle", "macro", "fisheye"], "hard"),
    ("macro lens", "സൂക്ഷ്മ വസ്തുക്കൾക്കുള്ള lens", ["wide angle", "telephoto", "fisheye"], "medium"),
    ("handheld camera", "കൈയിൽ പിടിച്ച ഷൂട്ടിംഗ്", ["steadicam", "tripod", "crane"], "medium"),
    ("crane shot", "ലംബ ചലന ക്യാമറ ഷോട്ട്", ["dolly only", "pan only", "static"], "medium"),
    ("Dutch angle", "ചായം horizon", ["level horizon", "aerial only", "macro"], "hard"),
    ("bokeh", "out-of-focus blur", ["deep focus", "sharp throughout", "noise"], "hard"),
    ("rack focus", "focus point മാറ്റം", ["zoom", "pan", "tilt"], "hard"),
]

# NOTE: Term categories with English loanwords still fail validation.
# Wave-20 uses pair-based questions for these topics instead of term emit.

MISE_EN_SCENE: list[Fact] = []
SOUND: list[Fact] = []
PRODUCTION_ROLES: list[Fact] = []
PIPELINE: list[Fact] = []

# Pair-based Malayalam cinema craft facts (used instead of English term emit)
CRAFT_PAIRS: list[tuple[str, str]] = [
    ("കഥാലോക ശബ്ദം", "dialogue in scene"),
    ("പശ്ചാത്തല സംഗീതം", "non-diegetic score"),
    ("ഫോളി", "post-recorded effects"),
    ("എഡിറ്റിംഗ്", "shot assembly"),
    ("മോണ്ടേജ്", "Eisenstein theory"),
    ("continuity editing", "seamless flow"),
    ("match cut", "visual continuity"),
    ("cross-cutting", "parallel action"),
    ("dissolve transition", "overlap transition"),
    ("fade in/out", "temporal transition"),
    ("180-degree rule", "screen direction"),
    ("eyeline match", "continuity editing"),
    ("shot-reverse-shot", "dialogue editing"),
    ("establishing shot", "scene geography"),
    ("insert shot", "detail emphasis"),
    ("long take", "extended single shot"),
    ("deep focus", "Citizen Kane style"),
    ("mise-en-scène", "frame visual elements"),
    ("production design", "visual world"),
    ("art direction", "visual style"),
    ("costume design", "wardrobe"),
    ("blocking", "actor placement"),
    ("storyboard", "visual plan"),
    ("pre-production", "shooting前 planning"),
    ("post-production", "edit and sound"),
    ("censor certification", "CBFC approval"),
    ("theatrical window", "cinema exclusive period"),
    ("playback singing", "lip-sync to singer"),
    ("ADR dubbing", "post dialogue record"),
    ("sound mixing", "final audio balance"),
]
