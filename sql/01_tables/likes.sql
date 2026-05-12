CREATE TABLE api_social_media.likes (
    id bigserial NOT NULL,
    id_post int8 NOT NULL,
    id_user int8 NOT NULL,
    guid UUID NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT likes_pk PRIMARY KEY (id),
    CONSTRAINT likes_unique UNIQUE (id_post, id_user),
    CONSTRAINT likes_guid_unique UNIQUE (guid),
    CONSTRAINT likes_post_fk FOREIGN KEY (id_post) REFERENCES api_social_media.posts(id) ON DELETE CASCADE,
    CONSTRAINT likes_user_fk FOREIGN KEY (id_user) REFERENCES api_social_media.users(id) ON DELETE CASCADE
);

COMMENT ON COLUMN api_social_media.likes.id IS 'Chave primária da tabela likes';
COMMENT ON COLUMN api_social_media.likes.id_post IS 'Chave estrangeira que referencia o post que recebeu o like';
COMMENT ON COLUMN api_social_media.likes.id_user IS 'Chave estrangeira que referencia o usuário que deu o like';
COMMENT ON COLUMN api_social_media.likes.guid IS 'GUID do like';
COMMENT ON COLUMN api_social_media.likes.created_at IS 'Data e hora de criação do like';