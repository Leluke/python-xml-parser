# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from datetime import datetime
from prettytable import PrettyTable
import sys
import csv
from os import listdir
from os.path import isfile, join

def get_name(root_object):
  general_data = root_object.find("./DADOS-GERAIS")
  full_name = general_data.attrib['NOME-COMPLETO']
  return full_name

#'NOME-CURSO'
#'NOME-INSTITUICAO'
#'ANO-DE-INICIO'
#'ANO-DE-CONCLUSAO' (#Checa se concluiu ou não o curso, se sim retorna o numero do ano, se não retorna falso)
def get_graduation_list(root_object):
  grad_list = root_object.findall("./DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/GRADUACAO")
  return grad_list

def get_masters_list(root_object):
  masters_list = root_object.findall("./DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/MESTRADO")
  return masters_list

def get_doctorates_list(root_object):
  doctorates_list = root_object.findall("./DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/DOUTORADO")
  return doctorates_list

def get_postgrad_list(root_object):
  postgrad_list = []
  academic_formation_object = root_object.find("./DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO")
  for academic_formation in academic_formation_object:
    if academic_formation.tag == 'GRADUACAO':
      pass
    else:
      postgrad_list.append(academic_formation)
  
  return postgrad_list

def get_postgrad_list_from_date(root_object, initial_date):
  return_list = []
  #Pega lista de todas as pos graduacoes
  postgrad_list = get_postgrad_list(root_object)
  
  for postgrad in postgrad_list:
    #Checa se ano de inicio da pos é maior ou igual ao initial date passado
    #Pega ano de inicio
    if get_grad_start_year(postgrad) >= initial_date :
      return_list.append(postgrad)
    else:
      pass
  return return_list

def is_course(root_object, course_name):
  grads_to_check = get_graduation_list(root_object)
  for grad in grads_to_check:
    #print(grad.attrib['NOME-CURSO'])
    if course_name == grad.attrib['NOME-CURSO']:
      return True  
  return False

def get_grad_elem_course_name_list(root_object):
  grad_elem_course_name_list = []
  graduations_to_get_course_name = get_graduation_list(root_object)
  for grad in graduations_to_get_course_name:
    grad_elem_course_name_list.append(grad.attrib['NOME-CURSO'])
  
  return grad_elem_course_name_list

def get_course_grad_elem(root_object, course_name):
  grads_to_check = get_graduation_list(root_object)
  for grad in grads_to_check:
    if course_name == grad.attrib['NOME-CURSO']:
      return grad

def get_grad_conclusion_year(grad):
  if 'ANO-DE-CONCLUSAO' not in grad.attrib:
    #print ('Não tem campo ANO-DE-CONCLUSAO')
    return "not-graduated"
  elif grad.attrib['ANO-DE-CONCLUSAO'] == "":
    return "not-graduated"
  elif grad.attrib['STATUS-DO-CURSO'] == "CONCLUIDO":
    return grad.attrib['ANO-DE-CONCLUSAO']
  else:
    return "not-graduated"

def get_grad_start_year(grad):
  if 'ANO-DE-INICIO' not in grad.attrib:
    #print ('Não tem campo ANO-DE-INICIO')
    return "not-graduated"
  elif grad.attrib['ANO-DE-INICIO'] == "":
    return "not-graduated"
  else:
    return grad.attrib['ANO-DE-INICIO']

def get_grad_institute(grad):
  if 'NOME-INSTITUICAO' not in grad.attrib:
    #print ('Não tem campo NOME-INSTITUICAO')
    return "no-name"
  elif grad.attrib['NOME-INSTITUICAO'] == "":
    return "no-name"
  else:
    return grad.attrib['NOME-INSTITUICAO']

def get_grad_course_name(grad):
  if 'NOME-CURSO' not in grad.attrib:
    #print ('Não tem campo NOME-CURSO')
    return "no-name"
  elif grad.attrib['NOME-CURSO'] == "":
    return "no-name"
  else:
    return grad.attrib['NOME-CURSO']

def get_course_grad_conclusion_year(root_object, course_name):
  course_grad_elem = get_course_grad_elem(root_object, course_name)
  conclusion_year = get_grad_conclusion_year(course_grad_elem)
  return conclusion_year

def get_course_grad_start_year(root_object, course_name):
  course_grad_elem = get_course_grad_elem(root_object, course_name)
  start_year = get_grad_start_year(course_grad_elem)
  return start_year

def get_course_grad_institute(root_object, course_name):
  course_grad_elem = get_course_grad_elem(root_object, course_name)
  course_grad_institute = get_grad_institute(course_grad_elem)
  return course_grad_institute

def get_professional_action_list(root_object):
  professional_action_list = root_object.findall("./DADOS-GERAIS/ATUACOES-PROFISSIONAIS/ATUACAO-PROFISSIONAL")
  return professional_action_list

