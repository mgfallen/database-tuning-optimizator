BEGIN;
INSERT INTO my_table (column1, column2) VALUES ('value1', 'value2');
UPDATE my_table SET column1 = 'updatedValue1' WHERE column1 = 'value1';
SELECT * FROM my_table WHERE column1 = 'updatedValue1’ JOIN ON my_table.id = another_table.id;
COMMIT;

