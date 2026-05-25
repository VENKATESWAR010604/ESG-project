# DECISIONS.md

## Overview

This document explains the main ambiguities in the assignment, the decisions made, why those decisions were chosen, and what I would ask the PM if possible.

---

## 1. SAP Source Format

### Ambiguity

SAP exports can come from IDoc, OData, BAPI, flat files, or custom reports. The assignment allowed choosing one subset of SAP reality.

### Decision

I chose to handle a flat file CSV/TSV export with German headers.

Sample headers:

- `Werk`
- `Material`
- `Menge`
- `Einheit`
- `Buchungsdatum`
- `Lieferant`
- `Kostenstelle`

### Why

Flat file exports are common in enterprise workflows and easier to simulate in a coding assignment. German headers represent a realistic SAP configuration issue.

### What I ignored

- IDoc parsing
- BAPI integration
- OData authentication
- SAP plant lookup from external master data
- Complex material master mapping

### PM question

Should SAP ingestion support only uploaded flat files first, or should it connect directly to SAP APIs later?

---

## 2. Utility Source Format

### Ambiguity

Utility data may arrive as PDF bills, CSV exports, meter data, or provider APIs.

### Decision

I chose to handle a CSV file containing account, meter, billing period, usage, and tariff information.

### Why

CSV utility exports are realistic for facilities teams and easier to validate programmatically.

### What I ignored

- PDF bill parsing
- OCR
- tariff cost calculations
- demand charges
- multiple meters per site with complex hierarchy

### PM question

Should utility bills be treated as monthly summary data or interval meter data?

---

## 3. Travel Source Format

### Ambiguity

Travel data can come from expense systems, booking tools, HR systems, or travel management APIs.

### Decision

I chose to handle JSON travel records for flights, hotels, and ground transport.

### Why

JSON is common for API-style travel exports and supports nested travel details better than CSV.

### What I ignored

- passenger-level allocation
- fare class
- airport code distance calculation
- hotel country-specific emission factors
- duplicate trip detection

### PM question

Should travel emissions be calculated from distance directly, or should the system calculate distance from origin/destination?

---

## 4. Scope Mapping

### Decision

- SAP fuel/procurement → Scope 1
- Utility electricity → Scope 2
- Travel → Scope 3

### Why

This follows common GHG Protocol categorization:

- direct fuel usage is Scope 1
- purchased electricity is Scope 2
- business travel is Scope 3

### PM question

Should procurement items always be Scope 1, or should some procurement categories be Scope 3 purchased goods?

---

## 5. Failed vs Suspicious Rows

### Decision

Invalid data becomes `FAILED`. Unusual but still parseable data becomes `SUSPICIOUS`.

### Why

This separates hard validation errors from rows that need human review.

Examples:

- non-numeric quantity → FAILED
- very high quantity → SUSPICIOUS

### PM question

What thresholds should define suspicious values for each customer and source?

---

## 6. Audit Logs

### Decision

Audit logs are created for approve and reject actions.

### Why

Reviewer decisions are the most important compliance actions.

### What I ignored

- audit logs for every ingestion row
- audit logs for every delete action
- user authentication identity in audit logs

### PM question

Should ingestion and deletion also create audit events in the MVP?

---

## 7. Delete Behavior

### Decision

Delete removes a row from the review table.

### Why

It keeps the demo simple.

### Better production decision

Use soft delete instead:

- status = DELETED
- deleted_at
- deleted_by

### PM question

Should reviewers be allowed to permanently delete rows, or only mark them as excluded?

---

## 8. Authentication

### Decision

Authentication was not implemented.

### Why

The assignment focused on ingestion, normalization, review, and audit trail.

### PM question

Should the first production version support admin/reviewer roles?

---

## 9. Emissions Calculation

### Decision

The app does not calculate final CO2e emissions.

### Why

Emission factors vary by region, year, fuel type, electricity grid, and methodology. I focused on data quality before calculation.

### PM question

Which emission factor source should be used: DEFRA, EPA, GHG Protocol, or customer-provided factors?

---

## 10. Deployment

### Decision

Frontend and backend are designed to be deployed separately.

### Why

This is common for React + Django projects.

Recommended:

- Backend: Render or Railway
- Frontend: Vercel or Netlify