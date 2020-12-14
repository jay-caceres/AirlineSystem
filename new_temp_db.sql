DROP TABLE IF EXISTS airport CASCADE;

DROP TABLE IF EXISTS boarding_passes CASCADE;

DROP TABLE IF EXISTS seats CASCADE;

DROP TABLE IF EXISTS aircraft CASCADE;

DROP TABLE IF EXISTS ticket CASCADE;

DROP TABLE IF EXISTS ticket_flights CASCADE;

DROP TABLE IF EXISTS bookings CASCADE;

DROP TABLE IF EXISTS flights CASCADE;

DROP TABLE IF EXISTS flight_leg CASCADE;

DROP TABLE IF EXISTS leg_actual CASCADE;

DROP TABLE IF EXISTS customer CASCADE;

DROP TABLE IF EXISTS payment CASCADE;

DROP TABLE IF EXISTS customer_entity CASCADE;



CREATE TABLE "aircraft"
(
 "aircraft_code" char(3) NOT NULL,
 "model"         char(25) NULL,
 "RANGE"         integer NULL,
 CONSTRAINT "PK_aircraft" PRIMARY KEY ( "aircraft_code" ),
 CONSTRAINT "flights_aircraft_code_fkey" FOREIGN KEY ( "aircraft_code" ) REFERENCES "aircraft" ( "aircraft_code" ),
 CONSTRAINT "seats_aircraft_code_fkey" FOREIGN KEY ( "aircraft_code" ) REFERENCES "aircraft" ( "aircraft_code" ) ON DELETE CASCADE
);

CREATE TABLE "airport"
(
 "airport_code" text NOT NULL,
 "airport_name" char(40) NULL,
 "city"         char(20) NULL,
 "coordinates"  point NULL,
 "timezone"     text NULL,
 CONSTRAINT "airport_code" PRIMARY KEY ( "airport_code" )
);

CREATE TABLE "flights"
(
 "flight_id"          integer NOT NULL,
 "airline_name"       text NOT NULL,
 "weekday_identifier" text NOT NULL,
 CONSTRAINT "PK_flights" PRIMARY KEY ( "flight_id" )
);

CREATE TABLE "flight_leg"
(
 "flight_id"           integer NOT NULL,
 "leg_no"              integer NOT NULL,
 "scheduled_departure" text NOT NULL,
 "scheduled_arrival"   text NOT NULL,
 "departure_airport"   text NOT NULL,
 "arrival_airport"     text NOT NULL,
 "STATUS"              character varying(50) NOT NULL,
 "seats_available"   integer NOT NULL,
 "seats_booked"      integer NOT NULL,
 CONSTRAINT "flight_id" PRIMARY KEY ( "flight_id", "leg_no" ),
 CONSTRAINT "FK_204" FOREIGN KEY ( "flight_id" ) REFERENCES "flights" ( "flight_id" ),
 CONSTRAINT "flights_arrival_airport_fkey" FOREIGN KEY ( "arrival_airport" ) REFERENCES "airport" ( "airport_code" ),
 CONSTRAINT "flights_departure_airport_fkey" FOREIGN KEY ( "departure_airport" ) REFERENCES "airport" ( "airport_code" ),
 CONSTRAINT "flights_check" CHECK ( (scheduled_arrival > scheduled_departure) ),
 CONSTRAINT "flights_status_check" CHECK ( (
            ("STATUS")::text = ANY (
                ARRAY [('On Time'::character varying)::text, ('Delayed'::character varying)::text, ('Departed'::character varying)::text, ('Arrived'::character varying)::text, ('Scheduled'::character varying)::text, ('Cancelled'::character varying)::text]
            )
        ) )
);

CREATE INDEX "fkIdx_204" ON "flight_leg"
(
 "flight_id"
);

CREATE TABLE "payment"
(
 "payment_id"     char(50) NOT NULL,
 "card_number"    text NOT NULL,
 "payment_amount" numeric(10,2) NOT NULL,
 CONSTRAINT "PK_payment" PRIMARY KEY ( "payment_id" )
);

