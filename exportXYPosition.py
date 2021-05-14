'''
注釋：
    author is Aaronace
    由於最新版本的darknet將images和video預測分開了，並不是很符合自己的額需求，
    因此參考darknet_images.py修改成屬於自己的預測函數
注：
    darknet.py 核心函數：load_network、detect_image draw_boxes bbox2points
    darknet_images.py 核心函數： image_detection,此函數需要修改成輸入圖像
    darknet官方寫的預測圖像輸出依舊為正方形，而非原圖！因此要轉換成原圖
'''
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

        image = darknet.draw_boxes(new_detections, image_rgb, class_colors)
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
        filename = str(save_path) + ".txt"
        file = open(filename , 'w')
        file.write("Objects:\n")
        for label, confidence, bbox in detections:
            x, y, w, h = bbox
            file.write(
                "{}: {}%    (left_x: {:.0f}   top_y:  {:.0f}   width:   {:.0f}   height:  {:.0f})\n".format(label,
                                                                                                            confidence,
                                                                                                            x, y, w, h))
        file.close()
        if is_show:
            if save_path:
                cv2.imwrite(save_path, draw_bbox_image)
            return draw_bbox_image
        return detections





def latest_API():
    # gpu 通過環境變量設置

    detect = Detect(metaPath=r'./cfg/obj.data',
                    configPath=r'./cfg/yolo-obj.cfg',
                    weightPath=r'./backup/yolo-obj_last.weights',
                    gpu_id=0)

    # 讀取單張圖像
    # image_path = r'/home/aa.jpg'
    # image = cv2.imread(image_path, -1)
    # draw_bbox_image = detect.predict_image(image, save_path='./pred.jpg')

    # 讀取文件夾


    image_root = r'./testimage'
    save_root = r'./output'

    if not os.path.exists(save_root):
        os.makedirs(save_root)
    for name in os.listdir(image_root):
        print(name)
        image = cv2.imread(os.path.join(image_root, name), -1)
        draw_bbox_image = detect.predict_image(image, save_path=os.path.join(save_root, name))

    # del detect
    # 讀取視頻
    # video_path = r'/home/aaronace/Downloads/darknet_L4/test.mp4'
    # video_save_path = r'/home/20200915_3_pred.mp4'
    # cap = cv2.VideoCapture(video_path)
    # # 獲取視頻的fps， width height
    # fps = int(cap.get(cv2.CAP_PROP_FPS))
    # width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # print(count)
    # # 創建視頻
    # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # # fourcc = cv2.VideoWriter_fourcc('I', '4', '2', '0')
    # video_writer = cv2.VideoWriter(video_save_path, fourcc=fourcc, fps=fps, frameSize=(width,height))
    # ret, frame = cap.read()  # ret表示下一幀還有沒有 有為True
    # while ret:
    #     # 預測每一幀
    #     pred = detect.predict_image(frame)
    #     video_writer.write(pred)
    #     cv2.waitKey(fps)
    #     # 讀取下一幀
    #     ret, frame = cap.read()
    #     print(ret)
    # cap.release()
    # cv2.destroyAllWindows()


    return 1

if __name__ == '__main__':
    latest_API()
