--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3
-- Dumped by pg_dump version 16.3

-- Started on 2024-07-17 15:54:01

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 216 (class 1259 OID 16429)
-- Name: roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles (
    id smallint NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.roles OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 16428)
-- Name: roles_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.roles_id_seq
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.roles_id_seq OWNER TO postgres;

--
-- TOC entry 4861 (class 0 OID 0)
-- Dependencies: 215
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;


--
-- TOC entry 218 (class 1259 OID 16438)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id bigint NOT NULL,
    username character varying(50) NOT NULL,
    role smallint,
    email character varying(100) NOT NULL,
    password character varying(255) NOT NULL,
    first_name character varying(100),
    last_name character varying(100),
    phone character varying(20),
    address text,
    created_at bigint DEFAULT EXTRACT(epoch FROM CURRENT_TIMESTAMP),
    updated_at bigint DEFAULT EXTRACT(epoch FROM CURRENT_TIMESTAMP),
    is_deleted boolean DEFAULT false,
    deleted_at bigint
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16437)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- TOC entry 4862 (class 0 OID 0)
-- Dependencies: 217
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 4692 (class 2604 OID 16432)
-- Name: roles id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- TOC entry 4693 (class 2604 OID 16441)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 4853 (class 0 OID 16429)
-- Dependencies: 216
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roles (id, name) FROM stdin;
1	admin
2	user
3	demo
\.


--
-- TOC entry 4855 (class 0 OID 16438)
-- Dependencies: 218
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, role, email, password, first_name, last_name, phone, address, created_at, updated_at, is_deleted, deleted_at) FROM stdin;
63	string	2	user@example.com	$2b$12$f7lKRqrpbeRVFIiXhCfruOeVlyV5k1HnDIoujkkWr3DUe2zNwqRUa	string	string	string	string	1720791728	1720791728	f	\N
64	SuperRogi	2	super@rogi.com	$2b$12$MQyy2nSmPkFlYoeC88keIONQC71eOjCl.huLCglPqi54Nr5kERJmu	Super	Rogi	\N	Moscow	1720792089	1720792089	f	\N
66	SuperRogi2	2	super@rogi2.com	$2b$12$u87n7hxsWY054mms3bcnP.zc3I8SGnMobzjIOeT.bEbp1JmzsGLha	\N	\N	\N	\N	1720796008	1720796008	f	\N
68	SlowPoke	2	slow@poke.com	$2b$12$eVfEbO4co0VFqp32U20J1.PBRs19FU1z8pcUCBU/YoL3tooIGUfny	Дмитрий	Проценко	+7 (xxx) zzz-yz-zy	Центр Краснодара	1720809603	1720809603	f	\N
69	mat	2	matvsuzu@gmail.com	$2b$12$cbaqOnhvyzz3FO3BeIw5c.k7Sw3fvwAWTWSamcebmUIYJysiowGEy	Матвей	Сюсюкин	+79859772386	пр К	1721046493	1721046493	f	\N
\.


--
-- TOC entry 4863 (class 0 OID 0)
-- Dependencies: 215
-- Name: roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.roles_id_seq', 3, true);


--
-- TOC entry 4864 (class 0 OID 0)
-- Dependencies: 217
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 71, true);


--
-- TOC entry 4698 (class 2606 OID 16436)
-- Name: roles roles_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_name_key UNIQUE (name);


--
-- TOC entry 4700 (class 2606 OID 16434)
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- TOC entry 4702 (class 2606 OID 16452)
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- TOC entry 4704 (class 2606 OID 16448)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 4706 (class 2606 OID 16450)
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- TOC entry 4708 (class 2620 OID 16459)
-- Name: users set_default_role_trigger; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER set_default_role_trigger BEFORE INSERT ON public.users FOR EACH ROW EXECUTE FUNCTION public.set_default_role();


--
-- TOC entry 4707 (class 2606 OID 16453)
-- Name: users users_role_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_role_fkey FOREIGN KEY (role) REFERENCES public.roles(id);


-- Completed on 2024-07-17 15:54:02

--
-- PostgreSQL database dump complete
--

