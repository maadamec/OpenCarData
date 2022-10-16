DROP TABLE IF EXISTS public.car CASCADE;
CREATE TABLE IF NOT EXISTS public."car"
(
    car_id SERIAL PRIMARY KEY,
    url text,
    image text,
    esa_id text NOT NULL UNIQUE,
    brand text NOT NULL,
    full_name text NOT NULL,
    engine text NOT NULL,
    equipment_class text NOT NULL,
    year integer NOT NULL,
    gear text NOT NULL,
    power text NOT NULL,
    fuel text NOT NULL,
    body_type text NOT NULL,
    mileage integer NOT NULL,
    tags text[],
    datetime_captured timestamp NOT NULL,
    job_id integer,


    CONSTRAINT fk_job
        FOREIGN KEY(job_id)
            REFERENCES job(job_id)
);

DROP TABLE IF EXISTS public.car_variable CASCADE;
CREATE TABLE IF NOT EXISTS public."car_variable"
(
    car_variable_id SERIAL PRIMARY KEY,
    car_id integer,
    lowcost boolean NOT NULL,
    premium boolean NOT NULL,
    monthly_price integer NOT NULL,
    special_price integer NOT NULL,
    condition numeric,
    price integer,
    discount integer,
    datetime_captured timestamp NOT NULL,
    job_id integer,

    CONSTRAINT fk_car
        FOREIGN KEY(car_id)
            REFERENCES car(car_id),

    CONSTRAINT fk_job
        FOREIGN KEY(job_id)
            REFERENCES job(job_id)
);

DROP TABLE IF EXISTS public.job CASCADE;
CREATE TABLE IF NOT EXISTS public.job
(
    job_id SERIAL PRIMARY KEY,
    job_name text NOT NULL,
    datetime_start timestamp NOT NULL,
    datetime_end timestamp,
    detail text
);