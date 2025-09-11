"""
Auto-generated CIDOC CRM property registry.
Generated from YAML specifications in codegen/specs/

This module provides:
- P: Dictionary of all P-properties with metadata
- DOMAIN: Lookup table from E-class to properties with that domain
- RANGE: Lookup table from E-class to properties with that range
"""

from typing import Dict, List, Any

P = {
    "P1": {
        "label": "is identified by",
        "domain": "E1",
        "range": "E41",
        "inverse": "P1i",
        "quantifier": "0..*",
        "aliases": ['IS_IDENTIFIED_BY'],
        "notes": "Identifies an entity with an appellation"
    },
    "P2": {
        "label": "has type",
        "domain": "E1",
        "range": "E55",
        "inverse": "P2i",
        "quantifier": "0..*",
        "aliases": ['HAS_TYPE'],
        "notes": "Assigns a type to an entity"
    },
    "P3": {
        "label": "has note",
        "domain": "E1",
        "range": "E62",
        "inverse": "P3i",
        "quantifier": "0..*",
        "aliases": ['HAS_NOTE'],
        "notes": "Adds a textual note to an entity"
    },
    "P4": {
        "label": "has time-span",
        "domain": "E2",
        "range": "E52",
        "inverse": "P4i",
        "quantifier": "0..1",
        "aliases": ['HAS_TIME_SPAN'],
        "notes": "Associates a temporal entity with its time-span"
    },
    "P7": {
        "label": "took place at",
        "domain": "E5",
        "range": "E53",
        "inverse": "P7i",
        "quantifier": "0..*",
        "aliases": ['TOOK_PLACE_AT'],
        "notes": "Specifies where an event took place"
    },
    "P11": {
        "label": "had participant",
        "domain": "E5",
        "range": "E39",
        "inverse": "P11i",
        "quantifier": "0..*",
        "aliases": ['HAD_PARTICIPANT'],
        "notes": "Identifies participants in an event"
    },
    "P53": {
        "label": "has current or former location",
        "domain": "E18",
        "range": "E53",
        "inverse": "P53i",
        "quantifier": "0..*",
        "aliases": ['HAS_CURRENT_LOCATION'],
        "notes": "Specifies the current or former location of a physical thing"
    },
    "P79": {
        "label": "beginning is qualified by",
        "domain": "E52",
        "range": "E61",
        "inverse": "P79i",
        "quantifier": "0..1",
        "aliases": ['BEGIN_OF_THE_BEGIN'],
        "notes": "Qualifies the beginning of a time-span"
    },
    "P80": {
        "label": "end is qualified by",
        "domain": "E52",
        "range": "E61",
        "inverse": "P80i",
        "quantifier": "0..1",
        "aliases": ['END_OF_THE_END'],
        "notes": "Qualifies the end of a time-span"
    },
    "P108": {
        "label": "was produced by",
        "domain": "E22",
        "range": "E12",
        "inverse": "P108i",
        "quantifier": "0..1",
        "aliases": ['WAS_PRODUCED_BY'],
        "notes": "Links a human-made object to its production event"
    },
    "P108i": {
        "label": "produced",
        "domain": "E12",
        "range": "E22",
        "inverse": "P108",
        "quantifier": "0..*",
        "aliases": ['PRODUCED'],
        "notes": "Inverse of was produced by"
    },
    "P1i": {
        "label": "identifies",
        "domain": "E41",
        "range": "E1",
        "inverse": "P1",
        "quantifier": "0..*",
        "aliases": ['IDENTIFIES'],
        "notes": "Inverse of is identified by"
    },
    "P2i": {
        "label": "is type of",
        "domain": "E55",
        "range": "E1",
        "inverse": "P2",
        "quantifier": "0..*",
        "aliases": ['IS_TYPE_OF'],
        "notes": "Inverse of has type"
    },
    "P3i": {
        "label": "is note of",
        "domain": "E62",
        "range": "E1",
        "inverse": "P3",
        "quantifier": "0..*",
        "aliases": ['IS_NOTE_OF'],
        "notes": "Inverse of has note"
    },
    "P4i": {
        "label": "is time-span of",
        "domain": "E52",
        "range": "E2",
        "inverse": "P4",
        "quantifier": "0..*",
        "aliases": ['IS_TIME_SPAN_OF'],
        "notes": "Inverse of has time-span"
    },
    "P7i": {
        "label": "witnessed",
        "domain": "E53",
        "range": "E5",
        "inverse": "P7",
        "quantifier": "0..*",
        "aliases": ['WITNESSED'],
        "notes": "Inverse of took place at"
    },
    "P11i": {
        "label": "participated in",
        "domain": "E39",
        "range": "E5",
        "inverse": "P11",
        "quantifier": "0..*",
        "aliases": ['PARTICIPATED_IN'],
        "notes": "Inverse of had participant"
    },
    "P53i": {
        "label": "is current or former location of",
        "domain": "E53",
        "range": "E18",
        "inverse": "P53",
        "quantifier": "0..*",
        "aliases": ['IS_CURRENT_LOCATION_OF'],
        "notes": "Inverse of has current or former location"
    },
    "P79i": {
        "label": "qualifies beginning of",
        "domain": "E61",
        "range": "E52",
        "inverse": "P79",
        "quantifier": "0..*",
        "aliases": ['QUALIFIES_BEGINNING_OF'],
        "notes": "Inverse of beginning is qualified by"
    },
    "P80i": {
        "label": "qualifies end of",
        "domain": "E61",
        "range": "E52",
        "inverse": "P80",
        "quantifier": "0..*",
        "aliases": ['QUALIFIES_END_OF'],
        "notes": "Inverse of end is qualified by"
    },
    "P5": {
        "label": "consists of",
        "domain": "E18",
        "range": "E18",
        "inverse": "P5i",
        "quantifier": "0..*",
        "aliases": ['CONSISTS_OF'],
        "notes": "Physical thing consists of other physical things"
    },
    "P5i": {
        "label": "forms part of",
        "domain": "E18",
        "range": "E18",
        "inverse": "P5",
        "quantifier": "0..*",
        "aliases": ['FORMS_PART_OF'],
        "notes": "Inverse of consists of"
    },
    "P8": {
        "label": "took place on or before",
        "domain": "E5",
        "range": "E61",
        "inverse": "P8i",
        "quantifier": "0..*",
        "aliases": ['TOOK_PLACE_ON_OR_BEFORE'],
        "notes": "Event took place on or before a specific time"
    },
    "P8i": {
        "label": "was the latest time of",
        "domain": "E61",
        "range": "E5",
        "inverse": "P8",
        "quantifier": "0..*",
        "aliases": ['WAS_THE_LATEST_TIME_OF'],
        "notes": "Inverse of took place on or before"
    },
    "P9": {
        "label": "consists of",
        "domain": "E4",
        "range": "E4",
        "inverse": "P9i",
        "quantifier": "0..*",
        "aliases": ['CONSISTS_OF'],
        "notes": "Period consists of other periods"
    },
    "P9i": {
        "label": "forms part of",
        "domain": "E4",
        "range": "E4",
        "inverse": "P9",
        "quantifier": "0..*",
        "aliases": ['FORMS_PART_OF'],
        "notes": "Inverse of consists of"
    },
    "P10": {
        "label": "falls within",
        "domain": "E4",
        "range": "E4",
        "inverse": "P10i",
        "quantifier": "0..*",
        "aliases": ['FALLS_WITHIN'],
        "notes": "Period falls within another period"
    },
    "P10i": {
        "label": "contains",
        "domain": "E4",
        "range": "E4",
        "inverse": "P10",
        "quantifier": "0..*",
        "aliases": ['CONTAINS'],
        "notes": "Inverse of falls within"
    },
    "P12": {
        "label": "occurred in the presence of",
        "domain": "E5",
        "range": "E77",
        "inverse": "P12i",
        "quantifier": "0..*",
        "aliases": ['OCCURRED_IN_THE_PRESENCE_OF'],
        "notes": "Event occurred in the presence of a persistent item"
    },
    "P12i": {
        "label": "was present at",
        "domain": "E77",
        "range": "E5",
        "inverse": "P12",
        "quantifier": "0..*",
        "aliases": ['WAS_PRESENT_AT'],
        "notes": "Inverse of occurred in the presence of"
    },
    "P13": {
        "label": "destroyed",
        "domain": "E6",
        "range": "E18",
        "inverse": "P13i",
        "quantifier": "0..*",
        "aliases": ['DESTROYED'],
        "notes": "Destruction event destroyed a physical thing"
    },
    "P13i": {
        "label": "was destroyed by",
        "domain": "E18",
        "range": "E6",
        "inverse": "P13",
        "quantifier": "0..*",
        "aliases": ['WAS_DESTROYED_BY'],
        "notes": "Inverse of destroyed"
    },
    "P14": {
        "label": "carried out by",
        "domain": "E7",
        "range": "E39",
        "inverse": "P14i",
        "quantifier": "0..*",
        "aliases": ['CARRIED_OUT_BY'],
        "notes": "Activity was carried out by an actor"
    },
    "P14i": {
        "label": "performed",
        "domain": "E39",
        "range": "E7",
        "inverse": "P14",
        "quantifier": "0..*",
        "aliases": ['PERFORMED'],
        "notes": "Inverse of carried out by"
    },
    "P15": {
        "label": "was influenced by",
        "domain": "E7",
        "range": "E1",
        "inverse": "P15i",
        "quantifier": "0..*",
        "aliases": ['WAS_INFLUENCED_BY'],
        "notes": "Activity was influenced by another entity"
    },
    "P15i": {
        "label": "influenced",
        "domain": "E1",
        "range": "E7",
        "inverse": "P15",
        "quantifier": "0..*",
        "aliases": ['INFLUENCED'],
        "notes": "Inverse of was influenced by"
    },
    "P16": {
        "label": "used specific object",
        "domain": "E7",
        "range": "E19",
        "inverse": "P16i",
        "quantifier": "0..*",
        "aliases": ['USED_SPECIFIC_OBJECT'],
        "notes": "Activity used a specific physical object"
    },
    "P16i": {
        "label": "was used for",
        "domain": "E19",
        "range": "E7",
        "inverse": "P16",
        "quantifier": "0..*",
        "aliases": ['WAS_USED_FOR'],
        "notes": "Inverse of used specific object"
    },
    "P17": {
        "label": "was motivated by",
        "domain": "E7",
        "range": "E1",
        "inverse": "P17i",
        "quantifier": "0..*",
        "aliases": ['WAS_MOTIVATED_BY'],
        "notes": "Activity was motivated by another entity"
    },
    "P17i": {
        "label": "motivated",
        "domain": "E1",
        "range": "E7",
        "inverse": "P17",
        "quantifier": "0..*",
        "aliases": ['MOTIVATED'],
        "notes": "Inverse of was motivated by"
    },
    "P19": {
        "label": "was intended use",
        "domain": "E7",
        "range": "E55",
        "inverse": "P19i",
        "quantifier": "0..*",
        "aliases": ['WAS_INTENDED_USE'],
        "notes": "Activity was intended for a specific use"
    },
    "P19i": {
        "label": "was use of",
        "domain": "E55",
        "range": "E7",
        "inverse": "P19",
        "quantifier": "0..*",
        "aliases": ['WAS_USE_OF'],
        "notes": "Inverse of was intended use"
    },
    "P20": {
        "label": "had specific purpose",
        "domain": "E7",
        "range": "E5",
        "inverse": "P20i",
        "quantifier": "0..*",
        "aliases": ['HAD_SPECIFIC_PURPOSE'],
        "notes": "Activity had a specific purpose"
    },
    "P20i": {
        "label": "was purpose of",
        "domain": "E5",
        "range": "E7",
        "inverse": "P20",
        "quantifier": "0..*",
        "aliases": ['WAS_PURPOSE_OF'],
        "notes": "Inverse of had specific purpose"
    },
    "P21": {
        "label": "had general purpose",
        "domain": "E7",
        "range": "E55",
        "inverse": "P21i",
        "quantifier": "0..*",
        "aliases": ['HAD_GENERAL_PURPOSE'],
        "notes": "Activity had a general purpose"
    },
    "P21i": {
        "label": "was purpose of",
        "domain": "E55",
        "range": "E7",
        "inverse": "P21",
        "quantifier": "0..*",
        "aliases": ['WAS_PURPOSE_OF'],
        "notes": "Inverse of had general purpose"
    },
    "P22": {
        "label": "transferred title to",
        "domain": "E8",
        "range": "E39",
        "inverse": "P22i",
        "quantifier": "0..*",
        "aliases": ['TRANSFERRED_TITLE_TO'],
        "notes": "Acquisition transferred title to an actor"
    },
    "P22i": {
        "label": "acquired title through",
        "domain": "E39",
        "range": "E8",
        "inverse": "P22",
        "quantifier": "0..*",
        "aliases": ['ACQUIRED_TITLE_THROUGH'],
        "notes": "Inverse of transferred title to"
    },
    "P23": {
        "label": "transferred title from",
        "domain": "E8",
        "range": "E39",
        "inverse": "P23i",
        "quantifier": "0..*",
        "aliases": ['TRANSFERRED_TITLE_FROM'],
        "notes": "Acquisition transferred title from an actor"
    },
    "P23i": {
        "label": "surrendered title through",
        "domain": "E39",
        "range": "E8",
        "inverse": "P23",
        "quantifier": "0..*",
        "aliases": ['SURRENDERED_TITLE_THROUGH'],
        "notes": "Inverse of transferred title from"
    },
    "P24": {
        "label": "transferred title of",
        "domain": "E8",
        "range": "E18",
        "inverse": "P24i",
        "quantifier": "0..*",
        "aliases": ['TRANSFERRED_TITLE_OF'],
        "notes": "Acquisition transferred title of a physical thing"
    },
    "P24i": {
        "label": "changed ownership through",
        "domain": "E18",
        "range": "E8",
        "inverse": "P24",
        "quantifier": "0..*",
        "aliases": ['CHANGED_OWNERSHIP_THROUGH'],
        "notes": "Inverse of transferred title of"
    },
    "P25": {
        "label": "moved",
        "domain": "E9",
        "range": "E18",
        "inverse": "P25i",
        "quantifier": "0..*",
        "aliases": ['MOVED'],
        "notes": "Move event moved a physical thing"
    },
    "P25i": {
        "label": "moved by",
        "domain": "E18",
        "range": "E9",
        "inverse": "P25",
        "quantifier": "0..*",
        "aliases": ['MOVED_BY'],
        "notes": "Inverse of moved"
    },
    "P26": {
        "label": "moved to",
        "domain": "E9",
        "range": "E53",
        "inverse": "P26i",
        "quantifier": "0..*",
        "aliases": ['MOVED_TO'],
        "notes": "Move event moved to a place"
    },
    "P26i": {
        "label": "was destination of",
        "domain": "E53",
        "range": "E9",
        "inverse": "P26",
        "quantifier": "0..*",
        "aliases": ['WAS_DESTINATION_OF'],
        "notes": "Inverse of moved to"
    },
    "P27": {
        "label": "moved from",
        "domain": "E9",
        "range": "E53",
        "inverse": "P27i",
        "quantifier": "0..*",
        "aliases": ['MOVED_FROM'],
        "notes": "Move event moved from a place"
    },
    "P27i": {
        "label": "was origin of",
        "domain": "E53",
        "range": "E9",
        "inverse": "P27",
        "quantifier": "0..*",
        "aliases": ['WAS_ORIGIN_OF'],
        "notes": "Inverse of moved from"
    },
    "P28": {
        "label": "custody surrendered by",
        "domain": "E10",
        "range": "E39",
        "inverse": "P28i",
        "quantifier": "0..*",
        "aliases": ['CUSTODY_SURRENDERED_BY'],
        "notes": "Transfer of custody surrendered by an actor"
    },
    "P28i": {
        "label": "surrendered custody through",
        "domain": "E39",
        "range": "E10",
        "inverse": "P28",
        "quantifier": "0..*",
        "aliases": ['SURRENDERED_CUSTODY_THROUGH'],
        "notes": "Inverse of custody surrendered by"
    },
    "P29": {
        "label": "custody received by",
        "domain": "E10",
        "range": "E39",
        "inverse": "P29i",
        "quantifier": "0..*",
        "aliases": ['CUSTODY_RECEIVED_BY'],
        "notes": "Transfer of custody received by an actor"
    },
    "P29i": {
        "label": "received custody through",
        "domain": "E39",
        "range": "E10",
        "inverse": "P29",
        "quantifier": "0..*",
        "aliases": ['RECEIVED_CUSTODY_THROUGH'],
        "notes": "Inverse of custody received by"
    },
    "P30": {
        "label": "transferred custody of",
        "domain": "E10",
        "range": "E18",
        "inverse": "P30i",
        "quantifier": "0..*",
        "aliases": ['TRANSFERRED_CUSTODY_OF'],
        "notes": "Transfer of custody transferred custody of a physical thing"
    },
    "P30i": {
        "label": "custody transferred through",
        "domain": "E18",
        "range": "E10",
        "inverse": "P30",
        "quantifier": "0..*",
        "aliases": ['CUSTODY_TRANSFERRED_THROUGH'],
        "notes": "Inverse of transferred custody of"
    }
}

