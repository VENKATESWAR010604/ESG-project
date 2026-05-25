# SOURCES.md

## Overview

This document explains the real-world source formats considered for each source, what was learned, what the sample data looks like, and what could break in a real deployment.

---

## 1. SAP Fuel and Procurement Data

### Real-world format researched

SAP data can be exported through:

- flat file reports
- IDoc
- OData services
- BAPI
- custom ABAP reports

For this project, I chose a flat file export.

### What I learned

SAP exports are often not clean. They may contain:

- localized column headers
- plant codes instead of readable facility names
- material codes instead of normalized fuel names
- inconsistent date formats
- inconsistent units
- missing or invalid quantities

### Sample data used

The sample SAP file uses German-style headers:

- `Werk` = plant
- `Material` = material
- `Menge` = quantity
- `Einheit` = unit
- `Buchungsdatum` = posting date
- `Lieferant` = supplier
- `Kostenstelle` = cost center

Example materials:

- DIESEL
- PETROL
- LPG
- LUBRICANT

Example units:

- L
- KG

### Why this sample data

This sample data tests realistic SAP issues:

- German headers
- mixed date formats
- invalid quantities such as text values
- unknown plant codes
- unusually high quantities

### What would break in real deployment

- new German or custom column names
- plant codes missing from lookup table
- material codes not matching expected names
- units requiring conversion
- duplicate SAP exports
- large file sizes
- different encodings
- direct SAP API authentication

---

## 2. Utility Electricity Data

### Real-world format researched

Utility electricity data can arrive as:

- CSV billing exports
- PDF bills
- smart meter interval data
- provider APIs

For this project, I chose a CSV billing export.

### What I learned

Utility data often contains:

- account numbers
- meter IDs
- billing periods
- electricity usage
- tariff or rate plan
- missing readings
- estimated readings

### Sample data used

The sample utility file contains fields like:

- account
- meter
- billing period
- usage
- tariff

The normalized activity is:

- source: UTILITY
- scope: SCOPE_2
- activity type: electricity
- unit: kWh

### Why this sample data

Electricity is the most common Scope 2 activity. CSV is simple to validate and suitable for the assignment.

### What would break in real deployment

- PDF-only bills
- multiple meters for one site
- estimated vs actual usage
- overlapping billing periods
- negative adjustments
- different units such as MWh
- timezone and billing cycle differences
- provider-specific CSV formats

---

## 3. Travel Data

### Real-world format researched

Travel data can come from:

- travel booking systems
- expense management systems
- HR travel records
- travel agency APIs

For this project, I chose JSON records.

### What I learned

Travel records can include:

- flights
- hotels
- taxis
- trains
- rental cars
- origin and destination
- distance
- number of nights
- traveler or department

### Sample data used

The sample travel JSON contains records for:

- flight
- hotel
- ground transport

The normalized activity is:

- source: TRAVEL
- scope: SCOPE_3
- activity type: flight, hotel, or ground_transport
- units: km or nights

### Why this sample data

JSON works well for travel because travel records can have different structures depending on type.

### What would break in real deployment

- missing distance
- airport code mapping
- multi-leg flights
- cancelled trips
- duplicate expense records
- currency conversion
- employee privacy requirements
- travel class affecting emissions
- hotel country-specific emission factors