import xml.etree.ElementTree as ET
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
  #Checa se concluiu ou não o curso, se sim retorna o numero do ano, se não retorna falso
  if grad.attrib['ANO-DE-CONCLUSAO'] == "":
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

def process_xml(root_object, course_name):
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

def process_xml_file(file_name, course_name):
  file = file_name
  tree = ET.parse(file)
  root = tree.getroot()
  return process_xml(root, course_name)

def process_all_xml_files(course_name, folder_name):
  path = './' + folder_name
  file_name_list = [f for f in listdir(path) if isfile(join(path, f))]
  final_data_row_list = []
  data_row_list = []

  for file_name in file_name_list:
    file_path = folder_name + '/' + file_name
    data_row_list = process_xml_file(file_path, course_name)
    if data_row_list == []:
      pass
    else:
      final_data_row_list = final_data_row_list + data_row_list

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
def process_xmls_to_csv(header, course_name_list, folder_name):
  final_data_row_list= []
  for course_name in course_name_list:
    data_row_list = process_all_xml_files(course_name, folder_name)
    final_data_row_list = final_data_row_list + data_row_list

  pretty_print_table(final_data_row_list, header)
  generate_csv(final_data_row_list, 'teste.csv', header)

csv_header = ['nome_completo', 'ano_conclusao_curso', 'nome_curso', 'inicio_vinculo', 'nome_instituicao', 'enquadramento_funcional']
course_name_list = ['Biblioteconomia', 'bibliotecomia', 'Biblioteconimia', 'Biblioteonomia', 'Bilioteconomia']
folder_name = 'files-to-process'

print('Começando a processar todos os xmls')
process_xmls_to_csv(csv_header, course_name_list, folder_name)

print()
print('Script executado com sucesso')
sys.exit()

