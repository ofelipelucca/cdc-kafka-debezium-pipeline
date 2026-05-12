ALTER TABLE api_social_media.likes
ADD CONSTRAINT likes_post_fk
FOREIGN KEY (id_post)
REFERENCES api_social_media.posts(id);

ALTER TABLE api_social_media.likes
ADD CONSTRAINT likes_user_fk
FOREIGN KEY (id_user)
REFERENCES api_social_media.users(id);