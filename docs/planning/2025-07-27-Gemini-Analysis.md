# Universal Taxonomy Implementation Plan

## 1. Overview

This document outlines the plan to transition our numismatic data to a new, universal taxonomy. The goal is to implement a flexible data model that can accommodate coins and banknotes from around the world, while also preserving the rich detail of our existing data.

This new structure will replace the current series-based files with a more granular `issue`-based system.

## 2. Target Data Model

The core of the new taxonomy is the `issue` object. Each unique coin or banknote issue (e.g., a specific year, mint, and variety) will be represented as a single JSON document.

Here is the target structure for a single coin issue, using the 1909-S VDB Lincoln Cent as an example:

```json
{
  "issue_id": "US-LWC-1909-S-VDB",
  "object_type": "coin",
  "series_id": "lincoln_wheat_cent",
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
  "issue_year": 1909,
  "mint_id": "S",
  "date_range_context": {
    "start": 1909,
    "end": 1909,
    "authority_period": {
      "entity_type": "republic",
      "leader": {
        "id": "theodore_roosevelt",
        "role": "president"
      }
    }
  },
  "specifications": {
    "weight_grams": 3.11,
    "diameter_mm": 19.05,
    "edge": "plain",
    "composition_key": "bronze_95_4_1"
  },
  "sides": {
    "obverse": {
      "design_id": "lincoln_wheat_obverse_1909",
      "primary_element": {
        "type": "portrait",
        "subject_id": "abraham_lincoln",
        "description": "Portrait of Abraham Lincoln"
      },
      "inscriptions": [
        {"text": "IN GOD WE TRUST", "position": "top_arc"},
        {"text": "LIBERTY", "position": "left_field"},
        {"text": "1909", "position": "right_field"}
      ],
      "designer_id": "victor_brenner"
    },
    "reverse": {
      "design_id": "wheat_ears_reverse_1909_vdb",
      "primary_element": {
        "type": "agricultural",
        "subject_id": "wheat_ears",
        "description": "Two ears of durum wheat"
      },
      "inscriptions": [
        {"text": "ONE CENT", "position": "center"},
        {"text": "UNITED STATES OF AMERICA", "position": "bottom_arc"},
        {"text": "E PLURIBUS UNUM", "position": "top_arc"}
      ],
      "designer_id": "victor_brenner",
      "designer_mark": "VDB"
    }
  },
  "mintage": {
    "business_strikes": 484000,
    "proof_strikes": 0
  },
  "rarity": "key"
}
```

## 3. Key Data Structures and Concepts

-   **`issue`**: The fundamental unit of the new system. Each `issue` represents a unique numismatic item.
-   **`issuing_entity`**: A flexible object to describe the authority that issued the coin or banknote, including country, political entity, and monetary system.
-   **`sides`**: An object containing details for the obverse and reverse (or front and back) of the item, including design elements and inscriptions.
-   **`Universal Subject Registry`**: A new, centralized registry to define and describe any person, symbol, or object that appears on a coin or banknote (e.g., Abraham Lincoln, Queen Elizabeth II, an eagle, the Statue of Liberty). This avoids hardcoding specific roles or figures.
-   **`specifications`**: Retains critical physical data like weight, diameter, and composition, adapted for both coins and banknotes.

## 4. Implementation Steps

### 4.1. Schema Definition
Define and implement JSON schemas for the new data models, including `issue`, `issuing_entity`, and the `Universal Subject Registry`.

### 4.2. Create New Reference Data Files
Create the necessary files for the `Universal Subject Registry`. An example file, `subject_registry.example.json`, will be provided in the `docs/planning` directory to serve as a starting point.

### 4.3. Data Migration
Develop a script to migrate the existing US coin data from the current structure (e.g., `data/us/coins/cents.json`) to the new `issue`-based model. The script must map all relevant fields from the old structure to the new one. Each entry in the current `coins` array within a series will become a distinct `issue` document.

### 4.4. Data Population and Integrity
The migration script will populate many fields automatically. However, new contextual fields will require separate, manual research.

**Note on Data Integrity:** Under no circumstances should placeholder or unverified information be entered into the production dataset. All new contextual data, such as the `authority_period`, `leader` details, or the information within the `Universal Subject Registry`, must be populated based on thorough, independent research. The examples provided in this document and accompanying files are for structural guidance only and may not be accurate.

## 5. Example Subject Registry

A separate example file named `subject_registry.example.json` is provided to illustrate the structure of the Universal Subject Registry. This file contains a few sample entries to guide development.
