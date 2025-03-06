import os

search_trigger = [
    "Atividades e Tarefas", "Funções e Responsabilidades", "Tarefas e Atribuições", "Deveres e Obrigações", "Principais Atividades",
    "Atividades Diárias", "Responsabilidades e Deveres", "Responsabilidades e Funções", "Atribuições e Responsabilidades", "Requisitos e Qualificações",
    "Exigências e Competências", "Critérios e Habilidades", "Habilidades e Experiência", "Requisitos Necessários", "Perfil e Requisitos",
    "Perfil e Qualificações", "Expectativas e Competências", "O que esperamos de você", "O que buscamos em você", "Qualificações Desejadas",
    "Competências e Experiência", "Requisitos e Experiência", "Critérios e Expectativas", "Funções, Tarefas e Responsabilidades", "Atividades, Requisitos e Qualificações",
    "Descrição das Funções", "Principais Responsabilidades", "Detalhamento das Atividades", "Especificações do Cargo", "Competências Requeridas",
    "Exigências e Qualificações", "Critérios de Seleção", "Contribuições e Responsabilidades", "Missão do Cargo", "Atuação e Responsabilidades",
    "Papel e Atribuições", "Desafios do Cargo", "Exigências do Cargo", "Perfil do Candidato", "Competências Essenciais",
    "Habilidades Necessárias", "Requisitos e Competências", "Experiência e Qualificações", "Detalhes da Vaga", "Atividades",
    "Funções", "Tarefas", "Deveres", "Rotina", "Atribuições",
    "Requisitos", "Exigências", "Critérios", "Habilidades", "Perfil",
    "Expectativas", "Busca", "Qualificações", "Competências", "Seleção",
    "Contribuição", "Missão", "Atuação", "Desafios", "Detalhes"
]

cargo = "Engenheiro de Dados Sênio"

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'extracted_data', cargo)

for file in os.listdir(path):
    with open(os.path.join(path, file), 'r', encoding='utf-8') as archive:

        archive = archive.read()

        start_row = 0
        
        for search_trigger_text in search_trigger:
            if search_trigger_text in archive:
                for i, row in enumerate(archive.split('\n')):
                    if search_trigger_text in row:
                        start_row = i
                


            
            

                

print(count_search_trigger, len(os.listdir(path)))
        

