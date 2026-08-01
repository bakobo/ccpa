"""The regulation sources, and what the Office of Administrative Law says happened to each section.

CCR Title 11, Division 6, Chapter 1 is not published as one current text anywhere we can reach.
`govt.westlaw.com/calregs` returns 403 to programmatic access, so the source of record is the
CPPA's own rulemaking PDFs (`this.i` @pgu273) — and those are *per rulemaking action*, not
consolidated. Two are needed:

    2023 package  OAL-approved 2023-03-29, effective the same day.  43 sections.
    2025 package  OAL-approved 2025-09-22, effective 2026-01-01.    49 sections.

Neither is the whole chapter. The 2025 text reprints only the sections that action touched, so
twelve sections exist solely in the 2023 text — and whether those are *unchanged* or *repealed*
cannot be inferred from the two texts alone. Guessing here would be the exact failure this repo
exists to avoid, so the answer comes from the OAL Notice of Approval, which states it:

    Adopt sections: 7120 7121 7122 7123 7124 7150 7151 7152 7153 7154 7155 7156 7157
                    7200 7220 7221 7222 7270 7271
    Amend sections: 7001 7002 7003 7004 7010 7011 7012 7013 7014 7015 7020 7021 7022
                    7023 7024 7025 7026 7027 7028 7050 7051 7053 7060 7062 7063 7070
                    7080 7102 7300 7302
    (no repeal section)

**Nothing was repealed.** So the twelve sections absent from the 2025 text remain in force as
enacted in 2023.

The lists are transcribed here rather than parsed from the PDF at run time. The NOA is a scanned
document and extracts with OCR noise — "7021" comes through as "70221" — so a parser would be
fragile in a way that fails silently. Transcribed, they act as an **oracle**: `harvest-regs.py`
refuses to store anything unless the sections it splits out of the 2025 text are exactly
ADOPTED | AMENDED. If a future rulemaking changes the shape, the harvest stops instead of
producing a plausible corpus.
"""

# OAL Matter Number 2025-0808-04, filed with the Secretary of State 2025-09-22.
NOA_URL = "https://cppa.ca.gov/regulations/pdf/ccpa_updates_cyber_risk_admt_noa.pdf"
NOA_MATTER = "OAL 2025-0808-04"

ADOPTED_2025 = {
    "7120", "7121", "7122", "7123", "7124",
    "7150", "7151", "7152", "7153", "7154", "7155", "7156", "7157",
    "7200", "7220", "7221", "7222", "7270", "7271",
}

AMENDED_2025 = {
    "7001", "7002", "7003", "7004", "7010", "7011", "7012", "7013", "7014", "7015",
    "7020", "7021", "7022", "7023", "7024", "7025", "7026", "7027", "7028",
    "7050", "7051", "7053", "7060", "7062", "7063", "7070", "7080", "7102",
    "7300", "7302",
}

REPEALED_2025 = set()

PACKAGES = [
    {
        "key": "2023",
        "url": "https://cppa.ca.gov/regulations/pdf/20230329_final_regs_text.pdf",
        "citation_suffix": "(2023 text)",
        "effective": "2023-03-29",
        "version_id": "CPPA-final-regs-2023-03-29",
        "note": "CCPA Regulations as approved by OAL 2023-03-29",
    },
    {
        "key": "2025",
        "url": "https://cppa.ca.gov/regulations/pdf/ccpa_updates_cyber_risk_admt_appr_text.pdf",
        "citation_suffix": "",
        "effective": "2026-01-01",
        "version_id": "CPPA-approved-text-2025-09-22-eff-2026-01-01",
        "note": (
            "CCPA Updates, Cybersecurity Audits, Risk Assessments, ADMT and Insurance "
            "Regulations; approved by OAL 2025-09-22 (" + NOA_MATTER + "), effective 2026-01-01"
        ),
    },
]

SUPERSEDED_NOTE = (
    "Superseded 2026-01-01 by the CCPA Updates, Cyber, Risk, ADMT and Insurance Regulations "
    "(" + NOA_MATTER + "). Retained as the text in force from 2023-03-29 to 2025-12-31."
)
