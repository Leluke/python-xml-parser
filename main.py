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

def get_graduation_list(root_object):
  grad_list = root_object.findall("./DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/GRADUACAO")
  return grad_list

def is_course(root_object, course_name):
  grads_to_check = get_graduation_list(root_object)
  for grad in grads_to_check:
    #print(grad.attrib['NOME-CURSO'])
    if course_name in grad.attrib['NOME-CURSO']:
      return True  
  return False

def get_course_grad_elem(root_object, course_name):
  grads_to_check = get_graduation_list(root_object)
  for grad in grads_to_check:
    if course_name in grad.attrib['NOME-CURSO']:
      return grad

def get_grad_conclusion_year(grad):
  if 'ANO-DE-CONCLUSAO' not in grad.attrib:
    print ('Não tem campo ANO-DE-CONCLUSAO')
    return "not-graduated"
  elif grad.attrib['ANO-DE-CONCLUSAO'] == "":
    return "not-graduated"
  else:
    return grad.attrib['ANO-DE-CONCLUSAO']

def get_course_grad_conclusion_year(root_object, course_name):
  course_grad_elem = get_course_grad_elem(root_object, course_name)
  conclusion_year = get_grad_conclusion_year(course_grad_elem)
  return conclusion_year

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
def create_data_row(full_name, grad_year, course_name, action, bond):
  data_row = [full_name, grad_year, course_name, bond.attrib['ANO-INICIO'], action.attrib['NOME-INSTITUICAO'], bond.attrib['OUTRO-ENQUADRAMENTO-FUNCIONAL-INFORMADO']]
  return data_row

def get_data_row_relation_action_bond(root_object, course_name):
  data_rows_list = []
  if is_course(root_object, course_name):
    full_name = get_name(root_object)
    conclusion_year = get_course_grad_conclusion_year(root_object, course_name)
    professional_action_list = get_professional_action_list(root_object)
    action_bond_list = get_action_bond_list_from_date(professional_action_list, conclusion_year)
    for action_bond_pair in action_bond_list:
      for bond in action_bond_pair['bond_list']:
        data_row = create_data_row(full_name, conclusion_year, course_name, action_bond_pair['action'], bond)
        data_rows_list.append(data_row)
  return data_rows_list
  
def process_xml(root_object, course_name, relation):
  if relation == "action_bond":
    data_rows_list = get_data_row_relation_action_bond(root_object, course_name)
  else:
    print("Nenhuma extração identificada com o tipo passado: {}".format(relation))
    data_rows_list = []
  return data_rows_list

def process_xml_file(file_name, course_name, relation):
  file = file_name
  tree = ET.parse(file)
  root = tree.getroot()
  return process_xml(root, course_name, relation)

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

#Processa os xmls da pasta passada na env folder_name
def process_xmls_to_csv(header, course_name_list, folder_name, csv_name, relation):
  final_data_row_list= []
  total_courses = len(course_name_list)
  course_count = 0
  print('Total de cursos para processar: {}'.format(total_courses))
  
  for course_name in course_name_list:
    course_count = course_count + 1
    percentage = ( course_count/ total_courses ) * 100
    print('Curso atualmente sendo processado: {}'.format(course_name))
    data_row_list = process_all_xml_files(course_name, folder_name, relation)
    final_data_row_list = final_data_row_list + data_row_list
    print('Porcentagem de completar todos os cursos: {}'.format(percentage))

  pretty_print_table(final_data_row_list, header)
  csv_final_name='{}-{}'.format(relation, csv_name)
  generate_csv(final_data_row_list, csv_final_name, header)

csv_header = ['nome_completo', 'ano_conclusao_curso', 'nome_curso', 'inicio_vinculo', 'nome_instituicao', 'enquadramento_funcional']

#from course_name_list_simple import course_name_list
#from course_name_list_full import course_name_list
from course_name_list_single import course_name_list

print('Começando a processar todos os xmls')

now = datetime.now()
formatted_date = now.strftime("%Y-%m-%d-time-%H-%M-%S")

csv_name=sys.argv[1]
folder_name=sys.argv[2]
relation=sys.argv[3]

process_xmls_to_csv(csv_header, course_name_list, folder_name, csv_name, relation)

print()
print('Script executado com sucesso')
sys.exit()

