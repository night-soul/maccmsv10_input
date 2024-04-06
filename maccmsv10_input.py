import time, os, subprocess, re, shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from tkinter import Tk, simpledialog, filedialog

# 登录苹果CMSv10后台

# 创建一个Edge浏览器实例
wd = webdriver.Edge()
# 打开网页
wd.get("http://127.0.0.1:55225/MDadmin.php/admin/index/login.html")
# 输入账号
wd.find_element(By.CSS_SELECTOR, 'body > div.login-box > form > div:nth-child(2) > div > input').send_keys('super')
# 输入密码
wd.find_element(By.CSS_SELECTOR, 'body > div.login-box > form > div:nth-child(3) > div > input').send_keys('656412388255817')


# # 如果需要输入验证码，就把这段的注释去掉,启动后会询问你的验证码,需要手动输入到输入框中
# # 询问验证码，赋值给yzm
# def ask_captcha():
#     root = Tk()
#     root.withdraw()
#     captcha = simpledialog.askstring("验证码", "请输入验证码：", parent=root)
#     return captcha
# yzm = ask_captcha()
# # 输入验证码
# wd.find_element(By.CSS_SELECTOR, 'body > div.login-box > form > div:nth-child(4) > div > input').send_keys(yzm)


# 按登录
wd.find_element(By.CSS_SELECTOR, 'body > div.login-box > form > button').click()
# 登录成功


# 开始处理视频文件
def process_videos(target_folder):
    global mc, tp, sp, sc  # 定义全局变量，以便在函数外部使用
    main_folders = sorted([os.path.join(target_folder, f) for f in os.listdir(target_folder) if os.path.isdir(os.path.join(target_folder, f))])
    for main_folder in main_folders:
        # 提取文件夹名称中的数字
        folder_name = os.path.basename(main_folder)  # 获取文件夹的名称
        match = re.search(r'\d+', folder_name)  # 查找名称中的数字
        if match:
            index = int(match.group())  # 将找到的第一个数字转换为整数并赋给index
        else:
            index = 0  # 如果没有找到数字，可以根据需求调整这里的默认值
        video_files = sorted([f for f in os.listdir(main_folder) if f.endswith(('.mp4', '.avi', '.mkv'))])
        for video_file in video_files:
            # 检查文件名是否含有空格并移除
            if ' ' in video_file:
                new_video_name = video_file.replace(' ', '')
                original_video_path = os.path.join(main_folder, video_file)
                new_video_path = os.path.join(main_folder, new_video_name)
                os.rename(original_video_path, new_video_path)
                # 更新变量，以便后续操作使用新的路径
                video_file = new_video_name
            video_path = os.path.join(main_folder, video_file)
            video_name_without_extension = os.path.splitext(video_file)[0]
            new_folder_path = os.path.join(main_folder, video_name_without_extension)
            os.makedirs(new_folder_path, exist_ok=True)
            new_video_path = os.path.join(new_folder_path, video_file)
            shutil.move(video_path, new_video_path)
            mc = video_name_without_extension
            video_name_for_url = f"{video_name_without_extension}/{video_name_without_extension}"
            tp = f"http://ys.linghun.xyz:55225/video/{index}/{video_name_for_url}.png"
            sp = f"http://ys.linghun.xyz:55225/video/{index}/{video_name_for_url}.mp4"
            def get_video_duration(video_path):
                """使用ffmpeg获取视频的时长"""
                cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                    '-of', 'default=noprint_wrappers=1:nokey=1', video_path]
                try:
                    duration = float(subprocess.check_output(cmd).decode('utf-8').strip())
                    return duration
                except subprocess.CalledProcessError as e:
                    print("Error with ffprobe:", e.output)
                    return None
            duration = get_video_duration(new_video_path)
            if duration:
                # 将时长从秒转换为时分秒格式
                hours, remainder = divmod(duration, 3600)
                minutes, seconds = divmod(remainder, 60)
                sc = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
                # 直接跳转到视频中间的时间点
                mid_time = duration / 2
                output_image = os.path.join(new_folder_path, f"{video_name_without_extension}.png")
                ffmpeg_cmd = ['ffmpeg', '-ss', str(mid_time), '-i', new_video_path, '-frames:v', '1', output_image]
                subprocess.run(ffmpeg_cmd)
            final_folder_path = os.path.join("G:/ys.linghun.xyz/video", str(index))
            shutil.move(new_folder_path, final_folder_path)


            # 开始添加视频

            # 打开视频页面
            wd.find_element(By.CSS_SELECTOR, 'body > div > div:nth-child(2) > div.bottom-nav > ul.layui-nav.fl.nobg.main-nav > li:nth-child(5) > a').click()
            # 打开添加视频
            wd.find_element(By.CSS_SELECTOR, '#navBar > ul:nth-child(5) > li > dl > dd:nth-child(5) > a').click()
            # 切换到添加视频的页面
            iframe_element = wd.find_element(By.CSS_SELECTOR, 'iframe[lay-id="455"]')
            time.sleep(0.3)
            wd.switch_to.frame(iframe_element)
            time.sleep(0.3)
            # 打开分类
            wd.find_element(By.CSS_SELECTOR, 'body > div.page-container.p10 > form > div.layui-tab > div > div.layui-tab-item.layui-show > div:nth-child(1) > div:nth-child(2) > div > div > input').click()
            time.sleep(0.5)
            # 选择分类
            css_selector = f'body > div.page-container.p10 > form > div.layui-tab > div > div.layui-tab-item.layui-show > div:nth-child(1) > div:nth-child(2) > div > dl > dd:nth-child({index + 1})'
            time.sleep(0.3)
            wd.find_element(By.CSS_SELECTOR, css_selector).click()
            time.sleep(0.3)
            # 选择自动生成tag
            wd.find_element(By.CSS_SELECTOR, 'body > div.page-container.p10 > form > div.layui-tab > div > div.layui-tab-item.layui-show > div:nth-child(4) > div.layui-input-inline.w120 > div > i').click()
            # 打开播放器分类
            wd.find_element(By.CSS_SELECTOR, '#player_list > div > div:nth-child(2) > div > div > input').click()
            time.sleep(0.5)
            # 选择播放器
            wd.find_element(By.CSS_SELECTOR, '#player_list > div > div:nth-child(2) > div > dl > dd:nth-child(9)').click()
            # 输入名称
            wd.find_element(By.ID, 'vod_name').send_keys(mc)
            # 输入时长
            wd.find_element(By.ID, 'vod_duration').send_keys(sc)
            # 输入图片链接
            wd.find_element(By.ID, 'vod_pic').send_keys(tp)
            # 输入视频链接
            wd.find_element(By.ID, 'vod_content1').send_keys(sp)
            # 保存
            wd.find_element(By.CSS_SELECTOR, 'body > div.page-container.p10 > form > div.layui-form-item.center > div > button:nth-child(1)').click()
            time.sleep(1)
            wd.switch_to.default_content()
            time.sleep(0.3)

            # 清空mc, tp, sp的值以便下一个视频使用
            mc = tp = sp = sc = ''

root = Tk()
root.withdraw()
target_folder = filedialog.askdirectory()
process_videos(target_folder)
