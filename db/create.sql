--DROP TABLE IF EXISTS public.brand CASCADE;
--CREATE TABLE IF NOT EXISTS public."brand"
--(
--    brand_id SERIAL PRIMARY KEY,
--    brand_name text NOT NULL UNIQUE
--);
--
--INSERT INTO public.brand(brand_name) VALUES ('Alfa Romeo') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('Audi') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('BMW') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('Chevrolet') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('Citroën') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('Dacia') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('Dodge') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('Dongfeng') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('DS Automobiles') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('Fiat') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('Ford') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('Honda') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('Hyundai') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('Jaguar') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('Jeep') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('Kia') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('Lada') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('Lancia') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('Land Rover') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('Mazda') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('Mercedes-Benz') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('Mini') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('Mitsubishi') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('Nissan') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('Opel') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('Peugeot') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('Renault') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('Rover') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('Seat') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('Škoda') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('Smart') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('SsangYong') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('Subaru') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('Suzuki') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('Toyota') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('Volkswagen') ON CONFLICT DO NOTHING;
--INSERT INTO public.brand(brand_name) VALUES ('Volvo') ON CONFLICT DO NOTHING;
--
--
--DROP TABLE IF EXISTS public.body_type CASCADE;
--CREATE TABLE IF NOT EXISTS public."body_type"
--(
--    body_type_id SERIAL PRIMARY KEY,
--    body_type_name text NOT NULL UNIQUE
--);
--
--INSERT INTO public.body_type(body_type_name) VALUES ('kombi') ON CONFLICT DO NOTHING;
--INSERT INTO public.body_type(body_type_name) VALUES ('hatchback') ON CONFLICT DO NOTHING;
--INSERT INTO public.body_type(body_type_name) VALUES ('sedan') ON CONFLICT DO NOTHING;
--INSERT INTO public.body_type(body_type_name) VALUES ('liftback') ON CONFLICT DO NOTHING;
--INSERT INTO public.body_type(body_type_name) VALUES ('MPV') ON CONFLICT DO NOTHING;
--INSERT INTO public.body_type(body_type_name) VALUES ('SUV') ON CONFLICT DO NOTHING;
--INSERT INTO public.body_type(body_type_name) VALUES ('chladící-mrazící') ON CONFLICT DO NOTHING;
--INSERT INTO public.body_type(body_type_name) VALUES ('kabriolet') ON CONFLICT DO NOTHING;
--INSERT INTO public.body_type(body_type_name) VALUES ('kupé') ON CONFLICT DO NOTHING;
--INSERT INTO public.body_type(body_type_name) VALUES ('minibus') ON CONFLICT DO NOTHING;
--INSERT INTO public.body_type(body_type_name) VALUES ('sklápěč') ON CONFLICT DO NOTHING;
--INSERT INTO public.body_type(body_type_name) VALUES ('pick up') ON CONFLICT DO NOTHING;
--INSERT INTO public.body_type(body_type_name) VALUES ('skříň') ON CONFLICT DO NOTHING;
--INSERT INTO public.body_type(body_type_name) VALUES ('užitkové vozidlo') ON CONFLICT DO NOTHING;
--INSERT INTO public.body_type(body_type_name) VALUES ('valník') ON CONFLICT DO NOTHING;
--INSERT INTO public.body_type(body_type_name) VALUES ('VAN') ON CONFLICT DO NOTHING;


DROP TABLE IF EXISTS public.car CASCADE;
CREATE TABLE IF NOT EXISTS public."car"
(
    car_id SERIAL PRIMARY KEY,
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
    datetime_captured timestamp NOT NULL
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

    CONSTRAINT fk_car
        FOREIGN KEY(car_id)
            REFERENCES car(car_id)
);