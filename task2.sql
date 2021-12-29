GIN індекс
Створення таблиці
DROP TABLE IF EXISTS "lab3_gin";
CREATE TABLE "lab3_gin"("id" serial PRIMARY KEY, "doc" text, "doc_tsv" tsvector);
INSERT INTO "lab3_gin"("doc") SELECT chr((65 + round(random() * 25)) :: int) || chr((65 + round(random() * 25)) :: int)||chr((65 + round(random() * 25)) :: int) FROM generate_series(1, 1000000);
UPDATE "lab3_gin" set "doc_tsv" = to_tsvector("doc");

Створення індексу 
CREATE INDEX "gin_i" ON "lab3_gin" USING gin("doc_tsv");
Видалення індексу
DROP INDEX IF EXISTS "gin_i";

Запити
SELECT * FROM lab3_gin WHERE doc_tsv @@ to_tsquery('abc');
SELECT COUNT(*) FROM lab3_gin WHERE doc_tsv @@ to_tsquery('xyz');
SELECT COUNT(*) FROM lab3_gin WHERE doc_tsv @@ to_tsquery('qwe') GROUP BY "id" % 2;
SELECT * FROM lab3_gin WHERE doc_tsv @@ to_tsquery('qwe') ORDER BY RANDOM();


Hash індекс
Створення таблиці
DROP TABLE IF EXISTS "lab3_hash";
CREATE TABLE "lab3_hash"("id" serial PRIMARY KEY, "num" integer);
INSERT INTO "lab3_hash"("num") SELECT ((random() * 25) :: int) FROM generate_series(1, 1000000);

Створення індексу 
CREATE INDEX "hash_i" ON "lab3_hash" USING hash("id");
Видалення індексу
DROP INDEX IF EXISTS "hash_i";

Запити
SELECT * FROM lab3_hash WHERE num=25;
SELECT COUNT(*) FROM lab3_hash WHERE num<10;
SELECT COUNT(*) FROM lab3_hash WHERE num=10 GROUP BY "id" % 2;
SELECT * FROM lab3_hash WHERE num=15 ORDER BY RANDOM();