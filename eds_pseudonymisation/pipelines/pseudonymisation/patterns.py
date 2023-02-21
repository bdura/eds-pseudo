import re

from edsnlp.utils.regex import make_pattern

# Phones
delimiters = ["", r"\.", r"\-", " "]
# phone_pattern = make_pattern(
#    [
#        r"((\+ ?3 ?3|0 ?0 ?3 ?3)|0 ?[1-8]) ?" + d.join([r"(\d ?){2}"] * 4)
#        for d in delimiters
#    ]
# )
phone_pattern = (
    r"("
    r"(?<!\d[ .-]{,3})\b"
    r"((?:(?:\+|00)33\s?[.]\s?(?:\(0\)\s?[.]\s?)?|0)[1-9](?:(?:[.]\d{2}){4}|\d{2}(?:[.]\d{3}){2})(?![\d])"
    r"|(?:(?:\+|00)33\s?[-]\s?(?:\(0\)\s?[-]\s?)?|0)[1-9](?:(?:[-]\d{2}){4}|\d{2}(?:[-]\d{3}){2})(?![\d])"
    r"|(?:(?:\+|00)33\s?[-]\s?(?:\(0\)\s)?|0)[1-9](?:(?:[ ]?\d{2}){4}|\d{2}(?:[ ]?\d{3}){2})(?![\d]))"
    r"\b(?![ .-]{,3}\d)"
    r")"
)

# IPP
ipp_pattern = r"(" r"(?<!\d[ .-]{,3})\b" r"(8(\d ?){9})" r"\b(?![ .-]{,3}\d)" r")"

# NDA
#nda_pattern = (
#    r"("
#    r"(?<!\d[ .-]{,3})\b"
#    r"(?:0 ?[159]|1 ?[0146]|2 ?[12689]|3 ?[2368]|4 ?[12479]"
#    r"|5 ?3|6 ?[14689]|7 ?[2369]|8 ?[478]|9 ?[0569]|A ?G) ?(\d ?){7,8}"
#    r"\b(?![ .-]{,3}\d)"
#    r")"
#)

nda_pattern = r"""(?x)
(?<=(?:
    (?:(?i:
        (?:(?:no|n°|numero|no\s+d[e'‘]|n°\s+d[e'‘]|numero\s+d[e'‘])\s+)?
        (?:examen|demande|sejour|dossier)
    ))
|(?:Examen|Demande|Sejour)
)\s*:?\s*)
\b
(
    \d{2,}[A-Z]?[A-Z]?\d*(?:[-]\d+)?
    |\d*[A-Z]?[A-Z]?\d{2,}(?:[-]\d+)?
)
\b
(?![-/+\\_])
"""