def get_bond_list(professional_action):
  bond_list = professional_action.findall("./VINCULOS")
  return bond_list

def get_action_bond_list_from_date(professional_action_list, initial_date):
  return_list = []
  for action in professional_action_list:
    bond_list = get_bond_list(action)
    #Checa vinculo a vinculo se o ano de inicio é maior que a data inicial passada
    valid_bond_list = []
    for bond in bond_list:
      if bond.attrib['ANO-INICIO'] >= initial_date :
        valid_bond_list.append(bond)
      else:
        pass
    action_bond_pair = {"action": action, "bond_list": valid_bond_list}
    return_list.append(action_bond_pair)
  return return_list

def print_action_bond_pair(action_bond_pair):
  if action_bond_pair['bond_list'] == []:
    pass
  else:
    print("Ação profissional:")
    print(action_bond_pair['action'].attrib)
    print("Vinculos validos:")
    for bond in action_bond_pair['bond_list']:
      print(bond.attrib)

def pretty_print_action_bond_pair(action_bond_pair):
  if action_bond_pair['bond_list'] == []:
    pass
  else:
    print("Ação profissional: " + action_bond_pair['action'].attrib['NOME-INSTITUICAO'])
    #print(action_bond_pair['action'].attrib)
    print("Vinculos validos:")
    for bond in action_bond_pair['bond_list']:
      #print(bond.attrib)
      print(bond.attrib['ANO-INICIO'])
      print(bond.attrib['OUTRO-ENQUADRAMENTO-FUNCIONAL-INFORMADO'])

#Melhoria: Receber a tupla e criar de maneira independente. Passar valor por valor
def create_data_row_generic():
  data_row = [full_name, grad_start_year, grad_year, course_name, course_grad_institute, bond.attrib['ANO-INICIO'], action.attrib['NOME-INSTITUICAO'], bond.attrib['OUTRO-ENQUADRAMENTO-FUNCIONAL-INFORMADO']]
  return data_row

def create_data_row(full_name, grad_start_year , grad_year, course_name, course_grad_institute, action, bond):
  data_row = [full_name, grad_start_year, grad_year, course_name, course_grad_institute, bond.attrib['ANO-INICIO'], action.attrib['NOME-INSTITUICAO'], bond.attrib['OUTRO-ENQUADRAMENTO-FUNCIONAL-INFORMADO']]
  return data_row

def create_data_row_relation_professional_action_after_course_conclusion(full_name, grad_start_year , grad_year, course_name, course_grad_institute, action, bond):
  data_row = [full_name, grad_start_year, grad_year, course_name, course_grad_institute, bond.attrib['ANO-INICIO'], action.attrib['NOME-INSTITUICAO'], bond.attrib['OUTRO-ENQUADRAMENTO-FUNCIONAL-INFORMADO']]
  return data_row

def create_data_row_relation_postgrad_after_course_conclusion(full_name, grad_start_year , grad_year, course_name, course_grad_institute, postgrad_start_year, postgrad_conclusion_year, postgrad_institue, postgrad_course):
  data_row = [full_name, grad_start_year, grad_year, course_name, course_grad_institute, postgrad_start_year, postgrad_conclusion_year, postgrad_institue, postgrad_course]
  return data_row

#professional_action_after_course_conclusion  professional_action_after_course_conclusion relation
#Para o curso passado, pega o ano de conclusao do curso e usa para definir todas as atuações profissionais que a pessoa teve após concluir o curso
def get_data_row_relation_professional_action_after_course_conclusion(root_object, course_name):
  data_rows_list = []
  if is_course(root_object, course_name):
    #nome_completo
    full_name = get_name(root_object)
    #ano_conclusao_curso
    conclusion_year = get_course_grad_conclusion_year(root_object, course_name)
    #ano_inicio_curso
    start_year = get_course_grad_start_year(root_object, course_name)
    #nome_instituicao_curso
    course_grad_institute = get_course_grad_institute(root_object, course_name)
    professional_action_list = get_professional_action_list(root_object)
    action_bond_list = get_action_bond_list_from_date(professional_action_list, conclusion_year)
    for action_bond_pair in action_bond_list:
      for bond in action_bond_pair['bond_list']:
        data_row = [full_name, start_year, conclusion_year, course_name, course_grad_institute, bond.attrib['ANO-INICIO'], action_bond_pair['action'].attrib['NOME-INSTITUICAO'], bond.attrib['OUTRO-ENQUADRAMENTO-FUNCIONAL-INFORMADO']]
        #data_row = create_data_row(full_name, start_year, conclusion_year, course_name, course_grad_institute, action_bond_pair['action'], bond)
        data_rows_list.append(data_row)
  return data_rows_list

