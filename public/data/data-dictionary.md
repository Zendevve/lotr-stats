# Data dictionary

- **persons**: person_id (stable key), canonical_name, slug, house_id, sex, birth_age, birth_year, death_age, death_year. Missing life dates are null. is_ruler separates 125 rulers from 28 connecting relatives; review_status, life_source_id and life_note record curation. reported_lifespan overrides arithmetic for Elros (500) and Aragorn (210). last_known_age/year preserve unresolved fates.
- **reigns**: reign_id (unique office tenure), person_id, office_id, start_age/start_year, end_age/end_year, status, note, succession_type, source_id.
- **realms**: realm_id, name, color. Analytical institutions are listed separately, including kings and stewards of Gondor.
- **offices**: office_id, realm_id, name, house_id. Person house and office house need not be identical.
- **relationships**: source_person_id is the parent or ancestor; target_person_id is the child or descendant. relationship_type distinguishes parent from ancestor; generations is 1 for parents, 2/3 where known, otherwise null. source_id cites each link. These are curated, not generated from succession.
- **sources**: source_id, title, url, reference, accessed, status.
- **field_sources**: entity_type, entity_id, field_name, source_id. Reign dates and entered life dates have explicit mappings. Names use the tenure's source. Source coverage is not a confidence score.
- **aliases**: person_id, name, source_id.
- **events**: event_id, name, age, year, realm_id, source_id. Selective list; inclusive year-boundary associations may attach to both adjacent tenures.
- **mart_ruler_reigns**: joined person/office/tenure plus start_sort/end_sort, reign_years, lifespan, accession_age, eligible, event_count, event_density, aliases.
- **mart_realm_summary**: n (eligible tenures), mean, median, minimum, maximum, variance (population), lifespan_known (eligible tenures with lifespan).
- **mart_succession**: reign_id, realm_name, succession_type; all transitions classified; foundations, parent-child, sibling, nephew/niece, collateral, usurpation and restoration are distinct.

Ordinal = year + {SA:0, TA:3441, FA:6462}. Duration = end minus start. The Fourth Age mapping is a documented year-label convention. No First Age date is normalized.

Eligibility = status exactly 'recorded'. Excluded: titular, usurper, uncertain, co-ruler, overlord. These flags are analytical inclusion choices, not judgments of legitimacy beyond the referenced records.
