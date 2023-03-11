CREATE VIEW ListarPessoas AS
SELECT id_pessoa, nome, login,
IF (ativo = 1, "Ativo", "Bloqueado") AS ativo,
IF (adm = 0, "Usuario", 
IF(adm = 1, "Administrador", 
IF(adm = 2, "Lider", 
IF(adm = 3, "Gestor", "")))) AS adm,

(SELECT departamento FROM departamento WHERE departamento.id_departamento = pessoa.id_departamento) as departamento,
(SELECT centrocusto FROM centro_custo WHERE centro_custo.id_centro_custo = pessoa.id_centrocusto) as centro_custo

FROM pessoa

SELECT * FROM ListarPessoas;

SHOW TABLES;

DROP VIEW ListarPessoas