from decisionTree import Classify as cls

#cofig
max_x = 600+750
min_x = 600
max_y = 270+750
min_y = 270
probability = 80.0

class Coordinate:
    def __init__(self, category, probability):
        self.category = category
        self.probability = probability

    def category(self):
        return self.category

    def probability(self):
        return self.probability

    def x(self):
        return self.x

    def y(self):
        return self.y

    def width(self):
        return self.width

    def height(self):
        return self.height

    def size(self):
        return self.size


def GetPosition(line):
    if (line.find('left_x:')):
        RecognizeItem[len(RecognizeItem) - 1].x = int(line[line.find('left_x:') + 7:line.find('left_x:') + 12])
        # print("x:",int(line[line.find('left_x:')+7:line.find('left_x:')+12]))
    if (line.find('top_y:')):
        RecognizeItem[len(RecognizeItem) - 1].y = int(line[line.find('top_y:') + 7:line.find('top_y:') + 12])
        # print("y:",int(line[line.find('top_y:')+7:line.find('top_y:')+12]))
    if (line.find('width:')):
        RecognizeItem[len(RecognizeItem) - 1].width = int(line[line.find('width:') + 7:line.find('width:') + 12])
        # print("width:",int(line[line.find('width:')+7:line.find('width:')+12]))
    if (line.find('height:')):
        RecognizeItem[len(RecognizeItem) - 1].height = int(line[line.find('height:') + 7:line.find('height:') + 12])
        # print("height:",int(line[line.find('height:')+7:line.find('height:')+12]))
    if (line.find('size:')):
        RecognizeItem[len(RecognizeItem) - 1].size = int(line[line.find('size:') + 7:line.find('size:') + 8])
        # print("size:",int(line[line.find('size:') + 7:line.find('size:') + 8]))


def Classify(line):
    ScrewPosition = line.find('Screw')
    NutPosition = line.find('Nut')

    # 判斷兩個都有辨識到的情況
    if (NutPosition >= 0 and ScrewPosition >= 0):
        RecognizeItem.append(Coordinate('Multi', int(0)))
        GetPosition(line)
        RecognizeItem[len(RecognizeItem) - 1].size = int(0)
    elif (NutPosition == 0):
        if (int(line[line.find('Nut:') + 4:line.find('Nut:') + 7]) >= probability ):
            RecognizeItem.append(Coordinate('Nut', int(line[line.find('Nut:') + 4:line.find('Nut:') + 7])))
            GetPosition(line)
    elif (ScrewPosition == 0):
        if (int(line[line.find('Screw:') + 6:line.find('Screw:') + 9]) >= probability ):
            RecognizeItem.append(Coordinate('Screw', int(line[line.find('Screw:') + 6:line.find('Screw:') + 9])))
            GetPosition(line)


def RecognizeItemPosition():

    global RecognizeItem
    RecognizeItem = []
    file = open("Coordinate.txt", "r")
    for line in file:
        Classify(line)
    file.close()
    for i in RecognizeItem:
        print("Category:   ", i.category)
        print("probability:", i.probability)
        print("x:          ", i.x)
        print("y:          ", i.y)
        print("width:      ", i.width)
        print("height:     ", i.height)
        print("size:       ", i.size)
        print("\n")
    return RecognizeItem

if __name__ == '__main__':
    RecognizeItemPosition()
