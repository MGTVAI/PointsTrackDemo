# coding=utf-8
# points tracing baseline

import cv2
import numpy as np
import sys

'''
    Baseline 通过特征点匹配计算单应性矩形来完成点位跟踪。
'''
class Points_Tracing():
    def __init__(self) :
        self.ratio = 0.85
        self.min_match = 4
        self.sift = cv2.xfeatures2d.SIFT_create()
        self.matcher = cv2.BFMatcher()

    # 单应性矩阵计算
    def get_homography(self,img1,img2):
        # 提取特征点
        kp1, des1 = self.sift.detectAndCompute(img1, None)
        kp2, des2 = self.sift.detectAndCompute(img2, None)
        
        # 匹配
        raw_matches = self.matcher.knnMatch(des1, des2, k=2)
        good_points = []
        good_matches = []
        for m1, m2 in raw_matches:
            if m1.distance < self.ratio * m2.distance:
                good_points.append((m1.trainIdx, m1.queryIdx))
                good_matches.append([m1])
        
        if len(good_points) >= self.min_match:
            image1_kp = np.float32(
                [kp1[i].pt for (_, i) in good_points])
            image2_kp = np.float32(
                [kp2[i].pt for (i, _) in good_points])
            
            H, status = cv2.findHomography(image1_kp, image2_kp, cv2.RANSAC,5.0)
            
            return H
        else:
            return np.eye(3,3)
            
    # 跟踪点位
    def tracing(self,video_path,points_txt,result_txt):
        # 结果列表
        points_results = list()
        
        # 初始单应
        M = np.eye(3,3)
        
        # 加载视频文件
        video_cap = cv2.VideoCapture(video_path)
        
        # 加载目标跟踪点位
        first_points = read_txt(points_txt)
        
        # 读取第一帧
        video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, pre_frame = video_cap.read()
        
        points_results.append((0,first_points))
        
        # 循环
        while video_cap.isOpened():
            
            index = video_cap.get(cv2.CAP_PROP_POS_FRAMES)
            ret, frame = video_cap.read()
            
            if ret == True:
                # 获取相邻两帧单应性矩阵
                H = self.get_homography(pre_frame,frame)
                
                # 计算到首帧的单应性矩阵
                M = np.matmul(H,M) 
                
                # 根据单应性矩阵跟踪目标点位
                dst = cv2.perspectiveTransform(first_points, M)
                
                points_results.append((int(index),dst))
                
                pre_frame = frame

            else:
                break
            
        # 释放cap
        video_cap.release()
        
        # 存储跟踪结果到结果文件
        store_txt(points_results,result_txt)
        
# 读取目标跟踪点位
def read_txt(points_txt):
    points = None
    with open(points_txt,"r") as p:
        points = np.float32(list(map(lambda x: list(map(float,x.split(","))),p.readline().split()[1:]))).reshape(-1, 1, 2)
    return points

# 存储结果 
def store_txt(points_results,result_txt):
    with open(result_txt,"w") as w:
        for result in points_results:
            frame_id = result[0]
            points = result[1]
            a = points.flatten().tolist()
            b = [str(frame_id)]
            b.extend([",".join(list(map(str,a[i:i+2]))) for i in range(0,len(a),2)])
            w.write(" ".join(b)+"\n")        


def main(argv1,argv2,argv3):
    # 跟踪
    Points_Tracing().tracing(argv1,argv2,argv3)
    
'''
    param 1:目标视频文件
    param 2:目标点位文件
    param 3:跟踪点位文件
'''
if __name__ == '__main__':
    try: 
        main(sys.argv[1],sys.argv[2],sys.argv[3])
        #main("baseline.mp4",'target_points.txt','results.txt')
    except IndexError:
        print ("Please input baseline.mp4 , target_points.txt and results.txt: ")
        print ("For example: python baseline.py 'baseline.mp4' 'target_points.txt' 'results.txt'")
    
