#encoding='utf-8'
import requests
from urllib.parse import urlencode
import time

#需下载的图片的数量
NUMBER_OF_PHOTO=100

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
        'page': str(page),
        'per_page': '12',
        'order_by': 'latest'
    }
    url = base_url + urlencode(params)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        json = response.json()
        photo_url_download_true=[]
        photo_id=[]
        data=[]
        for i in range(len(json)):
            photo_url_id = json[i].get('id')
            #print(photo_url_id)
            photo_url_download = 'https://unsplash.com/photos/' + photo_url_id + '/download?force=true'
            #获取重定向后的url
            response1 = requests.get(photo_url_download, headers=headers, allow_redirects=False)
            photo_url_download = response1.headers['Location']
            photo_url_download_true.append(photo_url_download)
            photo_id.append(photo_url_id)
        data.append(photo_url_download_true)
        data.append(photo_id)
        return data
    else:print('获取重定向后的url失败')

#将照片写入文件
def write_to_file(photo_url_download_true,id,page,number):
    response2 = requests.get(photo_url_download_true)
    if response2.status_code == 200:
        file_path = "e:/Unsplash/" + id + ".jpg"
        with open(file_path, 'wb') as f:
            f.write(response2.content)
        print('正在下载第%d张照片.....' % (page*12+number+1))
        print(id + ".jpg" + '下载成功')
    else:
        print('下载失败')

#计算函数
def calc():
    page=(NUMBER_OF_PHOTO -1)// 12
    number=NUMBER_OF_PHOTO -page*12
    return [page,number]

#主函数
def main():
    pages=calc()[0]
    numbers=calc()[1]
    for page in range(pages):
        print('********************请耐心等待********************')
        data = json_parse(page)
        for count in range(12):
            write_to_file(data[0][count],data[1][count],page,count)
    print("********************请耐心等待********************")
    data=json_parse(pages)
    for number in range(numbers):
        write_to_file(data[0][number],data[1][number],pages,number)

if __name__=='__main__':
    main()
