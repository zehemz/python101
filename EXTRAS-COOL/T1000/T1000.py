import hashlib

def handShakeDecode(fullDocument):
    elementsString = fullDocument.split(";")
    robots = []
    for element in elementsString:
        aux = element.strip("[]").split(",")
        robots.append({"name": aux[0], "key": aux[2]})
    return robots

if __name__ == "__main__":

    mFile = open("handshakes.lst", "r")
    robots = handShakeDecode(mFile.read())
    mFile.close()
    print(robots)
    fileWords = open("Spanish.dic", "r")
    for line in fileWords:
        print(line)
        coded = hashlib.sha1(line.replace('\n', '').encode("utf-8")).hexdigest()
        #for element in robots:
        #    if coded in element["key"]:
        #        element["decoded"] = line
        #        print(element["name"]+"-"+element["decoded"])
