CREATE TABLE feeds( id_feed INTEGER AUTO_INCREMENT, link TEXT, ind_ativo CHAR(1) PRIMARY KEY (id_feed));

CREATE TABLE perfis_twitter( id_perfil INTEGER AUTO_INCREMENT, nome TEXT, ind_ativo CHAR(1) PRIMARY KEY (id_perfil));

CREATE TABLE noticias
(
 id_noticia INTEGER,
 link TEXT,
 titulo TEXT,
 corpo TEXT,
 data_importacao DATE,
 id_feed INTEGER,
 id_perfil INTEGER
);

ALTER TABLE noticias ADD CONSTRAINT fk_noticias_feeds FOREIGN KEY (id_feed) REFERENCES feeds(id_feed);
ALTER TABLE noticias ADD CONSTRAINT fk_noticias_twitter FOREIGN KEY (id_perfil) REFERENCES perfis_twitter(id_perfil);

CREATE INDEX idx_link USING BTREE ON noticias(titulo(100));CREATE INDEX idx_feed USING BTREE ON noticias(id_feed);
CREATE INDEX idx_perfil USING BTREE ON noticias(id_perfil);
