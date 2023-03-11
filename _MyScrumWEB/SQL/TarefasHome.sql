CREATE VIEW TarefasHome AS
SELECT tarefa.id_tarefa, tarefa.prioridade, tarefa.stat, tarefa.porcentagem, tarefa.prazo,
tarefa.data_ini, tarefa.data_real, tarefa.data_fim,
(SELECT departamento FROM departamento WHERE departamento.id_departamento = tarefa.id_departamento) as departamento,
(SELECT centrocusto FROM centro_custo WHERE centro_custo.id_centro_custo = tarefa.id_centro_custo) as centro_custo,
(SELECT peso FROM tamanho WHERE id_tamanho = tarefa.id_tamanho) as tamanho,
(SELECT nome FROM pessoa WHERE id_pessoa = tarefa.pendente_por) as pendente_por, 
(SELECT nome FROM pessoa WHERE pessoa.id_pessoa = tarefa.responsavel) as responsavel,
(SELECT nome FROM pessoa WHERE pessoa.id_pessoa = tarefa.autoridade) as autoridade,
(SELECT nome FROM pessoa WHERE pessoa.id_pessoa = tarefa.checado) as checado,
(SELECT processo FROM processos WHERE id_processo = processo_relacionado) as processo_relacionado,
(SELECT nome FROM pessoa WHERE id_pessoa = executor.executor1) as executor1, executor.porcento1,
(SELECT nome FROM pessoa WHERE id_pessoa = executor.executor2) as executor2, executor.porcento2,
(SELECT nome FROM pessoa WHERE id_pessoa = executor.executor3) as executor3, executor.porcento3,
(SELECT nome FROM pessoa WHERE id_pessoa = executor.executor4) as executor4, executor.porcento4,
(SELECT nome FROM pessoa WHERE id_pessoa = executor.executor5) as executor5, executor.porcento5,
(SELECT nome FROM pessoa WHERE id_pessoa = executor.executor6) as executor6, executor.porcento6,
(SELECT nome FROM pessoa WHERE id_pessoa = executor.executor7) as executor7, executor.porcento7,
(SELECT nome FROM pessoa WHERE id_pessoa = executor.executor8) as executor8, executor.porcento8,
(SELECT nome FROM pessoa WHERE id_pessoa = executor.executor9) as executor9, executor.porcento9,
(SELECT nome FROM pessoa WHERE id_pessoa = executor.executor10) as executor10, executor.porcento10
FROM tarefa
INNER JOIN executor
ON tarefa.id_tarefa = executor.id_tarefa
WHERE tarefa.stat != 'Cancelado'

DROP VIEW TarefasHome

SELECT * FROM TarefasHome