DOMAIN = {
    "E1": ['P1', 'P2', 'P3', 'P15i', 'P17i'],
    "E2": ['P4'],
    "E5": ['P7', 'P11', 'P8', 'P12', 'P20i'],
    "E18": ['P53', 'P5', 'P5i', 'P13i', 'P24i', 'P25i', 'P30i'],
    "E52": ['P79', 'P80', 'P4i'],
    "E22": ['P108'],
    "E12": ['P108i'],
    "E41": ['P1i'],
    "E55": ['P2i', 'P19i', 'P21i'],
    "E62": ['P3i'],
    "E53": ['P7i', 'P53i', 'P26i', 'P27i'],
    "E39": ['P11i', 'P14i', 'P22i', 'P23i', 'P28i', 'P29i'],
    "E61": ['P79i', 'P80i', 'P8i'],
    "E4": ['P9', 'P9i', 'P10', 'P10i'],
    "E77": ['P12i'],
    "E6": ['P13'],
    "E7": ['P14', 'P15', 'P16', 'P17', 'P19', 'P20', 'P21'],
    "E19": ['P16i'],
    "E8": ['P22', 'P23', 'P24'],
    "E9": ['P25', 'P26', 'P27'],
    "E10": ['P28', 'P29', 'P30']
}

RANGE = {
    "E41": ['P1'],
    "E55": ['P2', 'P19', 'P21'],
    "E62": ['P3'],
    "E52": ['P4', 'P79i', 'P80i'],
    "E53": ['P7', 'P53', 'P26', 'P27'],
    "E39": ['P11', 'P14', 'P22', 'P23', 'P28', 'P29'],
    "E61": ['P79', 'P80', 'P8'],
    "E12": ['P108'],
    "E22": ['P108i'],
    "E1": ['P1i', 'P2i', 'P3i', 'P15', 'P17'],
    "E2": ['P4i'],
    "E5": ['P7i', 'P11i', 'P8i', 'P12i', 'P20'],
    "E18": ['P53i', 'P5', 'P5i', 'P13', 'P24', 'P25', 'P30'],
    "E4": ['P9', 'P9i', 'P10', 'P10i'],
    "E77": ['P12'],
    "E6": ['P13i'],
    "E7": ['P14i', 'P15i', 'P16i', 'P17i', 'P19i', 'P20i', 'P21i'],
    "E19": ['P16'],
    "E8": ['P22i', 'P23i', 'P24i'],
    "E9": ['P25i', 'P26i', 'P27i'],
    "E10": ['P28i', 'P29i', 'P30i']
}
