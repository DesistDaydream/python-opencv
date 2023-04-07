import cv2

# 视频的处理本质上与图片的处理是一样的，只不过视频是由一帧一帧的图片组成的。
# 所以视频处理本质上就是对每一帧图片进行处理，然后将处理后的图片组合成视频。


# 从摄像头捕获图片
def CapturePictureFromCamera(cap):
    # 读取当前帧，即拍照。
    # 返回值是一个 bool 和一个 cv::Mat 对象，ret 为 True 时表示读取成功
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        exit()

    # 后续的处理本质上就是处理 cv::Mat 对象，跟 image_handling.py 中的内容一样
    # 只不过这里的 cv::Mat 对象是从摄像头中读取的，而不是从文件中读取的
    cv2.imshow("Video Frame", frame)

    if cv2.waitKey(0) == ord("s"):
        cv2.imwrite("images/picture_from_camera.jpg", frame)


# 从摄像头捕获视频
def CaptureVideoFromCamera(cap):
    # 通过一个循环来捕获每一帧，然后在逐一显示捕获到的每一帧，这样就形成了视频。
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # 可以在显示之前处理捕获到的帧，这里是将图片转为灰色
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 显示当前帧。这里是在一个 while 循环中，所以每一帧都会显示，连起来就形成了视频
        cv2.imshow("frame", gray)
        if cv2.waitKey(1) == ord("q"):
            break


# 保存视频
def SavingVideo(cap):
    # 定义视频编解码器，由 4 字节代码表示。
    fourcc = cv2.VideoWriter_fourcc(*"XVID")

    # 使用 FOURCC 创建 VideoWriter 对象。
    # 第一个参数是输出文件名，第二个参数是编解码器，第三个参数是帧率，第四个参数是帧大小
    out = cv2.VideoWriter("output.avi", fourcc, 20.0, (640, 480))

    # 除了 while True 的形式，还可以通过
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # 将帧写入 out
        out.write(frame)

        cv2.imshow("frame", frame)
        if cv2.waitKey(1) == ord("q"):
            break

    out.release()


# 从文件播放视频
def PlayingVideoFromFile():
    cap = cv2.VideoCapture("output.avi")
    while cap.isOpened():
        ret, frame = cap.read()

        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        cv2.imshow("frame", frame)

        if cv2.waitKey(1) == ord("q"):
            break


# 获取、设置视频属性
def ViedeProperty(cap):
    # 获取视频属性，可以通过属性 ID 或者属性名来获取。
    # 18 个属性 ID 和属性名的对应关系如下，前面是属性名称，然后是中文解释，cap.get() 中的参数可以属性 ID或属性名。
    print("CAP_PROP_POS_MSEC 当前位置的毫秒数：", cap.get(0))
    print("CAP_PROP_POS_FRAMES 当前位置的帧数：", cap.get(1))
    print("CAP_PROP_POS_AVI_RATIO 当前位置的相对位置：", cap.get(2))
    print("CAP_PROP_FRAME_WIDTH 帧宽度：", cap.get(3))
    print("CAP_PROP_FRAME_HEIGHT 帧高度：", cap.get(4))
    print("CAP_PROP_FPS 帧率：", cap.get(5))
    print("CAP_PROP_FOURCC 编解码器：", cap.get(6))
    print("CAP_PROP_FRAME_COUNT 帧总数：", cap.get(7))
    print("CAP_PROP_FORMAT 格式：", cap.get(8))
    print("CAP_PROP_MODE 模式：", cap.get(9))
    print("CAP_PROP_BRIGHTNESS 亮度：", cap.get(10))
    print("CAP_PROP_CONTRAST 对比度：", cap.get(11))
    print("CAP_PROP_SATURATION 饱和度：", cap.get(12))
    print("CAP_PROP_HUE 色调：", cap.get(13))
    print("CAP_PROP_GAIN 增益：", cap.get(14))
    print("CAP_PROP_EXPOSURE 曝光：", cap.get(15))
    print("CAP_PROP_CONVERT_RGB 是否转为 RGB：", cap.get(16))
    print("CAP_PROP_WHITE_BALANCE 白平衡：", cap.get(17))
    print("CAP_PROP_RECTIFICATION 矫正：", cap.get(18))

    # 还可以通过视频的属性名称获取，比如 cap.get(3) 或者 cap.get(cv2.CAP_PROP_FRAME_WIDTH) 来获取。
    print("CAP_PROP_FRAME_WIDTH 帧宽度：", cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    # 设置视频的属性
    try:
        ret = cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap.get(3) / 2)
        ret = cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap.get(4) / 2)
        ret = cap.set(cv2.CAP_PROP_FPS, 60)
    except Exception as err:
        print("属性设置失败: ", err)

    # 打开一个窗口查看捕获的帧
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        cv2.imshow("Video Window", frame)
        if cv2.waitKey(1) == ord("q"):
            break


if __name__ == "__main__":
    cap: cv2.VideoCapture
    # 创建 VideoCapture 对象。
    # 参数是设备索引号，如果只有一个摄像头，那么索引号就是 0
    # 也可以是一个文件名，这样就可以播放视频文件
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    # CapturePictureFromCamera(cap)
    # CaptureVideoFromCamera(cap)
    # SavingVideo(cap)
    # PlayingVideoFromFile()

    ViedeProperty(cap)

    # 退出程序结束之前释放摄像头
    cap.release()
    cv2.destroyAllWindows()
