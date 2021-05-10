DROP TABLE IF EXISTS activations;
CREATE TABLE activations(device TEXT, dataset TEXT, lang TEXT, tld TEXT, trial INTEGER, ipaddress TEXT, word TEXT, duration REAL);

COPY activations FROM '/Users/MattWong/Desktop/Speaker-Misactivations/results/activations.csv' DELIMITER ',' CSV HEADER;

-- psql MattWong -h 127.0.0.1 -d activations -f load.sql