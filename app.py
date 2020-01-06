import os
from tkinter import *
from urllib.request import urlretrieve
from selenium import webdriver


# Step2-获取数据
# 下载音乐
def song_load(item):
    song_id = item['song_id']
    song_name = item['song_name']
    song_url = 'http://music.163.com/song/media/outer/url?id={}.mp3'.format(song_id)
    # 创建文件夹
    os.makedirs('music', exist_ok=True)  # 如果文件夹存在，不报错
    path = r'music\\{}.mp3'.format(song_name)
    # 文本框
    text.insert(END, '歌曲：{}. 正在下载中...'.format(song_name))
    # 文本框滚动
    text.see(END)
    # 更新
    text.update()
    # 下载
    urlretrieve(song_url, path)
    # 文本框
    text.insert(END, '下载完毕：{}. 请试听...'.format(song_name))
    # 文本框滚动
    text.see(END)
    # 更新
    text.update()


# 获取音乐id
def get_music_id():
    name = entry.get()
    url = 'https://music.163.com/#/search/m/?s={}&type=1'.format(name)
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=r'C:\\chromedriver.exe', chrome_options=option)
    driver.get(url=url)

    driver.switch_to.frame('g_iframe')
    req = driver.find_element_by_id('m-search')
    # 获取歌曲id
    a_id = req.find_element_by_xpath('.//div[@class="item f-cb h-flag  "]/div[2]//a').get_attribute('href')
    song_id = a_id.split('=')[-1]
    print(song_id)
    # 获取歌曲名称
    song_name = req.find_element_by_xpath('.//div[@class="item f-cb h-flag  "]/div[2]//b').get_attribute('title')
    print(song_name)
    # 构造返回数据
    item = {}
    item['song_id'] = song_id
    item['song_name'] = song_name

    song_load(item)


# Step1-构建窗口
# 主画布
root = Tk()
# 设置画布大小
root.geometry('575x450')
# 窗口标题
root.title('MusicDownloader')
# 添加label
label = Label(root, text='请输入：', font=('微软雅黑', 15))
label.grid(row=0, column=0)
# 添加entry
entry = Entry(root, font=('微软雅黑', 15))
entry.grid(row=0, column=1)
# 添加listbox
text = Listbox(root, font=('微软雅黑', 15), width=45, height=10)
text.grid(row=1, columnspan=2)
# 添加button
button_quit = Button(root, text='退出程序', width='10', command=root.quit)
button_quit.grid(row=2, column=1, sticky=E)
button_search = Button(root, text='开始搜索', width='10', command=get_music_id)
button_search.grid(row=2, column=0, sticky=W)


root.mainloop()

# Create EXE app
# pyinstaller.exe -F -i music_128px.ico app.py -w
