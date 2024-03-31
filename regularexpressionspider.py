import re,requests,time

def spide_page():
    resp = requests.get('http://woniunote.com/')
    resp.encoding='utf-8'
    # print(resp.text)
    page_pattern = '<a href="(.+?)"'
    page_links = re.findall(page_pattern,resp.text)
    for link in page_links:
        if 'css' in link or 'articleid' in link:
            continue
        if link.startswith('#'):
            continue
        if link.startswith('/'):
            link = 'http://woniunote.com' + link
        print(link)
        filename = link.split('/')[-1] + time.strftime('%Y%m%d_%H%M%S') + '.html'
        with open(f'./woniunote/pages/{filename}',mode='w',encoding='utf-8') as file:
            file.write(resp.text)

def spide_img():
    resp = requests.get('http://woniunote.com/')
    resp.encoding='utf-8'
    img_pattern = ' <img src="(.+?)"'
    img_links = re.findall(img_pattern,resp.text)
    for link in img_links:
        if link.startswith('/'):
            link = 'http://woniunote.com' + link
        # print(link)
        filename = link.split('/')[-1]
        content = requests.get(link).content
        with open(f'./woniunote/images/{filename}',mode='wb') as file:
            file.write(content)

if __name__ == '__main__':
    pass
    # spide_page()
    # spide_img()
