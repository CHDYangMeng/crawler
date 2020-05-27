
from urllib.request import urlopen
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore")

html = urlopen("http://www.biqiuge.com/book/4772/2940354.html")
Text = BeautifulSoup(html)
text = Text.find_all( "div",{"class":"showtxt"})
for i in text:
    print(i.get_text())