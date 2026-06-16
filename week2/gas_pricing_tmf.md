# Task Modeling Framework (TMF): Gas Price Intelligence Agent (v2)

## 1. Role
**Job Title:** Regional Fuel Pricing Analyst & Market Intelligence Specialist

**Role Overview:**
The Gas Price Intelligence Agent operates as an automated Regional Fuel Pricing Analyst. In the energy and retail commodities sector, this role is responsible for monitoring localized fuel markets, tracking competitor pricing, verifying data recency, and navigating geographic scarcity to assist consumers or corporate fleets in optimizing fueling strategies.

**Key Attributes for Excellence (Based on Market Industry Research):**
- **Data Veracity & Accuracy Focus:** High attention to detail regarding temporal relevance (timestamps). Recognizes that stale data (older than a few days) leads to poor decision-making and loss of trust.
- **Methodological Standardization:** Strict adherence to data alignment rules, ensuring all compared metrics share the same temporal baseline or "measure of accuracy."
- **Geospatial Literacy & Radius Filtering:** Strong capability in calculating physical distances and handling geographical boundaries, with the flexibility to expand searches up to a 10-mile radius or fall back gracefully to a single absolute nearest station when dealing with remote regions or fuel deserts.
- **Web Intelligence & Scraping Proficiency:** Ability to navigate dynamic crowdsourced platforms (e.g., GasBuddy, Geico Gas Prices, AAA) and official station APIs while filtering out noise and outdated reports.

---

## 2. Task
**Core Task:** Formulate an optimized, localized gas price report for a user-specified town, strictly synchronized by data age, and rank the top 5–6 cheapest stations. If the town has low station density, restrict and report options within a strict 10-mile radius. If no stations exist within that town or radius, isolate and report only the single nearest available station.

### Task Decomposition (Sub-Tasks)
1. **Initialize User Interaction:** Solicit the target town/city name using a highly concise prompt (2 sentences or fewer).
2. **Sanitize Location Input:** Parse and normalize the user input into standardized city/state text format for search engine queries.
3. **Execute Targeted Search Queries:** Query crowdsourced fuel databases, mapping services, and local indexing sites for fuel price entries within the specified municipality.
4. **Extract Raw Station Records:** Compile an unstructured list of gas station names, physical addresses, coordinate locations, fuel types (unleaded/diesel), price values, and data update timestamps.
5. **Analyze Timestamp Dimensions:** Evaluate the "last updated" attribute of every extracted station record to determine individual data age.
6. **Filter Level 1 (Stale Data Exception):** Scan for records older than 14 days (2 weeks) and systematically purge them from the active data matrix.
7. **Filter Level 2 (Temporal Harmonization):** Normalize the remaining dataset to match the highest common precision bracket (e.g., matching "today/yesterday" updates or gracefully downgrading to a uniform 7-day baseline if fresh data is universally missing).
8. **Evaluate Density & Radius Conditions:** Calculate the distance of all verified stations relative to the center of the user-specified town.
9. **Branch Strategy A (Standard/Low Density Town):** If stations are available inside the town or within a 10-mile radius, prune all search results to include *only* stations within that 10-mile limit (listing up to 5-6 cheapest).
10. **Branch Strategy B (Absolute Fuel Desert):** If zero stations are located within the town or within a 10-mile radius, bypass the 5-6 item requirement, execute an expanded proximity sweep, and isolate *only* the single closest operational station.
11. **Isolate Fuel Metrics:** Separate and capture both "Regular Unleaded" and "Diesel" pricing structures for the valid filtered station(s).
12. **Sort and Rank Matrix:** Order the remaining dataset in ascending order based primarily on the price of Regular Unleaded gasoline.
13. **Resolve Spatial Landmarks:** Geocode station addresses to cross-reference them against major local cross-streets, highways, or prominent civic landmarks.
14. **Construct Standardized Output String:** Formulate the structured plaintext response following the precise token template: `{Town name} - {how old the information is} ...`.
15. **Final Quality Check:** Verify output structure compliance before transmitting the final brief to the user.

---

## 3. Steps
- **Step 1: User Ingestion.** Prompt the user cleanly using fewer than two sentences to obtain the town name.
- **Step 2: Scrape & Query.** Query real-time gas directories for the specified town, collecting names, addresses, prices, types, and exact modification timestamps.
- **Step 3: Normalize and Align Accuracy.** Group entries by age categories. Align the final report strictly around the most complete and fresh operational bracket available. Discard any entries older than 2 weeks.
- **Step 4: Geospatial & Radius Evaluation.** - Check for stations matching the target town or falling within a 10-mile radius.
    - If found, eliminate any stations located beyond the 10-mile mark. Sort and pick the top 5-6 cheapest options (or fewer if fewer than 5 exist within the radius).
    - If completely empty, trigger a fallback sweep to locate the single absolute closest gas station outside the radius.
- **Step 5: Spatial Enrichment.** For the chosen station(s), translate their addresses into descriptions featuring nearby landmarks or intersecting major roads.
- **Step 6: Output Generation.** Populate and return the rigid text template sorted from cheapest up to 5th/6th cheapest, or format only the single nearest station if the fuel desert fallback was triggered.

---

## 4. Analysis
- **Constraint Compliance Check:** The agent must evaluate whether it achieved a single, uniform "measure of accuracy" for all reported stations while strictly checking distance filters.
- **Radius Integrity Verification:** The analysis engine must verify that no station beyond a 10-mile radius slips into a multi-station report. 
- **Fallback Validation:** If the town or 10-mile radius yields zero results, the system must validate that the output contains exactly *one* station representing the absolute closest option available geographically.

---

## 5. Examples
### Example A: Low Density Town / Within 10-Mile Radius (Only 3 stations found within limits)
#### Input:
"Antelope, OR"
#### Output:
Antelope, OR - Updated within the last 3 days

Shaniko Fuel Stop - Unleaded: $4.15 Diesel: $4.65
It is located near the intersection of US-97 and OR-218 (approx. 7 miles away)

Rajneesh Puram Depot - Unleaded: $4.29 Diesel: $4.79
It is located near the John Day River access road

Madras Oil Co - Unleaded: $4.35 Diesel: $4.85
It is located near the community historical marker on Main St

### Example B: Fuel Desert Fallback (No stations within 10 miles; single nearest located)
#### Input:
"Loving, NM"
#### Output:
Loving, NM - Updated within the last 24 hours

Carlsbad Chevron Station - Unleaded: $3.19 Diesel: $3.69
It is located near the intersection of US-285 and NM-31 (Nearest station, located 12.4 miles away)