CREATE TABLE "customer"
(
 "customer_email" char(50) NOT NULL,
 "customer_name"  text NULL,
 "customer_id"    integer NOT NULL,
 "customer_phone" char(15) NULL,
 "id_type"        text NULL,
 CONSTRAINT "PK_customer11" PRIMARY KEY ( "customer_email" )
);


CREATE TABLE "customer_entity"
(
 "customer_email" char(50) NOT NULL,
 "payment_id"     char(50) NOT NULL,
 CONSTRAINT "PK_customer_entity" PRIMARY KEY ( "customer_email","payment_id" ),
 CONSTRAINT "FK_130" FOREIGN KEY ( "payment_id" ) REFERENCES "payment" ( "payment_id" ),
 CONSTRAINT "FK_133" FOREIGN KEY ( "customer_email" ) REFERENCES "customer" ( "customer_email" )
);

CREATE INDEX "fkIdx_130" ON "customer_entity"
(
 "payment_id"
);

CREATE INDEX "fkIdx_133" ON "customer_entity"
(
 "customer_email"
);




CREATE TABLE "bookings"
(
 "book_ref"       character(6) NOT NULL,
 "customer_email" char(50) NOT NULL,
 "book_date"      timestamp NOT NULL,
 "passengers"     text NULL,
 CONSTRAINT "PK_bookings" PRIMARY KEY ( "book_ref" ),
 CONSTRAINT "FK_163" FOREIGN KEY ( "customer_email" ) REFERENCES "customer" ( "customer_email" )
);

CREATE INDEX "fkIdx_1631" ON "bookings"
(
 "customer_email"
);


CREATE TABLE "ticket"
(
 "ticket_no"      char(13) NOT NULL,
 "book_ref"       character(6) NOT NULL,
 "passenger_id"   varchar(20) NOT NULL,
 "passenger_name" text NOT NULL,
 "email"          char(50) NULL,
 "phone"          char(15) NULL,
 CONSTRAINT "ticket_no" PRIMARY KEY ( "ticket_no" ),
 CONSTRAINT "tickets_book_ref_fkey" FOREIGN KEY ( "book_ref" ) REFERENCES "bookings" ( "book_ref" ) ON DELETE CASCADE
);

CREATE TABLE "ticket_flights"
(
 "ticket_no"       char(13) NOT NULL,
 "flight_id"       integer NOT NULL,
 "leg_no"          integer NOT NULL,
 "fare_conditions" text NOT NULL,
 "amount"          numeric(10, 2) NOT NULL,
 CONSTRAINT "ticket_no1" PRIMARY KEY ( "ticket_no", "flight_id", "leg_no" ),
 CONSTRAINT "ticket_flights_flight_id_fkey" FOREIGN KEY ( "flight_id", "leg_no" ) REFERENCES "flight_leg" ( "flight_id", "leg_no" ),
 CONSTRAINT "ticket_flights_ticket_no_fkey" FOREIGN KEY ( "ticket_no" ) REFERENCES "ticket" ( "ticket_no" ) ON DELETE CASCADE,
 CONSTRAINT "ticket_flights_amount_check" CHECK ( (amount >= (0)::numeric) ),
 CONSTRAINT "ticket_flights_fare_conditions_check" CHECK ( (
            (fare_conditions)::text = ANY (
                ARRAY [('Economy'::character varying)::text, ('Comfort'::character varying)::text, ('Business'::character varying)::text]
            )
        ) )
);



