import json
def scrapPart(jsonFile,nameSection) :
    try :
        with open(jsonFile, "r") as f:
            data = json.load(f)
            
    except :
        print("Error while opening the json file")
        
    
    