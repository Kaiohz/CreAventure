import json
def scrapPart(jsonFile,nameSection) -> Any :
    try :
        with open(jsonFile, "r",encoding='utf-8') as f:
            data = json.load(f)
        data = explorer_json(data,nameSection)
        return data
    except json.JSONDecodeError:
        return "Error while opening the json file"
    except FileNotFoundError  :
        return "Any file was found"
    
def explorer_json(data, nameSection, niveau=0, path=None):
    if path is None:
        path = []

    # Dictionnaire pour accumuler les résultats trouvés
    jsonContent = {}

    # Si les données sont un dictionnaire
    if isinstance(data, dict):
        for key, value in data.items():
            # Si la clé correspond à la section recherchée, on l'ajoute à jsonContent
            if key == nameSection:
                if nameSection not in jsonContent:
                    jsonContent[nameSection] = []
                jsonContent[nameSection].append(value)
            
            # Exploration récursive de la valeur
            result = explorer_json(value, nameSection, niveau + 1, path)
            # Fusionner les résultats trouvés dans les sous-sections
            for sub_key, sub_value in result.items():
                if sub_key not in jsonContent:
                    jsonContent[sub_key] = sub_value
                else:
                    jsonContent[sub_key].extend(sub_value)

    # Si les données sont une liste
    elif isinstance(data, list):
        for item in data:
            result = explorer_json(item, nameSection, niveau + 1, path)
            for sub_key, sub_value in result.items():
                if sub_key not in jsonContent:
                    jsonContent[sub_key] = sub_value
                else:
                    jsonContent[sub_key].extend(sub_value)

    return jsonContent
if __name__ == "__main__" :
    jsonFile = "tableau_5.json"
    nameSection = "category"
    value = scrapPart(jsonFile,nameSection)
    print(value)
    value = scrapPart("tets.json","name")
    print(value)
    
        
    
    