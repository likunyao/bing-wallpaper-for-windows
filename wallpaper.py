import requests
import re
import win32api
import win32con
import win32gui


def get_image():
    url = 'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&nc=1578037207421&pid=hp'
    response = requests.get(url)

    reg = re.compile('"url":"(.*?)","urlbase"', re.S)
    name_reg = re.compile('"enddate":"(.*?)","url"', re.S)

    relative_path = re.findall(reg, response.text)[0].split('&')[0]
    image_url = 'http://cn.bing.com' + relative_path

    name = re.findall(name_reg, response.text)[0]
    image = requests.get(image_url).content
    file_name = 'D:\\wallpaper\\{}.jpg'.format(name)
    with open(file_name, 'wb') as f:
        f.write(image)
    return file_name


def setWallPaper(pic_path):
    key = win32api.RegOpenKeyEx(
        win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "2")
    win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER,pic_path, win32con.SPIF_SENDWININICHANGE)

if __name__ == '__main__':
    file_name = get_image()
    setWallPaper(file_name)