---
date: 2026-02-27
topic: taxonomy-bulletproofing-audit
---

# Taxonomy Bulletproofing Audit: Bullion, Numismatics & Grading

## What We're Confirming

Audit of the entire taxonomy system to verify it handles all world bullion (including the most complex case: Engelhard vintage bars with 65+ varieties), remains flexible for numismatics, and properly separates the grading dimension from coin identity.

## Audit Findings

### 1. ID Format: No Structural Changes Needed

The `{COUNTRY}-{SERIES}-{YEAR}-{MINT}[-SUFFIX]` format handles every product type tested:

| Product Type | Example ID | Mechanism |
|-------------|-----------|-----------|
| Government mint coin | `US-AGEO-XXXX-X` | Standard 4-part |
| Fractional weight | `US-AGEO-XXXX-X-14oz` | Weight suffix |
| Generic bar/round | `XX-GSB1-XXXX-X` | XX country code |
| Branded bar | `CA-RCMB-XXXX-P-10oz` | Own series + suffix |
| Vintage collectible bar | `US-EN32-XXXX-X` | Numbered series codes |
| Art/commemorative bar | `US-EN56-XXXX-X` | Same pattern |
| Junk silver | `US-JS90-XXXX-X` | Single entry per FV lot |
| World bullion (50+ products) | `CN-PAND-XXXX-X` | Standard pattern |

**Conclusion**: Format is bulletproof. No changes needed.

### 2. Weight Suffix Convention: Already Standardized

Per issue #137, all bullion uses one convention:
- No suffix = 1oz (the base unit)
- Suffix for other sizes: `12oz`, `14oz`, `110oz`, `120oz`, `2oz`, `5oz`, `10oz`, `100oz`, `1kg`, `1g`
- `variety_suffixes` JSON field on series_registry documents valid sizes per series

### 3. Engelhard Data Quality Issues

Engelhard is the hardest stress test — 74 entries covering 65+ die varieties across multiple countries. The ID format handles it, but data quality has issues:

| Issue | Details | Fix |
|-------|---------|-----|
| **type='coin' in registry** | All 12 Engelhard series_registry entries have `type='coin'` | Update to `type='bullion'` |
| **Series code mismatch** | Registry: `ENG/ENG1-ENG10/EN10`. Coins table: `EN01-EN72` | Reconcile — coins table codes are canonical |
| **Country code wrong** | Canadian Engelhard bars (EN02-EN11) tagged as `US` | Should be `CA` for Canadian-origin bars |
| **Denomination** | All use `"Engelhard Bullion"` as denomination | Should be `"No Face Value"` consistent with other bars |

### 4. Grading Dimension: Properly Separated

Architecture is correct — grade is NOT part of coin_id:

```
coins table (identity)  ←→  inventory table (grade + condition)
     coin_id                    coin_id + grade_id + grading_service
```

This means the same `US-MORG-1881-S` can be MS-65 PCGS in one collection and VF-30 NGC in another.

### 5. Approved Grading Services

**Approved trio for comp price tracking:**
- **PCGS** (Professional Coin Grading Service) — industry standard
- **NGC** (Numismatic Guaranty Company) — industry standard
- **CACG** (Certified Acceptance Corporation Grading) — NEW, must be added

**Excluded (not comparable pricing):**
- ANACS — older service, different price tier
- ICG — different price tier

**CAC vs CACG — two different things, same company:**
- **CAC (stickers)**: Verification service that applies green/gold stickers to coins already graded by PCGS or NGC. NOT a grading service. A CAC sticker means "this coin is solid/premium for its grade." The coin stays in its PCGS/NGC slab.
- **CACG (slabs)**: A full independent grading service with its own slabs/holders. Coins are submitted raw, CACG grades them, and returns them in a CACG holder — just like PCGS and NGC do. CACG is the grading arm of the same company (founded by John Albanese, launched 2023).

**In our system:**
- `grading_service: "PCGS"` — coin in PCGS slab
- `grading_service: "NGC"` — coin in NGC slab
- `grading_service: "CACG"` — coin in CACG slab (NEW)
- `grading_service: "raw"` — ungraded coin
- CAC sticker status could be tracked as a modifier/flag on PCGS/NGC graded coins (separate concern, not a grading_service value)

## Key Decisions

- **No ID format changes**: Current format handles all tested scenarios
- **Grading trio**: PCGS, NGC, CACG are the approved services for comp pricing
- **ANACS/ICG excluded**: Not "bad" services, but their graded coins don't have comparable market data for our price comparison use case
- **Engelhard cleanup needed**: Data quality fixes only, no structural changes
- **CAC stickers vs CACG slabs**: CAC stickers (green/gold on PCGS/NGC coins) are a verification modifier, NOT a grading service. CACG slabs are a full grading service with own holders — treated same as PCGS/NGC in our system.

## Action Items

- [x] Add CACG to `data/references/grading_services.json` with `industry_standard: true`
- [x] Update ANACS/ICG `reason_excluded` to reference the approved trio
- [x] Fix Engelhard series_registry: type='coin' → 'bullion'
- [x] Clean up Engelhard denomination: "Engelhard Bullion" → "No Face Value"
- [ ] Fix Canadian Engelhard country codes if warranted (follow-up scope)
- [x] Reconcile Engelhard series_registry codes with coins table codes (removed 10 stale entries)

## Next Steps

→ `/workflows:plan` or `/workflows:work` for implementation
