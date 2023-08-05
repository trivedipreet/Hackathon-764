-- select the query you want to run
--CTRL SHIFT P
-- select "SQLite Run Query"
-- select the database (this will be shown ONLY for the first time)

ALTER TABLE regionInfo ADD doctor_count INT;
ALTER TABLE regionInfo ADD doctor_visit DATE;

ALTER TABLE regionInfo ADD ngo_count INT;
ALTER TABLE regionInfo ADD ngo_visit DATE;

