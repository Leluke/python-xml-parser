# python-xml-parser

## Como usar

O script pode ser usado diretamente à partir de um shell rodando o comando:

```
  python main.py <nome-arquivo-csv-para-criar> <nome-pasta-com-xmls> <nome da relação para extrair>


  #Exemplo, queremos exportar para o arquivo "meu-novo-arquivo.csv" e os xsmls estão numa pasta chamada "files-to-process", a extração "professional_action_after_course_conclusion"
  python main.py meu-novo-arquivo.csv files-to-process professional_action_after_course_conclusion

```

## Como rodar em paralelo

Para acelerar o processamento, temos o script parallel_process_files.sh que quebra os arquivos em lotes definidos na hora de rodar o script e paraleliza a execução.

```
  ./parallel_process_files.sh <numero de batches> <nome da pasta> <nome da relação para extrair>

  #Exemplo, queremos processar em paralelo os xsmls que estão numa pasta chamada "files-to-process", usando a extração "professional_action_after_course_conclusion"

  ./parallel_process_files.sh 4 files-to-process professional_action_after_course_conclusion
```

Após a execução do script, uma nova pasta "export" será criada, e dentro dela teremos subpastas para cada execução do script. O nome da pasta tem a data da execução e o horário para facilitar a identificação das execuções

## Lista de extrações disponíveis

* professional_action_after_course_conclusion: Cada linha da tabela representa uma relação profissional que foi começada após a conclusão do curso de graduação indicado na linha
* postgrad_after_course_conclusion: Cada linha da tabela representa uma pós graduação que foi começada após a conclusão do curso de graduação indicado na linha