SELECT
    PostGIS_full_version();

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
    ref_bacen integer NOT NULL,
    nu_ordem integer NOT NULL,
    inicio_plantio date NOT NULL,
    final_plantio date NOT NULL,
    inicio_colheita date NOT NULL,
    final_colheita date NOT NULL,
    data_liberacao date NOT NULL,
    data_vencimento date NOT NULL,
    idempreendimento integer,
    idirrigacao integer,
    idciclo integer,
    idgrao integer,
    CONSTRAINT operacao_credito_estadual_pkey PRIMARY KEY (ref_bacen, nu_ordem),
    CONSTRAINT operacao_credito_estadual_idciclo_fkey FOREIGN KEY (idciclo)
        REFERENCES public.ciclo_producao (idciclo) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT operacao_credito_estadual_idgrao_fkey FOREIGN KEY (idgrao)
        REFERENCES public.grao (idgrao) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT operacao_credito_estadual_idirrigacao_fkey FOREIGN KEY (idirrigacao)
        REFERENCES public.irrigacao (idirrigacao) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)


CREATE TABLE IF NOT EXISTS public.glebas (
    idGleba INTEGER NOT NULL PRIMARY KEY,
    ref_bacen integer,
    nu_ordem integer,
    coordenadas geography(Point, 4326) NOT NULL,
    altitude double precision,
    nu_ponto INTEGER NOT NULL,
    FOREIGN KEY (ref_bacen, nu_ordem) REFERENCES public.operacao_credito_estadual (ref_bacen, nu_ordem)
)