# Mail
mail_pattern = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?: ?\. ?[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*") ?@ ?(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])? ?\. ?)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?) ?\. ?){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""  # noqa


# Zip
zip_pattern = (
    r"("
    r"(?<!\d[ .-°]{,3})\b"
    r"((?:(?:[0-8] [0-9])|(9 [0-5])|(2 [abAB]))\s?([0-9] ){2}[0-9]|"
    r"((?:(?:[0-8][0-9])|(9[0-5])|(2[abAB]))\s?([0-9]){2}[0-9]))"
    r"\b(?![ .-]{,3}\d)"
    r")"
)

# NSS
nss_pattern = r"""(?x)
# No digits just before on the same line
(?<!\d[ .-/+=_]{,3})\b
(    
# Sex
    (?:[1-2])[ ]?
# Year of birth
    (?:([0-9][ ]?){2})[ ]?
# Month of birth
    (?:0[ ]?[0-9]|[2-35-9][ ]?[0-9]|[14][ ]?[0-2])[ ]?
# Location of birth
    (?:
        (?:
            0[ ]?[1-9]
            |[1-8][ ]?[0-9]
            |9[ ]?[0-69]
            |2[ ]?[abAB]
        )[ ]?
        (?:
            0[ ]?0[ ]?[1-9]|0[ ]?[1-9][ ]?[0-9]|
            [1-8][ ]?([0-9][ ]?){2}|9[ ]?[0-8][ ]?[0-9]|9[ ]?9[ ]?0
        )
        |(?:9[ ]?[78][ ]?[0-9])[ ]?(?:0[ ]?[1-9]|[1-8][ ]?[0-9]|9 ?0)
    )[ ]?
# Birth number 001-999
    (?:0[ ]?0[ ]?[1-9]|0[ ]?[1-9][ ]?[0-9]|[1-9][ ]?([0-9][ ]?){2})[ ]?
# Control key
    (?:0[ ]?[1-9]|[1-8][ ]?[0-9]|9[ ]?[0-7])
|
# Temporary NSS
    [3478][ ]?(?:[0-9][ ]?){14}
)
# Not followed by digits on the same line
\b(?![ .-]{,3}\d)
"""

Xxxxx = r"[A-Z]\p{Ll}+"
XXxX_ = r"[A-Z][A-Z\p{Ll}-]"
sep = r"(?:[ ]*|-)?"
person_patterns = [
    rf"""(?x)
(?<![/+])
\b
(?:[Dd]r[.]?|[Dd]octeur|[mM]r?[.]?|[Ii]nterne[ ]?:|[Ee]xterne[ ]?:|[Mm]onsieur|[Mm]adame|[Rr].f.rent[ ]?:|[P]r[.]?|[Pp]rofesseure?|[Mm]me[.]?|[Ee]nfant|[Mm]lle)[ ]+
(?:
    (?P<LN0>[A-Z][A-Z](?:{sep}(?:ep[.]|de|[A-Z]+))*)[ ]+(?P<FN0>{Xxxxx}(?:{sep}{Xxxxx})*)
    |(?P<FN1>{Xxxxx}(?:{sep}{Xxxxx})*)[ ]+(?P<LN1>[A-Z][A-Z]+(?:{sep}(?:ep[.]|de|[A-Z]+))*)
    |(?P<LN3>{Xxxxx}(?:(?:-|[ ]de[ ]|[ ]ep[.][ ]){Xxxxx})*)[ ]+(?P<FN2>{Xxxxx}(?:-{Xxxxx})*)
    |(?P<LN2>{XXxX_}+(?:{sep}{XXxX_}+)*)
)
\b(?![/+])
""",
    rf"""
\b
(?<![/+%])
(?P<FN0>[A-Z][.])\s+(?P<LN0>{XXxX_}+(?:{sep}{XXxX_}+)*)
\b(?![/+%])
""",
]


common_medical_terms = {
    "EVA",
    "GE",
    "BIO",
    "SAU",
    "MEDICAL",
    "PA",
    "AVC",
    "PO",
    "OMS",
    "IVA",
    "AD",
}


street_patterns = ["rue", "route", "allée", "boulevard", "bd", "chemin"]
street_name_piece = "(?:[A-Z][A-Za-zéà]+|de|du|la|le|des)"
address_patterns = [
    rf"""(?x)
(
    (?:([1-9]\d*)\s+)?
    (?i:(?:(?:{'|'.join(map(re.escape, street_patterns))})\s+))
    (?:(?:{street_name_piece}\s+)*{street_name_piece})
)
(?=
    (?:[,]?\s*(?P<VILLE>[A-Z]+)\s+)?
    (?i:(?P<ZIP>(?:\s+\d{{2}}\s*?\d{{3}})|(?:[1-9]|1[0-9]|20)[èe]m?e?)?)
)
"""
]

patterns = dict(
    # ADRESSE=address_patterns,
    # DATE
    # DATE_NAISSANCE
    # HOPITAL
    IPP=ipp_pattern,
    MAIL=mail_pattern,
    TEL=phone_pattern,
    NDA=nda_pattern,
    # NOM
    # PRENOM
    SECU=nss_pattern,
    # VILLE
    # ZIP=zip_pattern,
)
