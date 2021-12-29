Створення тригерної функції
CREATE OR REPLACE FUNCTION trigger_func() RETURNS TRIGGER as $trigger$
BEGIN
	IF old."price" >= 500 THEN
INSERT INTO "lab3_trigger_for_check"  VALUES (old.id, old.name, old.price, old.rest);
	END IF;
	IF (TG_OP = 'DELETE') THEN
        RETURN OLD;
    	ELSIF (TG_OP = 'UPDATE') THEN
        RETURN NEW;
    	END IF;
END; 
$trigger$ LANGUAGE plpgsql;


Створення тригера
CREATE TRIGGER "trigger1"
BEFORE DELETE OR UPDATE ON "lab3_trigger"
FOR EACH ROW
EXECUTE procedure trigger_func();


Запити
DELETE FROM "lab3_trigger" WHERE name='gold';
DELETE FROM "lab3_trigger" WHERE name='water';
UPDATE "lab3_trigger" SET  name='caviar', price=950, rest=249 WHERE id=4;
UPDATE "lab3_trigger" SET  name='apple', price=4, rest=200 WHERE id=1;