CREATE TABLE "boarding_passes"
(
 "ticket_no"     char(13) NOT NULL,
 "flight_id"     integer NOT NULL,
 "leg_no"        integer NOT NULL,
 "boarding_no"   integer NOT NULL,
 "seat_no"       character(3) NOT NULL,
 "boarding_time" timestamp NOT NULL,
 "gate_number"   char(5) NOT NULL,
 "checked_bags"  boolean NOT NULL,
 "confirmed"     text NULL,
 CONSTRAINT "PK_boarding_passes" PRIMARY KEY ( "ticket_no", "flight_id", "leg_no" ),
 CONSTRAINT "boarding_passes_ticket_no_fkey" FOREIGN KEY ( "ticket_no", "flight_id", "leg_no" ) REFERENCES "ticket_flights" ( "ticket_no", "flight_id", "leg_no" ) ON DELETE CASCADE
);






CREATE TABLE "leg_actual"
(
 "flight_id"         integer NOT NULL,
 "leg_no"            integer NOT NULL,
 "actual_dept"       timestamp NOT NULL,
 "actual_arrival"    timestamp NOT NULL,
 "departure_airport" text NOT NULL,
 "arrival_airport"   text NOT NULL,
 "aircraft_code"     char(3) NOT NULL,
 CONSTRAINT "PK_leg_actual" PRIMARY KEY ( "flight_id", "leg_no" ),
 CONSTRAINT "FK_163" FOREIGN KEY ( "departure_airport" ) REFERENCES "airport" ( "airport_code" ),
 CONSTRAINT "FK_166" FOREIGN KEY ( "arrival_airport" ) REFERENCES "airport" ( "airport_code" ),
 CONSTRAINT "FK_169" FOREIGN KEY ( "aircraft_code" ) REFERENCES "aircraft" ( "aircraft_code" ),
 CONSTRAINT "FK_199" FOREIGN KEY ( "flight_id", "leg_no" ) REFERENCES "flight_leg" ( "flight_id", "leg_no" )
);

CREATE INDEX "fkIdx_163" ON "leg_actual"
(
 "departure_airport"
);

CREATE INDEX "fkIdx_166" ON "leg_actual"
(
 "arrival_airport"
);

CREATE INDEX "fkIdx_169" ON "leg_actual"
(
 "aircraft_code"
);

CREATE INDEX "fkIdx_199" ON "leg_actual"
(
 "leg_no",
 "flight_id"
);




CREATE TABLE "seats"
(
 "aircraft_code"   char(3) NOT NULL,
 "seat_no"         character NOT NULL,
 "fare_conditions" character NOT NULL,
 CONSTRAINT "aircraft_code" PRIMARY KEY ( "aircraft_code", "seat_no" ),
 CONSTRAINT "seats_aircraft_code_fkey" FOREIGN KEY ( "aircraft_code" ) REFERENCES "aircraft" ( "aircraft_code" ) ON DELETE CASCADE,
 CONSTRAINT "seats_fare_conditions_check" CHECK ( (
            (fare_conditions)::text = ANY (
                ARRAY [('Economy'::character varying)::text, ('Comfort'::character varying)::text, ('Business'::character varying)::text]
            )
        ) )
);

INSERT INTO airport
VALUES (
        'HOU',
        'George Bush Airport',
        'Houston',
        NULL,
        'CT'
    );

INSERT INTO airport
VALUES (
        'JFK',
        'John F Kennedy Airport',
        'New York',
        NULL,
        'ET'
    );

INSERT INTO airport
VALUES (
        'LAX',
        'Los Angeles Airport',
        'Los Angeles',
        NULL,
        'PT'
    );

INSERT INTO airport
VALUES ('ORD', 'O Hare Airport', 'Chicago', NULL, 'CT');

INSERT INTO airport
VALUES ('MIA', 'Miami Airport', 'Miami', NULL, 'ET');

/*aircraft*/
INSERT INTO aircraft
VALUES ('773', 'Boeing 777-300', 11100);

INSERT INTO aircraft
VALUES ('763', 'Boeing 767-300', 7900);

INSERT INTO aircraft
VALUES ('SU9', 'Boeing 777-300', 5700);

INSERT INTO aircraft
VALUES ('320', 'Boeing 777-300', 6400);

INSERT INTO aircraft
VALUES ('321', 'Boeing 777-300', 6100);

