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
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: choward
--

CREATE TABLE django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE django_migrations OWNER TO choward;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: choward
--

CREATE SEQUENCE django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_migrations_id_seq OWNER TO choward;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: choward
--

ALTER SEQUENCE django_migrations_id_seq OWNED BY django_migrations.id;


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: choward
--

ALTER TABLE ONLY django_migrations ALTER COLUMN id SET DEFAULT nextval('django_migrations_id_seq'::regclass);


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: choward
--

COPY django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2017-09-02 14:47:04.74079-04
2	auth	0001_initial	2017-09-02 14:47:04.786573-04
3	admin	0001_initial	2017-09-02 14:47:04.804321-04
4	admin	0002_logentry_remove_auto_add	2017-09-02 14:47:04.815885-04
5	contenttypes	0002_remove_content_type_name	2017-09-02 14:47:04.833882-04
6	auth	0002_alter_permission_name_max_length	2017-09-02 14:47:04.838737-04
7	auth	0003_alter_user_email_max_length	2017-09-02 14:47:04.847609-04
8	auth	0004_alter_user_username_opts	2017-09-02 14:47:04.858593-04
9	auth	0005_alter_user_last_login_null	2017-09-02 14:47:04.866874-04
10	auth	0006_require_contenttypes_0002	2017-09-02 14:47:04.868276-04
11	auth	0007_alter_validators_add_error_messages	2017-09-02 14:47:04.877911-04
12	auth	0008_alter_user_username_max_length	2017-09-02 14:47:04.887513-04
13	catalog	0001_initial	2017-09-02 14:47:04.909838-04
14	sessions	0001_initial	2017-09-02 14:47:04.916572-04
15	catalog	0002_comic_item_status	2017-09-02 14:49:56.70745-04
16	catalog	0003_auto_20170909_0909	2017-09-09 09:09:26.621608-04
17	catalog	0004_auto_20170910_1710	2017-09-10 17:10:52.712432-04
18	catalog	0005_auto_20170911_1745	2017-09-11 17:45:37.908563-04
19	catalog	0006_auto_20170911_1830	2017-09-11 18:33:02.411654-04
20	catalog	0007_auto_20170911_2138	2017-09-11 21:38:54.410163-04
21	catalog	0008_auto_20171003_1847	2017-10-03 18:47:52.347842-04
22	catalog	0008_auto_20171003_2102	2017-10-03 21:17:57.863972-04
23	catalog	0009_auto_20171006_1529	2017-10-06 15:29:50.063846-04
24	catalog	0010_auto_20171006_2112	2017-10-06 21:13:12.450354-04
\.


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: choward
--

SELECT pg_catalog.setval('django_migrations_id_seq', 24, true);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: choward
--

ALTER TABLE ONLY django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

