# Slenium+Chrome 爬取淘宝美食

## 访问页面抓取信息：

+ 设置cookies：

  首先访问淘宝网，接着`time.sleep(40)`，利用这个时间手动登陆淘宝。储存下cookies。再取出cookies加载就可以了。（主要是为了练习设置cookies，否则设置个时间等待，再进行下面的操作即可）

  ```python
  def get_cookie(url):
      browser.get(url)
      time.sleep(30)
      cookies = browser.get_cookies()
      with open('cookie.txt', 'wb') as f:
          pickle.dump(cookies, f)
      print('Get Cookies')
  
  
  def set_cookie(url):
      browser.get(url)
      browser.delete_all_cookies()
      with open('cookie.txt', 'rb') as f:
          cookies = pickle.load(f)
      for cookie in cookies:
          browser.add_cookie(cookie)
          print(cookie)
  ```

  

+ 利用selenium抓取信息

  通过CSS选择器，找到网页要操作的目标。进行操作

  **例：**通过淘宝输入框输入 美食

  + 利用chrome开发者工具找到对应元素，右键选择复制CSS SELECTOR

    ![](C:\Users\春晓\Pictures\MD图片\批注 2020-07-27 170404.png)

```python
    #等待页面相应元素显示
    input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
    )
    submit = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_TSearchForm > div.search-button > button"))
    )
    #输入美食并且点击按钮
    input.send_keys('Macbook Pro')
    submit.click()
```



接下来通过操作翻页按钮获取每一页的信息

## 分析页面，（抓取产品、价格、店铺等信息）

使用的工具：**PyQuery**

通过chrome开发者工具找到，html页面想要得到的信息的所在位置，然后通过PyQuery提取出来

```python
def parse_page():
    wait.until = (
        EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist'))
    )
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    product_value = []
    for item in items:
        product = {
            'name': item.find('.title').text(),
            'price': item.find('.price').text(),
            'shop': item.find('.shop').text(),
        }
        product_value.append(product)
    print(product_value)
    return product_value
```

## 存储信息

使用工具：**openpyxl**

将得到想要的数据保存在excel中。