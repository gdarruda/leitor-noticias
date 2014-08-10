CREATE TABLE feeds( id_feed INTEGER AUTO_INCREMENT, link TEXT, ind_ativo CHAR(1) PRIMARY KEY (id_feed));

CREATE TABLE perfis_twitter( id_perfil INTEGER AUTO_INCREMENT, nome TEXT, ind_ativo CHAR(1) PRIMARY KEY (id_perfil));

CREATE TABLE noticias
(
 id_noticia INTEGER AUTO_INCREMENT,
 link TEXT,
 titulo TEXT,
 corpo TEXT,
 tweet TEXT,
 data_importacao DATE,
 id_feed INTEGER,
 id_perfil INTEGER,
 PRIMARY KEY (id_noticia)
);

ALTER TABLE noticias ADD CONSTRAINT fk_noticias_feeds FOREIGN KEY (id_feed) REFERENCES feeds(id_feed);
ALTER TABLE noticias ADD CONSTRAINT fk_noticias_twitter FOREIGN KEY (id_perfil) REFERENCES perfis_twitter(id_perfil);

CREATE TABLE entidades
(
 id_entidade INTEGER AUTO_INCREMENT,
 nome        TEXT,
 PRIMARY KEY (id_entidade)
);

CREATE INDEX idx_entidades USING BTREE ON entidades(nome(30));

CREATE TABLE entidades_x_noticias
(
 id_entidade INTEGER,
 id_noticia  INTEGER,
 PRIMARY KEY (id_entidade, id_noticia)
);

ALTER TABLE entidades_x_noticias ADD CONSTRAINT fk_entidadesnoticias_noticias FOREIGN KEY (id_noticia) REFERENCES noticias(id_noticia);
ALTER TABLE entidades_x_noticias ADD CONSTRAINT fk_entidadesnoticias_entidades FOREIGN KEY (id_entidade) REFERENCES entidades(id_entidade);

CREATE INDEX idx_link USING BTREE ON noticias(titulo(100));CREATE INDEX idx_feed USING BTREE ON noticias(id_feed);
CREATE INDEX idx_perfil USING BTREE ON noticias(id_perfil);