INSERT INTO flights VALUES(11001,'Spirit','Monday');
INSERT INTO flights VALUES(11002,'American Airlines', 'Monday');
INSERT INTO flights VALUES(21001,'Spirit', 'Tuesday');
INSERT INTO flights VALUES(21002,'American Airlines', 'Tuesday');
INSERT INTO flights VALUES(31001,'Spirit', 'Wednesday');
INSERT INTO flights VALUES(31002,'American Airlines', 'Wednesday');
INSERT INTO flights VALUES(41001,'Spirit', 'Thursday');
INSERT INTO flights VALUES(41002,'American Airlines', 'Thursday');
INSERT INTO flights VALUES(51001,'Spirit', 'Friday');
INSERT INTO flights VALUES(51002,'American Airlines', 'Friday');

INSERT INTO flights VALUES(11101,'Spirit','Monday');
INSERT INTO flights VALUES(11102,'American Airlines', 'Monday');
INSERT INTO flights VALUES(21101,'Spirit', 'Tuesday');
INSERT INTO flights VALUES(21102,'American Airlines', 'Tuesday');
INSERT INTO flights VALUES(31101,'Spirit', 'Wednesday');
INSERT INTO flights VALUES(31102,'American Airlines', 'Wednesday');
INSERT INTO flights VALUES(41101,'Spirit', 'Thursday');
INSERT INTO flights VALUES(41102,'American Airlines', 'Thursday');
INSERT INTO flights VALUES(51101,'Spirit', 'Friday');
INSERT INTO flights VALUES(51102,'American Airlines', 'Friday');

INSERT INTO FLIGHT_LEG VALUES(11001, 1, '2020-12-7 09:50:00', '2020-12-7 14:55:00', 'HOU', 'JFK', 'Scheduled', 50, 0);
INSERT INTO FLIGHT_LEG VALUES(11002, 1, '2020-12-7 10:50:00', '2020-12-7 16:55:00', 'HOU', 'MIA', 'Scheduled', 50, 0);
INSERT INTO FLIGHT_LEG VALUES(11002, 2, '2020-12-7 17:50:00', '2020-12-7 20:55:00', 'MIA', 'JFK', 'Scheduled', 50, 0);
INSERT INTO FLIGHT_LEG VALUES(21001, 1, '2020-12-15 03:00:00', '2020-12-15 8:00:00', 'HOU', 'LAX', 'Scheduled', 50, 0);
INSERT INTO FLIGHT_LEG VALUES(21002, 1, '2020-12-15 06:00:00', '2020-12-15 9:00:00', 'HOU', 'ORD', 'Scheduled', 50, 0);
INSERT INTO FLIGHT_LEG VALUES(21002, 2, '2020-12-15 11:00:00', '2020-12-15 15:00:00', 'ORD', 'MIA', 'Scheduled', 50, 0);
INSERT INTO FLIGHT_LEG VALUES(31001, 1, '2020-12-23 07:00:00', '2020-12-23 10:00:00', 'LAX', 'HOU', 'Scheduled', 50, 0);
INSERT INTO FLIGHT_LEG VALUES(31002, 1, '2020-12-23 08:00:00', '2020-12-23 11:00:00', 'JFK', 'MIA', 'Scheduled', 50, 0);
INSERT INTO FLIGHT_LEG VALUES(31002, 2, '2020-12-23 12:00:00', '2020-12-23 15:00:00', 'MIA', 'HOU', 'Scheduled', 50, 0);
INSERT INTO FLIGHT_LEG VALUES(41001, 1, '2020-12-31 02:00:00', '2020-12-31 6:00:00', 'JFK', 'HOU', 'Scheduled', 50, 0);
INSERT INTO FLIGHT_LEG VALUES(41002, 1, '2020-12-31 05:00:00', '2020-12-31 9:00:00', 'MIA', 'ORD', 'Scheduled', 50, 0);
INSERT INTO FLIGHT_LEG VALUES(41002, 2, '2020-12-31 10:00:00', '2020-12-31 14:00:00', 'ORD', 'HOU', 'Scheduled', 50, 0);
INSERT INTO FLIGHT_LEG VALUES(51001, 1, '2020-12-18 13:00:00', '2020-12-18 17:00:00', 'MIA', 'LAX', 'Scheduled', 50, 0);
INSERT INTO FLIGHT_LEG VALUES(51002, 1, '2020-12-18 07:00:00', '2020-12-18 11:00:00', 'LAX', 'ORD', 'Scheduled', 50, 0);
INSERT INTO FLIGHT_LEG VALUES(51002, 2, '2020-12-18 12:00:00', '2020-12-18 16:00:00', 'ORD', 'JFK', 'Scheduled', 50, 0);

