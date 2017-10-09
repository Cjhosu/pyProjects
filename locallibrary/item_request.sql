--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.3
-- Dumped by pg_dump version 9.6.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: catalog_item_request; Type: TABLE; Schema: public; Owner: choward
--

CREATE TABLE catalog_item_request (
    id integer NOT NULL,
    requested_at timestamp with time zone,
    item_id integer,
    requester_id integer,
    filled_at timestamp with time zone
);


ALTER TABLE catalog_item_request OWNER TO choward;

--
-- Name: catalog_item_request_id_seq; Type: SEQUENCE; Schema: public; Owner: choward
--

CREATE SEQUENCE catalog_item_request_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE catalog_item_request_id_seq OWNER TO choward;

--
-- Name: catalog_item_request_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: choward
--

ALTER SEQUENCE catalog_item_request_id_seq OWNED BY catalog_item_request.id;


--
-- Name: catalog_item_request id; Type: DEFAULT; Schema: public; Owner: choward
--

ALTER TABLE ONLY catalog_item_request ALTER COLUMN id SET DEFAULT nextval('catalog_item_request_id_seq'::regclass);


--
-- Data for Name: catalog_item_request; Type: TABLE DATA; Schema: public; Owner: choward
--

COPY catalog_item_request (id, requested_at, item_id, requester_id, filled_at) FROM stdin;
50	2017-10-08 09:55:44.722199-04	5	2	2017-10-08 09:56:58.472904-04
52	2017-10-08 14:34:48.132029-04	4	2	2017-10-08 14:35:30.834767-04
49	2017-10-08 14:36:31.319558-04	5	1	2017-10-08 09:56:23.741969-04
51	2017-10-08 14:38:17.892787-04	5	3	2017-10-08 09:58:38.854983-04
54	2017-10-08 15:11:29.785566-04	5	3	2017-10-08 15:11:29.785561-04
53	2017-10-08 15:08:30.905679-04	5	3	2017-10-08 15:20:28.519117-04
56	2017-10-08 15:37:36.496851-04	5	1	2017-10-08 15:37:36.521181-04
55	2017-10-08 15:37:59.729188-04	5	2	2017-10-08 15:37:59.732901-04
57	2017-10-08 15:38:17.45737-04	5	3	2017-10-08 15:38:17.461576-04
59	2017-10-08 15:39:28.091618-04	4	3	2017-10-08 15:39:28.096348-04
58	2017-10-08 15:39:51.820647-04	4	2	2017-10-08 15:39:51.823921-04
\.


--
-- Name: catalog_item_request_id_seq; Type: SEQUENCE SET; Schema: public; Owner: choward
--

SELECT pg_catalog.setval('catalog_item_request_id_seq', 59, true);


--
-- Name: catalog_item_request catalog_item_request_pkey; Type: CONSTRAINT; Schema: public; Owner: choward
--

ALTER TABLE ONLY catalog_item_request
    ADD CONSTRAINT catalog_item_request_pkey PRIMARY KEY (id);


--
-- Name: catalog_item_request_item_id_75ce5022; Type: INDEX; Schema: public; Owner: choward
--

CREATE INDEX catalog_item_request_item_id_75ce5022 ON catalog_item_request USING btree (item_id);


--
-- Name: catalog_item_request_requester_id_63c3c4cc; Type: INDEX; Schema: public; Owner: choward
--

CREATE INDEX catalog_item_request_requester_id_63c3c4cc ON catalog_item_request USING btree (requester_id);


--
-- Name: catalog_item_request catalog_item_request_item_id_75ce5022_fk_catalog_item_id; Type: FK CONSTRAINT; Schema: public; Owner: choward
--

ALTER TABLE ONLY catalog_item_request
    ADD CONSTRAINT catalog_item_request_item_id_75ce5022_fk_catalog_item_id FOREIGN KEY (item_id) REFERENCES catalog_item(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: catalog_item_request catalog_item_request_requester_id_63c3c4cc_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: choward
--

ALTER TABLE ONLY catalog_item_request
    ADD CONSTRAINT catalog_item_request_requester_id_63c3c4cc_fk_auth_user_id FOREIGN KEY (requester_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

