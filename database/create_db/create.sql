CREATE TABLE IF NOT EXISTS public.produtos (
    idProduto integer NOT NULL PRIMARY KEY,
    nome character varying(255) NOT NULL
)

CREATE TABLE IF NOT EXISTS public.empreendimento
(
    idteste serial NOT NULL DEFAULT nextval('empreendimento_idteste_seq'::regclass),
    idempreendimento bigint NOT NULL,
    idproduto integer NOT NULL,
    finalidade character varying(255) COLLATE pg_catalog."default",
    cesta character varying(255) COLLATE pg_catalog."default" NOT NULL,
    modalidade character varying(255) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT empreendimento_pkey PRIMARY KEY (idteste),
    CONSTRAINT empreendimento_idproduto_fkey FOREIGN KEY (idproduto)
        REFERENCES public.produtos (idproduto) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

CREATE TABLE IF NOT EXISTS public.irrigacao (
    idIrrigacao INTEGER NOT NULL PRIMARY KEY,
    descricao character varying(255)
)

CREATE TABLE IF NOT EXISTS public.grao (
    idGrao INTEGER NOT NULL PRIMARY KEY,
    descricao character varying(255)
)

CREATE TABLE IF NOT EXISTS public.ciclo_producao (
    idCiclo INTEGER NOT NULL PRIMARY KEY,
    descricao character varying(255)
)


CREATE TABLE IF NOT EXISTS public.operacao_credito_estadual
(
    ref_bacen numeric NOT NULL,
    nu_ordem numeric NOT NULL,
    inicio_plantio character varying(255) COLLATE pg_catalog."default",
    final_plantio character varying(255) COLLATE pg_catalog."default",
    inicio_colheita character varying(255) COLLATE pg_catalog."default",
    final_colheita character varying(255) COLLATE pg_catalog."default",
    data_vencimento character varying(255) COLLATE pg_catalog."default",
    idempreendimento numeric,
    idevento integer,
    idsolo integer,
    idirrigacao integer,
    idciclo integer,
    idgrao integer,
    idcultivar integer,
    idprograma integer,
    estado character(2) COLLATE pg_catalog."default",
    CONSTRAINT operacao_credito_estadual_pkey PRIMARY KEY (ref_bacen, nu_ordem),
    CONSTRAINT operacao_credito_estadual_idciclo_fkey FOREIGN KEY (idciclo)
        REFERENCES public.ciclo_producao (idciclo) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT operacao_credito_estadual_idevento_fkey FOREIGN KEY (idevento)
        REFERENCES public.evento_climatico (idevento) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT operacao_credito_estadual_idgrao_fkey FOREIGN KEY (idgrao)
        REFERENCES public.grao (idgrao) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT operacao_credito_estadual_idirrigacao_fkey FOREIGN KEY (idirrigacao)
        REFERENCES public.irrigacao (idirrigacao) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT operacao_credito_estadual_idsolo_fkey FOREIGN KEY (idsolo)
        REFERENCES public.solo (idsolo) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)



CREATE TABLE IF NOT EXISTS public.glebas
(
    idgleba integer SERIAL,
    ref_bacen numeric,
    nu_ordem numeric,
    longitude character varying(255) COLLATE pg_catalog."default",
    latitude character varying(255) COLLATE pg_catalog."default",
    coordenadas geography(Point,4326),
    altitude numeric,
    nu_ponto numeric,
    nu_identificador numeric,
    nu_indice numeric,
    CONSTRAINT glebas_pkey PRIMARY KEY (idgleba),
    CONSTRAINT glebas_ref_bacen_nu_ordem_fkey FOREIGN KEY (nu_ordem, ref_bacen)
        REFERENCES public.operacao_credito_estadual (nu_ordem, ref_bacen) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)


CREATE TABLE PUBLIC.PROGRAMA(
IDPROGRAMA    SERIAL PRIMARY KEY,
DESCRICAO     CHARACTER VARYING(255),
DATA_INICIO   DATE,
DATA_FIM      DATE,
FINANCIAMENTO CHARACTER VARYING(255)
);

CREATE TABLE PUBLIC.COOPERADOS(
ID  SERIAL,
REF_BACEN  NUMERIC,
NU_ORDEM   NUMERIC,
VALOR_PARCELA NUMERIC,
CNPJ  CHARACTER VARYING(255),
CPF  CHARACTER VARYING(255),
PRIMARY KEY(ID, REF_BACEN, NU_ORDEM));

CREATE TABLE PUBLIC.EVENTO_CLIMATICO(
IDEVENTO  SERIAL PRIMARY KEY,
DESCRICAO CHARACTER VARYING(255));

CREATE TABLE PUBLIC.SOLO(
IDSOLO    SERIAL PRIMARY KEY,
DESCRICAO CHARACTER VARYING(255));

CREATE TABLE PUBLIC.MUNICIPIO_GLEBAS(
    REF_BACEN NUMERIC,
    NU_ORDEM NUMERIC,
    NOME CHARACTER VARYING(255),
    PRIMARY KEY(REF_BACEN, NU_ORDEM),
	CONSTRAINT municipio_glebas_ref_bacen_nu_ordem_fkey FOREIGN KEY (nu_ordem, ref_bacen)
    REFERENCES public.operacao_credito_estadual (nu_ordem, ref_bacen) MATCH SIMPLE
)