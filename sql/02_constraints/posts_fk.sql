ALTER TABLE api_social_media.posts
ADD CONSTRAINT posts_users_fk
FOREIGN KEY (id_user)
REFERENCES api_social_media.users(id);