CREATE TABLE api_social_media.users (
    id bigserial NOT NULL,
    nome varchar(800) NOT NULL,
    email varchar(254) NOT NULL,
    guid UUID NOT NULL,

    CONSTRAINT users_pk PRIMARY KEY (id),
    CONSTRAINT users_unique UNIQUE (email),
    CONSTRAINT users_unique_1 UNIQUE (guid)
);

COMMENT ON TABLE api_social_media.users IS 'Tabela de usuários';

COMMENT ON COLUMN api_social_media.users.id IS 'Chave primária da tabela users';
COMMENT ON COLUMN api_social_media.users.nome IS 'Nome do usuário';
COMMENT ON COLUMN api_social_media.users.email IS 'Email do usuário';
COMMENT ON COLUMN api_social_media.users.guid IS 'GUID do usuário';