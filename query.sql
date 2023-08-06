-- select the query you want to run
--CTRL SHIFT P
-- select "SQLite Run Query"
-- select the database (this will be shown ONLY for the first time)

SELECT name from regionInfo
WHERE doctor_visit < date('now', '+7 days') ;

SELECT name, doctor_visit FROM regionInfo
WHERE name = 'Walani';

SELECT ngo_visit FROM regionInfo
WHERE name = 'Walani';

drop table periodLog
