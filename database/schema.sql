-- DuckDB analytical schema. Run from the project root.
-- The application has no hosted D1 database.

CREATE TABLE "aliases" (
  "person_id" VARCHAR,
  "name" VARCHAR,
  "source_id" VARCHAR
);

CREATE TABLE "events" (
  "event_id" VARCHAR,
  "name" VARCHAR,
  "age" VARCHAR,
  "year" BIGINT,
  "realm_id" VARCHAR,
  "source_id" VARCHAR
);

CREATE TABLE "field_sources" (
  "entity_type" VARCHAR,
  "entity_id" VARCHAR,
  "field_name" VARCHAR,
  "source_id" VARCHAR
);

CREATE TABLE "houses" (
  "house_id" VARCHAR,
  "name" VARCHAR
);

CREATE TABLE "mart_realm_summary" (
  "realm_id" VARCHAR,
  "realm_name" VARCHAR,
  "n" BIGINT,
  "mean" DOUBLE,
  "median" DOUBLE,
  "minimum" BIGINT,
  "maximum" BIGINT,
  "variance" DOUBLE,
  "lifespan_known" BIGINT
);

CREATE TABLE "mart_ruler_reigns" (
  "person_id" VARCHAR,
  "canonical_name" VARCHAR,
  "slug" VARCHAR,
  "house_id" VARCHAR,
  "birth_age" VARCHAR,
  "birth_year" BIGINT,
  "death_age" VARCHAR,
  "death_year" BIGINT,
  "sex" VARCHAR,
  "is_ruler" BOOLEAN,
  "review_status" VARCHAR,
  "reported_lifespan" BIGINT,
  "life_note" VARCHAR,
  "last_known_age" VARCHAR,
  "last_known_year" BIGINT,
  "life_source_id" VARCHAR,
  "reign_id" VARCHAR,
  "office_id" VARCHAR,
  "start_age" VARCHAR,
  "start_year" BIGINT,
  "end_age" VARCHAR,
  "end_year" BIGINT,
  "status" VARCHAR,
  "note" VARCHAR,
  "succession_type" VARCHAR,
  "source_id" VARCHAR,
  "ruler_name" VARCHAR,
  "realm_name" VARCHAR,
  "color" VARCHAR,
  "office_name" VARCHAR,
  "start_sort" BIGINT,
  "end_sort" BIGINT,
  "reign_years" BIGINT,
  "lifespan" BIGINT,
  "accession_age" BIGINT,
  "eligible" BOOLEAN,
  "event_count" BIGINT,
  "event_density" DOUBLE,
  "aliases" VARCHAR
);

CREATE TABLE "mart_succession" (
  "reign_id" VARCHAR,
  "realm_name" VARCHAR,
  "succession_type" VARCHAR
);

CREATE TABLE "offices" (
  "office_id" VARCHAR,
  "realm_id" VARCHAR,
  "name" VARCHAR,
  "house_id" VARCHAR
);

CREATE TABLE "persons" (
  "person_id" VARCHAR,
  "canonical_name" VARCHAR,
  "slug" VARCHAR,
  "house_id" VARCHAR,
  "birth_age" VARCHAR,
  "birth_year" BIGINT,
  "death_age" VARCHAR,
  "death_year" BIGINT,
  "sex" VARCHAR,
  "is_ruler" BOOLEAN,
  "review_status" VARCHAR,
  "reported_lifespan" BIGINT,
  "life_note" VARCHAR,
  "last_known_age" VARCHAR,
  "last_known_year" BIGINT,
  "life_source_id" VARCHAR
);

CREATE TABLE "realms" (
  "realm_id" VARCHAR,
  "name" VARCHAR,
  "color" VARCHAR
);

CREATE TABLE "reigns" (
  "reign_id" VARCHAR,
  "person_id" VARCHAR,
  "office_id" VARCHAR,
  "start_age" VARCHAR,
  "start_year" BIGINT,
  "end_age" VARCHAR,
  "end_year" BIGINT,
  "status" VARCHAR,
  "note" VARCHAR,
  "succession_type" VARCHAR,
  "source_id" VARCHAR
);

CREATE TABLE "relationships" (
  "source_person_id" VARCHAR,
  "target_person_id" VARCHAR,
  "relationship_type" VARCHAR,
  "source_id" VARCHAR,
  "generations" BIGINT
);

CREATE TABLE "sources" (
  "source_id" VARCHAR,
  "title" VARCHAR,
  "url" VARCHAR,
  "reference" VARCHAR,
  "accessed" VARCHAR,
  "status" VARCHAR
);

CREATE VIEW ruler_reigns AS SELECT * FROM mart_ruler_reigns;
CREATE VIEW rulers AS SELECT * FROM persons WHERE is_ruler = true;
