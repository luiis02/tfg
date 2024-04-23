from gpt4all import GPT4All
import json 
model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")
model = GPT4All(model_name='orca-mini-3b-gguf2-q4_0.gguf')


def start(entrada):
    #generalText= "Texto: "
    #generalText+= entrada
    #generalText= "Dado el texto anterior responde con este fomato {numero, probabilidad de acierto} Numeros a escoger:\n 1. Pedir un camarero presencial por algun problema. \n 2. Pagar todo lo consumido o pagar la cuenta \n 3. Hacer un pedido al local."
    #generalText+= " . Responde solo con el número de la opción correcta, sin explicar nada: \n 1. Pedir un camarero presencial por algun problema. \n 2. Pagar todo lo consumido. \n 3. Hacer un pedido al local. "
    generalText= "Resume this text in less than 5 words:" + entrada
    with model.chat_session():
        response1 = model.generate(prompt=generalText, temp=0.7)        
        a = json.dumps(model.current_chat_session, indent=4)
        a_json = json.loads(a)
        last_content = a_json[-1]["content"]
        generalText= "classify with 1. Create a order 2. Call to a waiter 3. Bring to the user the bill.  the following text: " + last_content + ".\n\nAnswer with the number of the option that you think is correct."
        response2 = model.generate(prompt=generalText, temp=0.7)
        print(response2)    

start("Please bring me the bill")
