import cv2

class camera:
    def __init__(self,dev=0,proc_func=None,output=None):
        self.dev=dev
        self.proc=proc_func
    
    def main_loop(self):
        self.cap = cv2.VideoCapture(0)
        while self.cap.isOpened():
            success, frame = self.cap.read()
            if not success:
                break
            if(self.proc!=None):frame = self.proc(frame)
            
            cv2.imshow('ASL recognition', frame)

            if cv2.waitKey(1) in [ord('q'),27]: # 按键盘上的q或esc退出（在英文输入法下）
                break
        self.cap.release()