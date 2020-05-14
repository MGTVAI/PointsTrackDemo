import cv2
import sys
import numpy as np

'''
    浏览验证跟踪结果在视频中的跟踪效果
'''
def main(video_path,results_txt):
    # Create a VideoCapture object and read from input file
    cap = cv2.VideoCapture(video_path) 
    
    points_lines = list()
    with open(results_txt,"r") as f:
        points_lines = f.readlines()

    if (cap.isOpened()== False):
         print("Error opening video stream or file")

    ind = 0
    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            # Draw rectangle
            line = points_lines[ind]
            pt_tuple = line.strip('\n').split()
            pt_1 = list(map(int,list(map(float, pt_tuple[1].split(",")))))
            pt_2 = list(map(int,list(map(float, pt_tuple[2].split(",")))))
            pt_3 = list(map(int,list(map(float, pt_tuple[3].split(",")))))
            pt_4 = list(map(int,list(map(float, pt_tuple[4].split(",")))))
            pts = np.array([[pt_1,pt_2,pt_3,pt_4]], dtype = np.int32)
            cv2.fillPoly(frame, pts, 255) 
            # Display videp
            cv2.imshow('Preview',frame)
            
            # flush
            cv2.waitKey(10)
            ind += 1
            
            # q quit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

            
        # Break the loop
        else:
            break
    
    if cv2.waitKey(0) == 27:     
        cv2.destroyAllWindows() 
            
    cap.release()

   
'''
    param 1：目标视频文件
    param 1：跟踪点位文件
'''    
if __name__ == '__main__':
    try: 
        main(sys.argv[1],sys.argv[2])
        #main("baseline.mp4",'results.txt')
    except IndexError:
        print ("Please input baseline.mp4 , results.txt: ")
        print ("For example: python preview.py 'baseline.mp4' 'results.txt'")