#postgrad_after_course_conclusion  postgrad_after_course_conclusion relation
#Para o curso passado, pega o ano de conclusao do curso e usa para definir todos os aperfeiçoamentos que a pessoa fez após concluir o curso
def get_data_row_relation_postgrad_after_course_conclusion(root_object, course_name):
  data_rows_list = []
  if is_course(root_object, course_name):
    #nome_completo
    full_name = get_name(root_object)
    #ano_conclusao_curso
    conclusion_year = get_course_grad_conclusion_year(root_object, course_name)
    #ano_inicio_curso
    start_year = get_course_grad_start_year(root_object, course_name)
    #nome_instituicao_curso
    course_grad_institute = get_course_grad_institute(root_object, course_name)
    postgrad_list_from_date = get_postgrad_list_from_date(root_object, conclusion_year)
    for postgrad in postgrad_list_from_date:
      postgrad_start_year = get_grad_start_year(postgrad)
      postgrad_conclusion_year = get_grad_conclusion_year(postgrad)
      postgrad_institue = get_grad_institute(postgrad)
      postgrad_course_name = get_grad_course_name(postgrad)
      postgrad_type = postgrad.tag

      data_row = [full_name, start_year, conclusion_year, course_name, course_grad_institute, postgrad_start_year, postgrad_conclusion_year, postgrad_type, postgrad_institue, postgrad_course_name]
      data_rows_list.append(data_row)
  return data_rows_list
  
def process_xml(root_object, course_name, relation):
  if relation == "professional_action_after_course_conclusion":
    data_rows_list = get_data_row_relation_professional_action_after_course_conclusion(root_object, course_name)
  elif relation == "postgrad_after_course_conclusion":
    data_rows_list = get_data_row_relation_postgrad_after_course_conclusion(root_object, course_name)
  else:
    print("Nenhuma extração identificada com o tipo passado: {}".format(relation))
    data_rows_list = []
  return data_rows_list

def process_xml_filterless(root_object, relation):
  #Pegar cursos na graduação.
  #Montar aqui uma lista de cursos que sabemos que ja tem então vai dar match
  #Rodamos a função de pegar relações passando os cursos
  #Combinamos os resultados antes de enviar

  #grad_elem_course_name_list = get_grad_elem_course_name_list(root_object)
  #Ao inves de retornar os nomes, só retorna nomes dos cursos formados
  grad_elem_course_name_list = get_grad_elem_course_name_list(root_object)
  grad_elem_course_name_list = list(set(grad_elem_course_name_list))

  final_data_row_list = []
  for course_name in grad_elem_course_name_list:
    if relation == "professional_action_after_course_conclusion":
      data_rows_list = get_data_row_relation_professional_action_after_course_conclusion(root_object, course_name)
    elif relation == "postgrad_after_course_conclusion":
      data_rows_list = get_data_row_relation_postgrad_after_course_conclusion(root_object, course_name)
    else:
      print("Nenhuma extração identificada com o tipo passado: {}".format(relation))
      data_rows_list = []
    final_data_row_list = final_data_row_list + data_rows_list
  
  return final_data_row_list

def process_xml_file(file_name, course_name, relation):
  file = file_name
  tree = ET.parse(file)
  root = tree.getroot()
  return process_xml(root, course_name, relation)

def process_xml_file_filterless(file_name, relation):
  file = file_name
  tree = ET.parse(file)
  root = tree.getroot()
  return process_xml_filterless(root, relation)

LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'

def process_all_xml_files(course_name, folder_name, relation):
  path = './' + folder_name
  file_name_list = [f for f in listdir(path) if isfile(join(path, f))]
  final_data_row_list = []
  data_row_list = []

  total_files=len(file_name_list)
  current_file_number = 0
  print('')
  print("Total files to process: {}".format(total_files))
  for file_name in file_name_list:
    current_file_number = current_file_number + 1
    percentage =  (current_file_number / total_files) * 100
    print("percent complete: {}".format(percentage), end='\n')
    print("current file number: {}".format(current_file_number))  
    print(LINE_UP, end='')
    print(LINE_UP, end='\r')
    file_path = folder_name + '/' + file_name
    data_row_list = process_xml_file(file_path, course_name, relation)
    if data_row_list == []:
      pass
    else:
      final_data_row_list = final_data_row_list + data_row_list

  print("percent complete: {}".format(percentage), end='\n')
  return final_data_row_list

