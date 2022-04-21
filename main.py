import xml.etree.ElementTree as ET
from prettytable import PrettyTable
import sys

import csv  

tree = ET.parse('1539390812340093.xml')
root = tree.getroot()

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

def create_data_row(full_name, grad_year, action, bond):
  data_row = [full_name, grad_year, bond.attrib['ANO-INICIO'], action.attrib['NOME-INSTITUICAO'], bond.attrib['OUTRO-ENQUADRAMENTO-FUNCIONAL-INFORMADO']]
  return data_row


def process_xml(root_object):
  if is_course(root_object, "Biblioteconomia"):
    t = PrettyTable(header)
    full_name = get_name(root_object)
    conclusion_year = get_course_grad_conclusion_year(root_object, "Biblioteconomia")
    professional_action_list = get_professional_action_list(root_object)
    print("Ano de conclusão em Biblioteconomia: " + conclusion_year)
    print()
    data_rows_list = []
    action_bond_list = get_action_bond_list_from_date(professional_action_list, conclusion_year)
    for action_bond_pair in action_bond_list:
      #pretty_print_action_bond_pair(action_bond_pair)
      #print()
      for bond in action_bond_pair['bond_list']:
        data_row = create_data_row(full_name, conclusion_year, action_bond_pair['action'], bond)
        data_rows_list.append(data_row)
        t.add_row(data_row)
        print(data_row)

  print(t)

def process_all_xml_files(file_list):

file_list = 
header = ['nome_completo', 'ano_conclusao', 'inicio_vinculo', 'nome_instituição', 'enquadramento_funcional']
process_xml(root)
sys.exit()



with open('values.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    # write the data
    writer.writerow(data)