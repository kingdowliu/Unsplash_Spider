import requests
from urllib.parse import urlencode

#需下载的图片的数量
NUMBER_OF_PHOTO=1

#初始信息
base_url='https://unsplash.com/napi/photos?'
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0',
    'X-Requested-With':'XMLHttpRequest',
    'Referer':'https://unsplash.com/',
    'Host':'unsplash.com',
    'Connection':'keep-alive',
    'Cookie':'i=95caba50-1d15-11e8-86e1-73123983863e; xpo=%7B%7D; _sp_id.0295=93dbf183-b5f0-4823-86ab-ed830d4da8a9.1519883914.27.1530416040.1530370938.650ac4ce-9475-4dce-bfd6-0cbd7bf32d02; _ga=GA1.2.2028538097.1519883915; uuid=96d08fb0-5d8e-11e8-825c-715be5f2c2f3; xpos=%7B%7D; _gid=GA1.2.588177965.1530343545; lsnp=bwF3hwmnGWQ; _sp_ses.0295=*; _gat=1'
}

#解析一个页面的json
def json_parse(page):
    params = {
        'page': str(page + 1),
        'per_page': '12',
        'order_by': 'latest'
    }
    url = base_url + urlencode(params)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        json = response.json()
        photo_url_id = json[0].get('id')
        photo_url_download = 'https://unsplash.com/photos/' + photo_url_id + '/download?force=true'
        #获取重定向后的url
        response1 = requests.get(photo_url_download, headers=headers, allow_redirects=False)
        photo_url_download_true = response1.headers['Location']
        return [photo_url_download_true,photo_url_id]
    else:print('获取重定向后的url失败')

#将照片写入文件
def write_to_file(photo_url_download_true,id,page):
    response2 = requests.get(photo_url_download_true)
    if response2.status_code == 200:
        file_path = "e:/Unsplash/" + id + ".jpg"
        with open(file_path, 'wb') as f:
            f.write(response2.content)
        print(str(page) + id + ".jpg" + '下载成功')
    else:
        print('下载失败')

#主函数
def main():
    for page in range(NUMBER_OF_PHOTO):
        write_to_file(json_parse(page)[0],json_parse(page)[1],page)


if __name__=='__main__':
    main()
