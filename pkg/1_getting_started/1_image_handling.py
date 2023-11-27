import sys
import cv2

# 注释说说明的函数调用都是指 C++ 的函数，OpenCV 是用 C++ 编写的，而 OpenCV-Python 只是用 Python 代码调用 C++ 的函数


# 教程-OpenCV 中的 GUI 之 图像入门：https://docs.opencv.org/4.x/db/deb/tutorial_display_image.html
def GUIGettingStartedWithImages():
    # 调用 cv::imread 函数读取图片，图片的数据将会存储在 cv::Mat 对象。
    # 说白了就是实例化一个 cv::Mat 对象，所有对图片的操作其实都是在操作这个对象
    # image = cv2.imread("images/starry_night.jpg")
    # 函数的第二个参数可以指定我们想要的图像格式
    # - IMREAD_COLOR 以 BGR 8 位格式加载图像。这是此处使用的默认值。
    # - IMREAD_UNCHANGED 按原样加载图像（包括 alpha 通道，如果存在）。其实就是将图片变为黑白的了
    # - IMREAD_GRAYSCALE 将图像作为强度加载
    image = cv2.imread("images/starry_night.jpg", cv2.IMREAD_COLOR)
    # 注意：Mat 对象实际上是 NumPy 库中的 numpy.ndarray 对象，因此我们可以使用 numpy 的函数来操作它

    if image is None:
        sys.exit("无法读取图片")

    # 调用 cv::imshow 打开一个窗口，并显示图片
    # 第一个参数是窗口的标题，第二个参数是将要显示的 cv::Mat 对象。
    cv2.imshow("Window Title", image)

    # 调用 cv::imshow 后，必须等待用户按键，否则窗口打开后会立即关闭
    # 调用 cv::waitKey 等待用户按键，函数的参数是等待时间(毫秒)，为 0 时表示一直等待直到接收到用户的按键。
    # cv::waitKey 的返回值是按键对应的数字，比如按下 s 键，返回值就是 115。
    k = cv2.waitKey(0)

    # 由于 waitKey 的返回值是数字，所以如果想要人类可读，需要使用 ord 函数将按键转换为数字
    # 这里按下 s 则会将图片保存到本地
    if k == ord("s"):
        # 调用 cv::imwrite 将 Mat 对象写入文件
        cv2.imwrite("images/starry_night_save.jpg", image)


if __name__ == "__main__":
    GUIGettingStartedWithImages()
