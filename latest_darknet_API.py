#***************************************************************************
#   NDHU    CSIE                                                           *
#  Author:Aaronace                                                         *
#    2020-2021                                                             *
#  GraduateProject                                                         *
#   Professor:CCC                                                          *
#                                                                          *
#   darknet.py 核心函數：load_network、detect_image draw_boxes bbox2points   *
#   darknet_images.py 核心函數： image_detection,此函數需要修改成輸入圖像        *
#   darknet官方寫的預測圖像輸出依舊為正方形，而非原圖！因此要轉換成原圖               *
#***************************************************************************

import os
import cv2
import numpy as np
import darknet


class Detect:
    def __init__(self, metaPath, configPath, weightPath, gpu_id=0, batch=1):
        '''
        :param metaPath:   ***.data 存儲各種參數
        :param configPath: ***.cfg  網路結構文件
        :param weightPath: ***.weights yolo的權重
        :param batch:      ########此類隻支持batch=1############
        '''
        assert batch == 1, "batch必須為1"
        # 設置gpu_id
        darknet.set_gpu(gpu_id)
        # 網路
        network, class_names, class_colors = darknet.load_network(
            configPath,
            metaPath,
            weightPath,
            batch_size=batch
        )
        self.network = network
        self.class_names = class_names
        self.class_colors = class_colors

    def bbox2point(self, bbox):
        x, y, w, h = bbox
        xmin = x - (w / 2)
        xmax = x + (w / 2)
        ymin = y - (h / 2)
        ymax = y + (h / 2)
        return (xmin, ymin, xmax, ymax)

    def point2bbox(self, point):
        x1, y1, x2, y2 = point
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2
        w = (x2 - x1)
        h = (y2 - y1)
        return (x, y, w, h)

    def image_detection(self, image_bgr, network, class_names, class_colors, thresh=0.25):
        # 判斷輸入圖像是否為3通道
        if len(image_bgr.shape) == 2:
            image_bgr = np.stack([image_bgr] * 3, axis=-1)
        # 獲取原始圖像大小
        orig_h, orig_w = image_bgr.shape[:2]

        width = darknet.network_width(network)
        height = darknet.network_height(network)
        darknet_image = darknet.make_image(width, height, 3)

        # image = cv2.imread(image_path)
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        image_resized = cv2.resize(image_rgb, (width, height), interpolation=cv2.INTER_LINEAR)

        darknet.copy_image_from_bytes(darknet_image, image_resized.tobytes())
        detections = darknet.detect_image(network, class_names, darknet_image, thresh=thresh)
        darknet.free_image(darknet_image)
        '''注意：這裡原始程式碼依舊是608*608，而不是原圖大小，因此我們需要轉換'''
        new_detections = []
        for detection in detections:
            pred_label, pred_conf, (x, y, w, h) = detection
            new_x = x / width * orig_w
            new_y = y / height * orig_h
            new_w = w / width * orig_w
            new_h = h / height * orig_h

            # 可以約束一下
            (x1, y1, x2, y2) = self.bbox2point((new_x, new_y, new_w, new_h))
            x1 = x1 if x1 > 0 else 0
            x2 = x2 if x2 < orig_w else orig_w
            y1 = y1 if y1 > 0 else 0
            y2 = y2 if y2 < orig_h else orig_h

            (new_x, new_y, new_w, new_h) = self.point2bbox((x1, y1, x2, y2))

            new_detections.append((pred_label, pred_conf, (new_x, new_y, new_w, new_h)))
        global size
        image, size = darknet.draw_boxes(new_detections, image_rgb, class_colors)
        img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        return img, new_detections

    def predict_image(self, image_bgr, thresh=0.25, is_show=True, save_path=''):
        '''
        :param image_bgr:  輸入圖像
        :param thresh:     置信度閾值
        :param is_show:   是否將畫框之後的原始圖像返回
        :param save_path: 畫框後的保存路徑, eg='/home/aaa.jpg'
        :return:
        '''
        draw_bbox_image, detections = self.image_detection(image_bgr, self.network, self.class_names, self.class_colors,
                                                           thresh)
        # 輸出座標文件
        file = open("Coordinate.txt", 'w')
        file.write("Objects:\n")
        num = 0
        for label, confidence, bbox in detections:
            x, y, w, h = bbox
            file.write(
                "{}: {}%    (left_x: {:.0f}   top_y:  {:.0f}   width:   {:.0f}   height:  {:.0f} size: {})\n".format(
                    label, confidence, x, y, w, h, size[num]))
            num +=1
        file.close()
        if is_show:
            if save_path:
                cv2.imwrite(save_path, draw_bbox_image)
            return draw_bbox_image
        return detections


def latest_API(detect):
    # 讀取文件夾
    image_root = r'/home/aaronace/Downloads/Project/testimage'
    save_root = r'./output'
    if not os.path.exists(save_root):
        os.makedirs(save_root)
    for name in os.listdir(image_root):
        print(name)
        image = cv2.imread(os.path.join(image_root, name), -1)
        detect.predict_image(image, save_path=os.path.join(save_root, name))
    return 1
