CREATE TABLE api_social_media.posts (
    id bigserial NOT NULL,
    content text NOT NULL,
    id_user int8 NOT NULL,
    guid varchar(36) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT posts_pk PRIMARY KEY (id),
    CONSTRAINT posts_unique UNIQUE (guid)
);

COMMENT ON COLUMN api_social_media.posts.id IS 'Chave primária da tabela posts';
COMMENT ON COLUMN api_social_media.posts.content IS 'Conteúdo do post';
COMMENT ON COLUMN api_social_media.posts.id_user IS 'Chave estrangeira que referencia o usuário criador do post';
COMMENT ON COLUMN api_social_media.posts.guid IS 'GUID do post';
COMMENT ON COLUMN api_social_media.posts.created_at IS 'Data e hora de criação do post';