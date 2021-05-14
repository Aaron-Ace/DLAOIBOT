# 植基於深度學習之自動光學檢測與機械手臂自動控制 
![image](https://github.com/Aaron-Ace/DLAOIBOT/blob/main/resource/Cover.jpg)

## 前言
* 在台灣工廠勞動力短缺以及人事成本高昂等因素下，越來越多工廠轉型發展自動化，從產品的生產、組裝、包裝到品管，一整條的流水線，都已漸漸朝自動化作業努力，期能藉此減少人力成本外，並提昇生產效能及生產品質，以提高產業競爭力。但許多自動化的技術基礎目前仍有一定瓶頸與門檻，且工廠生產線上的產品不同，技術通常就須面對不同的挑戰，無法用同一套技術施作在所有生產線上，技術開者仍然要針對實際狀況做不同程度的修正調校，所幸近年來深度學習技術發展迅速，尤其在電腦視覺的應用上更有許多令人矚目的突破，加上其經常可以端到端(End-to-End)的方式運作，只須借助大量訓練資料的收集即可建立有效的智慧偵測與辨識模型，並不需要設計者運用太多專業知識於資料的處理與模型的設計，可大幅降低系統開者專業背景的需求門檻，即使要運用技術於不同產品的生產線，通常也只需收集新訓練資料後再追加訓練或調校模型即可，因此，系統的更新與延伸擴充成本也相對容易且成本較低。
本計畫設定以五金零件工廠的生產線自動化為應用情境，特別針對一般螺絲釘的生產線運作為標的來進行軟硬體技術開發與整合。
---
## 計畫摘要
* 本計畫設定以五金零件工廠的生產線自動化為應用情境，特別針對一般螺絲的生產線運作為標的來進行軟硬體技術開發與整合。本計畫以三種大小的螺絲與螺帽為生產之元件，我們將開發以深度學習技術為基礎的螺絲及螺帽的定位與辨識技術，讓電腦透過攝影機監控生產線工作臺上擺放的不同尺寸與不同置放角度與方向的螺釘與螺帽進行自動定位，並且能分辨出是何種尺寸的螺釘或是螺帽，完成定位與分辨後，接著就控制機械手臂從工作臺上精準夾出所指定尺寸的螺釘或螺帽。為此，本計畫將自行以3D列印機製作與組裝機械手臂組件進行組裝，並利用Arduino搭配控制電路的設計來製作一具實際可操控的六軸機械手臂。
---
## 流程簡析
* Step 1 : **拍攝圖片**  
利用網路攝影機拍取平台畫面，將圖片儲存至電腦。  
* Step 2 : **Yolo**  
將儲存的圖片放進Yolo模型，讓模型抓取特徵，分辨出螺絲或螺帽。  
* Step 3 : **辨識物件**  
利用Yolo取得辨識出來的位置座標以及物件bouning box的長和寬  
* Step 4 : **分類器**  
利用二元決定樹(binary decision tree)的方法製作分類器。   
* Step 5 : **辨識物件大小**  
利用分類器辨識物件的大小，改善Yolo無法辨識物體大小的缺陷。  
* Step 6 : **預測馬達角度**  
利用神經網路K-Nearest Neighbors(KNN)，根據物體座標去預測6個軸的馬達角度。   
* Step 7 : **夾取物件**  
將分類器和神經網路得出的參數傳入Arduino，控制夾取物件並且依據大小分類。 
* Step 8 : **重複直到完成**  
回到Step 1直到畫面上再無物件存在。  
---
## 流程簡圖
![image](https://github.com/Aaron-Ace/DLAOIBOT/blob/main/resource/Process%20Chart.png)  
---
## 開發系統
### 硬體
*	Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz
*	64 位元作業系統， x64 型處理器
*	GEFORCE GTX 1080 Ti
*	Arduino Uno 開發板
*	3D列印機械手臂
### 軟體
* Ubuntu 20.04
* Python Language
*	C/C++ Language
*	Opencv
*	Sklearn
---
## 技術應用  
### Yolo  
Yolo是一種靠CNN實現的物件識別演算法，利用CNN來同時預測多個bounding-box並且針對每一個box來計算物體的機率，而在訓練的時候也是直接拿整張圖丟到NN中來訓練，這樣end-to-end的演算法可以避免傳統object detection的必須分開訓練的缺點，並且大幅加快運算速度。  
Yolo 參考資料 : https://github.com/AlexeyAB  
CNN 參考資料 : https://medium.com/jameslearningnote/%E8%B3%87%E6%96%99%E5%88%86%E6%9E%90-%E6%A9%9F%E5%99%A8%E5%AD%B8%E7%BF%92-%E7%AC%AC5-1%E8%AC%9B-%E5%8D%B7%E7%A9%8D%E7%A5%9E%E7%B6%93%E7%B6%B2%E7%B5%A1%E4%BB%8B%E7%B4%B9-convolutional-neural-network-4f8249d65d4f  
#### Labelimg  
Yolo是屬於機器學習領域當中監督式學習的一種，所以所有訓練資料都必須Label，底下連結為我們這次Label所使用的工具。  
連結 : https://github.com/tzutalin/labelImg  
#### 訓練結果
![image](https://github.com/Aaron-Ace/DLAOIBOT/blob/main/resource/Yolo_Demo.jpg)  

---
### 二元決策樹(Binary Decision Tree)
我們將Yolo辨識出物件的BoundingBox的長和寬，放進此Binary Decision Tree中，來辨別此物件的大小。
* **Requirement**
  * **csv**
  * **Pandas**
  * **Sklearn**
  * **Numpy**  

程式碼 : https://github.com/Aaron-Ace/DLAOIBOT/blob/main/decisionTree.py  
binary decision tree 參考資料 : https://medium.com/@Packt_Pub/binary-decision-trees-1ec94cfed208  

---
### Arduino  
Arduino是一套可以將Arduino的編譯環境中已編譯的程式碼燒錄至Arduino開發板，開發板再將電子訊號傳給伺服馬達，達成我們要的效果，藉此來驅動機器手臂。  
Arduino 參考資料 : https://blog.jmaker.com.tw/arduino-tutorials-1/
* **Requirement**  (Arduino的環境是建立在Anaconda中，故環境安裝皆採用conda install)  
Anaconda官網 : https://www.anaconda.com/products/individual
  * **Python*
  * **Pyserial**    
```
conda create -n arduino python
``` 
```
conda install pyserial
```  
* **Pycharm**  
Arduino的編譯環境與Pycharm之間資料的傳輸需要以Pyserial為媒介，需再Python的編譯環境前加上標頭檔。  
Pycharm官網 : https://www.jetbrains.com/pycharm/
```python
import serial
```  
程式碼 : https://github.com/Aaron-Ace/DLAOIBOT/blob/main/armcontrol.py
* **Arduino IDE**   
記得要加入此標頭檔，才能與Pycharm傳輸資料。  
```c
#include <SoftwareSerial.h>
```  
此標頭檔為伺服馬達所需。  
```c
#include <Servo.h>
``` 
---
### Attend Regressor
我們用此神經網路模型，將圖片經過Yolo模型所得出的物件位置(x, y)後並採用Perspective Transform的方式，轉換成平台上的座標(u, v)，  
將此(u, v)放入神經網路中，得出機器手臂的6個軸角度。  
* **Requirement**  
  * **Python**  
  * **Numpy**  
  * **Opencv**
  * **Pandas**
  * **Tensorflow**  
* **Perspective Transform 透視轉換**  
程式碼 : https://github.com/Aaron-Ace/DLAOIBOT/blob/main/XY2UV.py 
Perspective Transform 可以將圖片中任意四點，依此為參考點重新校正成矩形。  
```python
src_points = np.array([[25, 39], [711, 38], [27, 715], [706, 714]],np.float32) #(x, y)
dst_points = np.array([[-20, -20], [-20, 20], [20, -20], [20, 20]],np.float32) #(x, y)
```
src_points為參考點(可以根據需求自行調整)，校正成dst_points為需要的座標點。  
```python
M = cv2.getPerspectiveTransform(src_points, dst_points)
```
使用此函數，得出的M即為轉換矩陣。  
Perspective Transform 參考資料 : https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/  
* **Attend Regressor模型**  
程式碼 : https://github.com/Aaron-Ace/DLAOIBOT/tree/main/MLP  
資料蒐集約250筆，其中訓練資料約200筆，測資約50筆。  
  
---
### 機器手臂 RobotArm
機器手臂為自己製作，先用3D印表機印出需要的零件，在進行組裝。  
機器手臂設計圖 : https://github.com/Aaron-Ace/DLAOIBOT/tree/main/RoboticArm3DModel  
3D印表機規格 : https://www.3dprow.com/products/snapmaker-20-a250  
機器手臂控制程式碼 : https://github.com/Aaron-Ace/DLAOIBOT/blob/main/ArduinoCode/ArduinoCode.ino 

---
## Usage
在command下載 :   
```
https://github.com/Aaron-Ace/DLAOIBOT.git
```
執行Main Program
```
python main.py
```
利用GUI執行Main Program
```
python GUI.py
```
---
# 成果展示
* **影片連結** : https://youtu.be/YGjaYCNhIYg  
* **平台展示**
![image](https://github.com/Aaron-Ace/DLAOIBOT/blob/main/resource/Platform.png)
