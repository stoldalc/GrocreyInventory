#Libraries
import json
import requests


#Objects

class Item(object):
    UPC = 0
    title = ""
    quantity = 0

    # The class "constructor" - It's actually an initializer 
    def __init__(self, UPC, title, quantity):
        self.UPC = UPC
        self.title = title
        self.quantity = quantity




inventory = []

dictionaryBuffer = []



def inventorySearch(upc):
    
    global inventory
    position = 0

    for i in range(len(inventory)):

        if inventory[i].UPC == upc:
            position = i
            return True,position

    return False,-1


def dictionarySearch(upc):

    global dictionaryBuffer
    position = 0

    for i in range(len(dictionaryBuffer)):

        if dictionaryBuffer[i].UPC == upc:
            position = i
            return True,position

    return False,-1

def printInventory():

    global inventory

    if len(inventory) > 0:
        for item in inventory:
            print("Title: " + item.title + " UPC: " + str(item.UPC) + " Quantity: " + str(item.quantity))
    else:
        print("NOTHING IN INVENTORY")


#In process of creating function of printing inverntory and dictionary to file
def save2File():

    global inventory
    global dictionaryBuffer

    inventoryFileName = "inventory.txt"
    dictionaryFileName = "dictionary.txt"


    inventoryFile = open(inventoryFileName,"w+")
    
    for item in inventory:
        bufferStr = item.title + " , " + str(item.UPC) + " , " + str(item.quantity) + "\n"
        inventoryFile.write(bufferStr)


def itemScannedIn(upc):

    #global includes
    global inventory
    global dictionaryBuffer

    #Does the UPC Exist within the inventory already
    searchResult = inventorySearch(upc)

    #Yes
    if searchResult[0] == True:
        #Increase the quantity of the object
        inventory[searchResult[1]].quantity = inventory[searchResult[1]].quantity + 1

    #No 
    elif searchResult[0] == False:
        #Check if the item is in the local dictionary

        dictionaryResults = dictionarySearch(upc)

        if dictionaryResults[0] == True:
            print("DICTIONARY CALLED")

            #Create a new object
            newItem = Item(upc,dictionaryBuffer[dictionaryResults[1]].title,1)
            inventory.append(newItem)

        #If the item is not in the local dictionary
        else:
            print("API CALLED")
            #Check if the UPC for the new item is real
            requestURL = "https://api.upcitemdb.com/prod/trial/lookup?upc=" + str(upc)

            response = requests.get(requestURL)
            responseCode = response.status_code

            if responseCode == 200:

                #Get title from API call
                response = response.json()

                items = response['items']

                title = items[0]['title']

                #Create a new object
                newItem = Item(upc,title,1)

                inventory.append(newItem)
                dictionaryBuffer.append(newItem)



#Scanning out an inventory item
def itemScannedOut(upc):

    global inventory

    #Search the inventory list for the scanned item
    searchResult = inventorySearch(upc)

    #If the item is not in the inventory list
    if searchResult[0] == False:
        print("ITEM NOT FOUND IN CURRENT INVENTORY")
    elif searchResult[0] == True:
        
        #Reduce the quantity of that item by one
        inventory[searchResult[1]].quantity = inventory[searchResult[1]].quantity - 1

        #If the quantity of that item is now 0 remove it from the inventory
        if inventory[searchResult[1]].quantity == 0:
            inventory.pop(searchResult[1])


#Testing

print("-Inventory")
printInventory()

print("Adding UPC: 644135217935  Title: AXE Body Spray for Men Gold 4 Oz")
itemScannedIn(644135217935)

print("-Inventory")
printInventory()

print("Adding a second UPC: 644135217935  Title: AXE Body Spray for Men Gold 4 Oz")
itemScannedIn(644135217935)

print("-Inventory")
printInventory() 

print("Removing first UPC: 644135217935  Title: AXE Body Spray for Men Gold 4 Oz")
itemScannedOut(644135217935)

print("-Inventory")
printInventory() 

print("Removing second UPC: 644135217935  Title: AXE Body Spray for Men Gold 4 Oz")
itemScannedOut(644135217935)

print("-Inventory")
printInventory() 

save2File()

