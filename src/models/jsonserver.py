import json

def modeloJSON(titulo, valor=None):
    with open('config.json', 'r+') as f:
        config = json.load(f)

        if valor is not None:
            config[titulo] = valor
            f.seek(0)
            json.dump(config, f, indent=4)
            f.truncate()
        return config.get(titulo)
