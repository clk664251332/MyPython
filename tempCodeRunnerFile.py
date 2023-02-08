for i in range(1, 28):
    url = URL.format(i)
    try:
        html = Request(url)
    except urllib.error.URLError as e:
         print(e)
         continue
    print("----第{0}页----".format(i))
    ExtractData(html, i)