INSERT INTO FLIGHT_LEG VALUES(11101, 1, '2021-01-4 09:50:00', '2021-01-4 14:55:00', 'HOU', 'JFK', 'Scheduled', 50, 0);
INSERT INTO FLIGHT_LEG VALUES(11102, 1, '2021-01-4 10:50:00', '2021-01-4 16:55:00', 'HOU', 'MIA', 'Scheduled', 50, 0);
INSERT INTO FLIGHT_LEG VALUES(11102, 2, '2021-01-4 17:50:00', '2021-01-4 20:55:00', 'MIA', 'JFK', 'Scheduled', 50, 0);
INSERT INTO FLIGHT_LEG VALUES(21101, 1, '2021-01-12 03:00:00', '2021-01-12 8:00:00', 'HOU', 'LAX', 'Scheduled', 50, 0);
INSERT INTO FLIGHT_LEG VALUES(21102, 1, '2021-01-12 06:00:00', '2021-01-12 9:00:00', 'HOU', 'ORD', 'Scheduled', 50, 0);
INSERT INTO FLIGHT_LEG VALUES(21102, 2, '2021-01-12 11:00:00', '2021-01-12 15:00:00', 'ORD', 'MIA', 'Scheduled', 50, 0);
INSERT INTO FLIGHT_LEG VALUES(31101, 1, '2021-01-20 07:00:00', '2021-01-20 10:00:00', 'LAX', 'HOU', 'Scheduled', 50, 0);
INSERT INTO FLIGHT_LEG VALUES(31102, 1, '2021-01-20 08:00:00', '2021-01-20 11:00:00', 'JFK', 'MIA', 'Scheduled', 50, 0);
INSERT INTO FLIGHT_LEG VALUES(31102, 2, '2021-01-20 12:00:00', '2021-01-20 15:00:00', 'MIA', 'HOU', 'Scheduled', 50, 0);
INSERT INTO FLIGHT_LEG VALUES(41101, 1, '2021-01-28 02:00:00', '2021-01-28 6:00:00', 'JFK', 'HOU', 'Scheduled', 50, 0);
INSERT INTO FLIGHT_LEG VALUES(41102, 1, '2021-01-28 05:00:00', '2021-01-28 9:00:00', 'MIA', 'ORD', 'Scheduled', 50, 0);
INSERT INTO FLIGHT_LEG VALUES(41102, 2, '2021-01-28 10:00:00', '2021-01-28 14:00:00', 'ORD', 'HOU', 'Scheduled', 50, 0);
INSERT INTO FLIGHT_LEG VALUES(51101, 1, '2021-01-15 13:00:00', '2021-01-15 17:00:00', 'MIA', 'LAX', 'Scheduled', 50, 0);
INSERT INTO FLIGHT_LEG VALUES(51102, 1, '2021-01-15 07:00:00', '2021-01-15 11:00:00', 'LAX', 'ORD', 'Scheduled', 50, 0);
INSERT INTO FLIGHT_LEG VALUES(51102, 2, '2021-01-15 12:00:00', '2021-01-15 16:00:00', 'ORD', 'JFK', 'Scheduled', 50, 0);





