import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def Dot_Product(org, M):
    result = np.dot(org, M)
    #result[0] = round(result[0] - 2.33)
    #result[1] = round(result[1] - 1.51)
    return result

def xy2uv(test_X,test_Y):

    #config
    height, width = 40, 40 #(y, x)
    #test_X,test_Y = 367,373

    src_points = np.array([[35, 42], [711, 41], [39, 758], [707, 707]],np.float32) #(x, y)
    dst_points = np.array([[-20, -20], [-20, 20], [20, -20], [20, 20]],np.float32) #(x, y)

    M = cv2.getPerspectiveTransform(src_points, dst_points)

    org1 = np.array([35, 42, 1])
    period = Dot_Product(org1, M)
    org_test = np.array([test_X, test_Y, 1])
    orginal = Dot_Product(org_test,M)

    output = orginal-period
    print(period)
    print(orginal)

    print("U:{} V:{}".format(output[0],output[1]))
    return output

if __name__ == '__main__':
    xy2uv(367,373)
