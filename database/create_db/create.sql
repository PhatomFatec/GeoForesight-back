SELECT
    PostGIS_full_version();

CREATE TABLE IF NOT EXISTS public.produtos (
    idProduto integer NOT NULL PRIMARY KEY,
    nome character varying(255) NOT NULL
)

CREATE TABLE IF NOT EXISTS public.empreendimento (
	idteste SERIAL PRIMARY KEY,
    idEmpreendimento bigint NOT NULL,
    idproduto integer NOT NULL,
    finalidade character varying(255),
    cesta character varying(255) NOT NULL,
    modalidade character varying(255) NOT NULL,
    FOREIGN KEY (idproduto) REFERENCES public.produtos (idproduto)
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

CREATE TABLE IF NOT EXISTS public.operacao_credito_estadual (
    ref_bacen integer NOT NULL,
    nu_ordem integer NOT NULL,
    inicio_plantio date NOT NULL,
    final_plantio date NOT NULL,
    inicio_colheita date NOT NULL,
    final_colheita date NOT NULL,
    data_liberacao date NOT NULL,
    data_vencimento date NOT NULL,
    idempreendimento integer,
    idIrrigacao integer,
    idCiclo integer,
    idGrao integer,
    PRIMARY KEY (ref_bacen, nu_ordem),
    FOREIGN KEY (idEmpreendimento) REFERENCES public.empreendimento (idEmpreendimento),
    FOREIGN KEY (idIrrigacao) REFERENCES public.irrigacao (idIrrigacao),
    FOREIGN KEY (idCiclo) REFERENCES public.ciclo_producao (idCiclo),
    FOREIGN KEY (idGrao) REFERENCES public.grao (idGrao)
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