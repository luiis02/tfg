from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
the_model = 'mrm8488/distill-bert-base-spanish-wwm-cased-finetuned-spa-squad2-es'
tokenizer = AutoTokenizer.from_pretrained(the_model, do_lower_case=False)
model = AutoModelForQuestionAnswering.from_pretrained(the_model)
from textwrap import wrap

contexto = '''
    Te llamas Crubo.Eres Crubo un asistente virtual que ayudara a responder dudas a los clientes de la aplicación
    Para crear un menu nuevo los clientes deben ir a la página de inicio, escoger un nombre, un indicie y un estado.
    El índice significa su orden, es decir el índice 1 aparecera antes a los clientes que el indice 3.
    El estado significa si la carta esta encendida o apagada, si esta apagada los clientes no podran verla.
    Para atender a los clientes debes pulsar en el boton de atender, alli te apareceran los pedidos de los clientes. Una vez dentro 
    puedes filtrar por categorias. En caso de que el cliente se haya equivocado al realizar el pedido puedes eliminarlo. Es importante marcar un pedido como
    acabado una vez que lo hayas entregado al cliente, ya que se utilizan para tomar estadísticas.

    Para crear una sección o un plato debes de hacer lo mismo que para crear un menu, solo que desde dentro del menu.

    Para obtener los qr de las mesas, solo pulsa en mesas, crea las mesas que necesites y descargar sus qr. No debes de perderlos, ya que desde ese codigo podran hacer pedidos, 
    En caso de perder algun qr puedes eliminarlo desde la palicación y crear una nueva mesa.

    Las recomendaciones por IA sirven para ayudar a los clientes a elegir que plato quieren, en base a sus gustos. Potenciando de estas maneras tus ventas. Al activar las recomendaciones por IA
    se ignora el indice que hayas puesto en los menus, ya que se mostraran en base a los gustos de los clientes. Ademas en tu caso se mostraran los platos ordenados por los gustos de los clientes.
    
    Ahora en base a esto responde:
'''


pregunta = input("Hazme una pregunta:")
encode = tokenizer.encode_plus(pregunta, contexto, return_tensors='pt')
input_ids = encode['input_ids'].tolist()
tokens = tokenizer.convert_ids_to_tokens(input_ids[0])
for id, token in zip(input_ids[0], tokens):
  print('{:<12} {:>6}'.format(token, id))
  print('')
nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)
salida = nlp({'question':pregunta, 'context':contexto})
print(salida)
pregunta = input("Hazme una pregunta:")




