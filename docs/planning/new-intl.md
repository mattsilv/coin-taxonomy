# Universal Coin Taxonomy: Enhanced Abstract Design

## Why Both Sides Matter

Every coin tells two stories - one on each face. The **obverse** (heads) typically features the issuing authority's symbol of sovereignty, while the **reverse** (tails) showcases national symbols, commemorative designs, or denominational elements. This duality isn't arbitrary; it's fundamental to how coins communicate value, authority, and cultural identity.

Consider these patterns across cultures:
- **Authority Side**: Rulers (US Presidents), symbols (Britannia), or state emblems (Canadian Maple Leaf)
- **Value Side**: Denominational designs, national symbols, or commemorative themes

## Proposed Abstract Structure

### Core Entity Model

```json
{
  "coin_id": "US-CENT-1909-S-VDB",
  "issuing_entity": {
    "country_code": "US",
    "authority_name": "United States of America",
    "monetary_system": "decimal",
    "currency_unit": "dollar"
  },
  "denomination": {
    "face_value": 0.01,
    "unit_name": "cent",
    "common_names": ["penny"],
    "system_fraction": "1/100 dollar"
  },
  "date_range": {
    "start": 1909,
    "end": 1909,
    "authority_period": {
      "entity_type": "republic",
      "leader": {
        "id": "theodore_roosevelt",
        "role": "president",
        "term": {"start": 1901, "end": 1909}
      }
    }
  },
  "sides": {
    "obverse": {
      "design_id": "lincoln_wheat_obverse_1909",
      "primary_element": {
        "type": "portrait",
        "subject_id": "abraham_lincoln",
        "subject_type": "historical_figure",
        "facing": "right"
      },
      "inscriptions": [
        {"text": "IN GOD WE TRUST", "position": "top"},
        {"text": "LIBERTY", "position": "left"},
        {"text": "1909", "position": "right"}
      ],
      "designer_id": "victor_brenner"
    },
    "reverse": {
      "design_id": "wheat_ears_reverse_1909",
      "primary_element": {
        "type": "agricultural",
        "subject_id": "wheat_ears",
        "subject_type": "flora",
        "arrangement": "flanking"
      },
      "inscriptions": [
        {"text": "ONE CENT", "position": "center"},
        {"text": "UNITED STATES OF AMERICA", "position": "top"},
        {"text": "E PLURIBUS UNUM", "position": "middle"}
      ],
      "designer_id": "victor_brenner",
      "designer_mark": "VDB"
    }
  }
}
```

### Universal Subject Registry

Instead of hardcoding "monarch" or "president", we use a flexible subject system:

```json
{
  "subject_registry": {
    "abraham_lincoln": {
      "type": "historical_figure",
      "roles": ["president"],
      "nationality": "American",
      "life_dates": {"birth": 1809, "death": 1865},
      "coin_appearances": ["cent_1909_present", "dollar_2009_bicentennial"]
    },
    "elizabeth_ii": {
      "type": "historical_figure", 
      "roles": ["monarch", "head_of_state"],
      "nationality": "British",
      "life_dates": {"birth": 1926, "death": 2022},
      "reign": {"start": 1952, "end": 2022},
      "coin_appearances": ["all_british_1953_2022", "canadian_1953_2022"]
    },
    "britannia": {
      "type": "allegorical_figure",
      "represents": ["Britain", "maritime_power"],
      "first_appearance": 1672,
      "coin_appearances": ["penny_1797_1967", "two_pound_1997_present"]
    },
    "liberty": {
      "type": "allegorical_figure",
      "represents": ["freedom", "democracy"],
      "variations": ["seated", "standing", "walking", "head"],
      "coin_appearances": ["multiple_us_series"]
    }
  }
}
```

### Design Elements Taxonomy

```json
{
  "design_elements": {
    "portraits": {
      "orientation": ["left", "right", "facing"],
      "style": ["realistic", "idealized", "symbolic"],
      "elements": ["bare", "laureate", "crowned", "capped"]
    },
    "symbols": {
      "national": ["eagles", "shields", "maple_leaves", "harps"],
      "allegorical": ["liberty", "britannia", "marianne"],
      "architectural": ["buildings", "monuments", "bridges"],
      "natural": ["mountains", "rivers", "flora", "fauna"]
    },
    "patterns": {
      "geometric": ["stars", "dots", "lines"],
      "heraldic": ["arms", "crests", "shields"],
      "decorative": ["wreaths", "scrollwork", "borders"]
    }
  }
}
```

## Implementation Examples

### US Lincoln Cent
```json
{
  "series_id": "lincoln_cent",
  "obverse": {
    "primary_element": {
      "type": "portrait",
      "subject_id": "abraham_lincoln",
      "subject_type": "historical_figure"
    }
  },
  "authority_context": {
    "entity_type": "federal_republic",
    "continuity": "continuous_since_1789"
  }
}
```

### British Victorian Florin
```json
{
  "series_id": "victoria_florin",
  "obverse": {
    "primary_element": {
      "type": "portrait",
      "subject_id": "victoria",
      "subject_type": "historical_figure",
      "variation": "gothic_portrait"
    }
  },
  "authority_context": {
    "entity_type": "constitutional_monarchy",
    "ruler_id": "victoria",
    "ruler_role": "monarch"
  }
}
```

### Canadian Maple Leaf
```json
{
  "series_id": "maple_leaf_dollar",
  "reverse": {
    "primary_element": {
      "type": "flora",
      "subject_id": "maple_leaf",
      "subject_type": "national_symbol"
    }
  },
  "authority_context": {
    "entity_type": "constitutional_monarchy",
    "nominal_ruler_id": "elizabeth_ii",
    "effective_authority": "parliament_of_canada"
  }
}
```

### Japanese Yen
```json
{
  "series_id": "heisei_yen",
  "obverse": {
    "primary_element": {
      "type": "flora",
      "subject_id": "paulownia",
      "subject_type": "imperial_symbol"
    }
  },
  "authority_context": {
    "entity_type": "constitutional_monarchy",
    "era_name": "heisei",
    "ruler_id": "akihito",
    "ruler_role": "emperor"
  }
}
```

## Benefits of This Approach

1. **Universal Application**: Works for republics, monarchies, theocracies, or any government type
2. **Historical Continuity**: Handles regime changes, revolutions, and succession
3. **Cultural Sensitivity**: Avoids Western-centric terminology
4. **Design Searchability**: Find all coins with eagles, portraits, or buildings
5. **Cross-Reference Power**: Link Washington across quarters, dollars, and commemoratives
6. **Temporal Flexibility**: Track how the same subject appears differently over time

## Migration Path

Existing US-centric data migrates easily:
- "Washington Quarter" → subject_id: "george_washington"
- "Mercury Dime" → subject_id: "liberty_winged"
- Designer names → designer_id with registry lookup

## Query Examples

With this structure, you can ask:
- "Show all coins featuring eagles"
- "Find coins from constitutional monarchies"
- "List all allegorical figures on world coins"
- "Which coins feature the same person on both sides?"
- "Track portrait evolution of a specific ruler"

This abstraction creates a truly universal taxonomy while preserving the rich detail that makes each coin unique.