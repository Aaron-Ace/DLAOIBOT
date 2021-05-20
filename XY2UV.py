import cv2
import numpy as np

# Perspective Transform
def Dot_Product(org, M):
    result = np.dot(org, M)
    return result

def xy2uv(test_X,test_Y):
    corner = [[0, 0], [0, 0], [0, 0], [0, 0]]
    file = open('pixel_position.ini', 'r')
    for line in file:
        corner[0][0] = int(line[line.find('left_top_x:')+11:line.find('left_top_x:')+14])
        corner[0][1] = int(line[line.find('left_top_y:')+11:line.find('left_top_y:')+14])
        corner[1][0] = int(line[line.find('right_top_x:') + 12:line.find('right_top_x:') + 15])
        corner[1][1] = int(line[line.find('right_top_y:') + 12:line.find('right_top_y:') + 15])
        corner[2][0] = int(line[line.find('left_bottom_x:') + 14:line.find('left_bottom_x:') + 17])
        corner[2][1] = int(line[line.find('left_bottom_y:') + 14:line.find('left_bottom_y:') + 17])
        corner[3][0] = int(line[line.find('right_bottom_x:') + 15:line.find('right_bottom_x:') + 18])
        corner[3][1] = int(line[line.find('right_bottom_y:') + 15:line.find('right_bottom_y:') + 18])
    file.close()
    output=[]
    height, width = 40, 40 #(y, x)
    src_points = np.array([[corner[0][0], corner[0][1]], [corner[1][0], corner[1][1]], [corner[2][0], corner[2][1]], \
                           [corner[3][0], corner[3][1]]],np.float32) #(x, y)
    dst_points = np.array([[-20, -20], [-20, 20], [20, -20], [20, 20]],np.float32) #(x, y)
    M = cv2.getPerspectiveTransform(src_points, dst_points)
    org1 = np.array([corner[0][0], corner[0][1], 1])
    org_test = np.array([test_X, test_Y, 1]) # input the boundindbox center
    final = Dot_Product(org_test, M)-Dot_Product(org1, M)
    print(Dot_Product(org1, M))
    print(Dot_Product(org_test, M))
    output.append(final[0])
    output.append(final[1])
    print("U:{} V:{}".format(output[0],output[1]))

    return output

if __name__ == '__main__':
    xy2uv(430,392)