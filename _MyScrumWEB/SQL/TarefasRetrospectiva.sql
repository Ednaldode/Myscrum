CREATE VIEW TarefasRetrospectiva AS
SELECT tarefa.id_tarefa, tarefa.descri, tarefa.stat, tarefa.prioridade,
(SELECT nome FROM pessoa WHERE id_pessoa = tarefa.responsavel) AS responsavel,
(SELECT nome FROM pessoa WHERE id_pessoa = tarefa.autoridade) AS autoridade,
tarefa.data_ini, tarefa.data_real, tarefa.data_fim,
(SELECT departamento.departamento FROM departamento WHERE id_departamento = tarefa.id_departamento) AS departamento,
(SELECT centro_custo.centrocusto FROM centro_custo WHERE id_centro_custo = tarefa.id_centro_custo) AS centro_custo,
(SELECT processos.processo FROM processos WHERE id_processo = tarefa.processo_relacionado) AS processo_relacionado,
CONCAT(executor.executor1, ', ', executor.executor1) AS Executores,
(SELECT nome FROM pessoa WHERE id_pessoa = executor.executor1) as executor1, executor.porcento1,
(SELECT nome FROM pessoa WHERE id_pessoa = executor.executor2) as executor2, executor.porcento2,
(SELECT nome FROM pessoa WHERE id_pessoa = executor.executor3) as executor3, executor.porcento3,
(SELECT nome FROM pessoa WHERE id_pessoa = executor.executor4) as executor4, executor.porcento4,
(SELECT nome FROM pessoa WHERE id_pessoa = executor.executor5) as executor5, executor.porcento5,
(SELECT nome FROM pessoa WHERE id_pessoa = executor.executor6) as executor6, executor.porcento6,
(SELECT nome FROM pessoa WHERE id_pessoa = executor.executor7) as executor7, executor.porcento7,
(SELECT nome FROM pessoa WHERE id_pessoa = executor.executor8) as executor8, executor.porcento8,
(SELECT nome FROM pessoa WHERE id_pessoa = executor.executor9) as executor9, executor.porcento9,
(SELECT nome FROM pessoa WHERE id_pessoa = executor.executor10) as executor10, executor.porcento10,
retrospectiva.descricao, retrospectiva.stats, retrospectiva.finalizado, retrospectiva.id_responsavel
FROM tarefa
INNER JOIN executor 
ON tarefa.id_tarefa = executor.id_tarefa
INNER JOIN retrospectiva 
ON tarefa.id_tarefa = retrospectiva.id_tarefa
WHERE retrospectiva.finalizado != 1