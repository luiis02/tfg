import os,random,json,torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
#from src.chatbot.generate import generaJSON
from generate import generaJSON
#from src.database.dbcontroller import DBController
from dbcontroller import DBController

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

intents = generaJSON()

data_dir = os.path.join(os.path.dirname(__file__))
FILE = os.path.join(data_dir, 'chatdata.pth')
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()
bot_name = "iris-NLP"

def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    print(prob.item())
    if prob.item() > 0.7:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])
    return "No te he entendido. Que querias..."

def reentrena(frase):
    val = input("Te ha sido de ayuda? (S/N):")
    bd = DBController()
    bd.connect()
    if val == "S":
        bd.execute_query("UPDATE intents set indice_apoyo=indice_apoyo+1 where texto=%s", (frase,))
    else:
        numero = input("Cual de estas categoria se ajusta más a su necesidad? \n1. Saludar  \n2. Solicitar un camarero \n3. Hacer un pedido\n4. Pagar\n")
        print("Categoria: ",numero, "Frase: ",frase)
        if numero == "1": categoria = "saludos"
        if numero == "2": categoria = "camarero"
        if numero == "3": categoria = "pedir"
        if numero == "4": categoria = "pagar"
        bd.execute_query("INSERT INTO intents (indice_apoyo, tag, Tipo, Texto) VALUES (2, %s,0, %s)", (categoria,frase,))
    print("Gracias por su respuesta, estamos reentrenando el modelo para mejorar su experiencia")

def chatbot_mini():
    print("Chateemos! (pulsa 'quit' para cerrar el chatbot)")
    while True:
        sentence = input("You: ")
        if sentence == "quit":
            break
        resp = get_response(sentence)
        print(resp)
        aleatorio = random.randint(0, 10)
        if aleatorio == 9:
            reentrena(sentence)

def chatbot_mini_asincrono(sentence):
    resp = get_response(sentence)
    print(resp)
    aleatorio = random.randint(0, 10)
    if aleatorio == 9:
        reentrena(sentence)
    return resp

chatbot_mini_asincrono("Me preparas una cocacola y tres gintonics")

#chatbot_mini()