def process_all_xml_files_filterless(folder_name, relation):
  path = './' + folder_name
  file_name_list = [f for f in listdir(path) if isfile(join(path, f))]
  final_data_row_list = []
  data_row_list = []

  total_files=len(file_name_list)
  current_file_number = 0
  print('')
  print("Total files to process: {}".format(total_files))
  for file_name in file_name_list:
    current_file_number = current_file_number + 1
    percentage =  (current_file_number / total_files) * 100
    #print("percent complete: {}".format(percentage), end='\n')
    #print("current file number: {}".format(current_file_number))  
    #print(LINE_UP, end='')
    #print(LINE_UP, end='\r')
    file_path = folder_name + '/' + file_name
    data_row_list = process_xml_file_filterless(file_path, relation)
    if data_row_list == []:
      pass
    else:
      final_data_row_list = final_data_row_list + data_row_list

  #print("percent complete: {}".format(percentage), end='\n')
  return final_data_row_list

#Recebe lista de tuplas da tabela e um header e printa na tela de maneira organizada
def pretty_print_table(data_row_list, header):
  t = PrettyTable(header)
  for row in data_row_list:
    t.add_row(row)
  print(t)

def generate_csv(data_row_list, file_name, header):
  with open(file_name, 'w', encoding='UTF8') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    # write the data
    for data_row in data_row_list:
      writer.writerow(data_row)

#aqui precisaremos separar as coisas
#Processa os xmls da pasta passada na env folder_name
#Novo nome: process_xmls_to_csv_course_filter
def process_xmls_to_csv_course_filter(header, course_name_list, folder_name, csv_name, relation):
  final_data_row_list= []
  total_courses = len(course_name_list)
  course_count = 0
  print('Total de cursos para processar: {}'.format(total_courses))
  
  #Inicia o algoritmo que passa cursos para filtrar e gerar as relações
  for course_name in course_name_list:
    course_count = course_count + 1
    percentage = ( course_count/ total_courses ) * 100
    print('Curso atualmente sendo processado: {}'.format(course_name))
    data_row_list = process_all_xml_files(course_name, folder_name, relation)
    final_data_row_list = final_data_row_list + data_row_list
    print('Porcentagem de completar todos os cursos: {}'.format(percentage))

  #Gera CSV
  pretty_print_table(final_data_row_list, header)
  csv_final_name='{}-{}'.format(relation, csv_name)
  generate_csv(final_data_row_list, csv_final_name, header)

#Novo algoritmo: Processa os XMLs apenas uma vez. Pega o curso do campo graduação, pega o ano de conclusão do curso e usa ele no
#processo original, pegando atuações profissionais realizadas após a conclusão de curso.
def process_xmls_to_csv_filterless(header, folder_name, csv_name, relation):
  final_data_row_list= []
  #total_courses = len(course_name_list)
  #course_count = 0
  #print('Total de cursos para processar: {}'.format(total_courses))
  
  #Ao inves de passar curso a curso, faremos uma passagem direto pelos xmls
  #Inicia o algoritmo que passa cursos para filtrar e gerar as relações
  #for course_name in course_name_list:
  #course_count = course_count + 1
  #percentage = ( course_count/ total_courses ) * 100
  #print('Curso atualmente sendo processado: {}'.format(course_name))
  data_row_list = process_all_xml_files_filterless(folder_name, relation)
  final_data_row_list = final_data_row_list + data_row_list
  
  #Precisa ficar mas não tem dados:
  #print('Porcentagem de completar todos os cursos: {}'.format(percentage))

  #Gera CSV
  pretty_print_table(final_data_row_list, header)
  csv_final_name='{}-{}'.format(relation, csv_name)
  generate_csv(final_data_row_list, csv_final_name, header)

csv_header_dict = { 
  "professional_action_after_course_conclusion" : ['nome_completo', 'ano_inicio_curso', 'ano_conclusao_curso', 'nome_curso', 'nome_instituicao_curso' , 'inicio_vinculo', 'nome_instituicao_acao_profissional', 'enquadramento_funcional'],
  "postgrad_after_course_conclusion" : ['nome_completo', 'ano_inicio_curso', 'ano_conclusao_curso', 'nome_curso', 'nome_instituicao_curso' , 'inicio_pos_graduacao', 'conclusao_pos_graduacao', 'tipo_pos_graduacao' ,'nome_instituicao_pos_graduacao', 'nome_curso_pos_graduacao'] 
}

#from course_name_list_simple import course_name_list
from course_name_list_full import course_name_list
#from course_name_list_single import course_name_list

print('Começando a processar todos os xmls')

now = datetime.now()
formatted_date = now.strftime("%Y-%m-%d-time-%H-%M-%S")

csv_name=sys.argv[1]
folder_name=sys.argv[2]
relation=sys.argv[3]

#A esse nivel, estamos escolhendo a relação
#process_xmls_to_csv_course_filter(csv_header_dict[relation], course_name_list, folder_name, csv_name, relation)
process_xmls_to_csv_filterless(csv_header_dict[relation], folder_name, "filterless_{}".format(csv_name), relation)

print()
print('Script executado com sucesso')
sys.exit()

