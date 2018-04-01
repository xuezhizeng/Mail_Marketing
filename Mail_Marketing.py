#_*_encoding:utf-8_*_
"""
@Python -V: 3.X 
@SoftWave: Pycharm
@OS: Win10
@Author: SKYNE
@Contact: 520@skyne.cn
@Time: 2018.3.7
"""

import re

import time

from Spider import get_article, get_book_list

from SendMail import sendmail

from DataBase import get_slug, get_email, get_eid_number, update_all_flag, insert_email

html_header = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>鲸鱼圈-有料有趣的互联网资讯</title>
</head>
<body>
    <table align="center" border="0" cellpadding="0" cellspacing="0" style="BORDER-COLLAPSE: collapse; POSITION: relative; BACKGROUND-COLOR: #eee" width="640">
      <tbody>
          <tr>
            <td><img height="220" src="http://www.easemob.com/themes/official_v3/Public/img/edm/developers_weekly_v2/edm-banner@2x.jpg" style="BORDER-LEFT-WIDTH: 0px; BORDER-RIGHT-WIDTH: 0px; BORDER-BOTTOM-WIDTH: 0px; DISPLAY: block; BORDER-TOP-WIDTH: 0px" width="640"  /> </td>
            <td style="position: absolute; left: 8px; top: 8px"><a href="http://sctrack.sendcloud.net/track/click/eyJ1c2VyX2lkIjogMjk1MjksICJ0YXNrX2lkIjogIiIsICJlbWFpbF9pZCI6ICIxNTEzMjM3NjEzNjg1XzI5NTI5XzE5NzA5XzM1MjEuc2MtMTBfOV82XzE4MS1pbmJvdW5kMCQxMTI3MjE4MTI0QHFxLmNvbSIsICJzaWduIjogIjdjODVkZDU2ZWUyYmNlYTZmYjU4NzBhYzZkYWRkZTYxIiwgInVzZXJfaGVhZGVycyI6IHt9LCAibGFiZWwiOiAwLCAibGluayI6ICJodHRwJTNBLy93d3cuZWFzZW1vYi5jb20lM0Z1dG1fc291cmNlJTNEZWRtIiwgImNhdGVnb3J5X2lkIjogOTUxODR9.html" target="_blank"><img height="28" src="http://miduapp.jingyu.in/logo.png" style="BORDER-TOP: 0px; BORDER-RIGHT: 0px; BORDER-BOTTOM: 0px; BORDER-LEFT: 0px; DISPLAY: block" width="49"  /></a></td>
            <td height="100" style="FONT-SIZE: 10px; POSITION: absolute; COLOR: #fff; TEXT-ALIGN: left; LEFT: 53px; TOP: 4%; " valign="middle" width="640">鲸鱼圈<br  /><span>有料有趣的互联网资讯</span>
            <td style="right: 28px; position: absolute; top: 12px"><a href="http://jingyu.in" style="FONT-SIZE: 11px; TEXT-DECORATION: none; COLOR: #ccc" target="_blank">&gt;&gt;进入官网</a> </td>
            <td height="100" style="FONT-SIZE: 14px; POSITION: absolute; COLOR: #fff; TEXT-ALIGN: center; LEFT: 0px; TOP: 40%" valign="middle" width="640"><a href="http://jingyu.in" style="font-weight:bold;text-decoration:none; COLOR: #FFFFFF";" target="_blank">每周互联网热文精选-第number期<br/><br><span>鲸鱼圈-这里有产品运营干货知识、创业报道、精品书单、科技人物报道、应用推荐</span></a>
            </td>
          </tr>
        </tbody>
    </table>
    <!--上面是题图部分，下面则是文章列表的tbody-->
<table align="center" border="0" cellpadding="0" cellspacing="0" style="BORDER-COLLAPSE: collapse; bakcground-color: #ffffff" width="640">
  <tbody>
  <tr>
    <td>
      <table align="center" border="0" cellpadding="0" cellspacing="0" style="BORDER-COLLAPSE: collapse; BACKGROUND-COLOR: #eee" width="640">
        <tbody>
        <tr>
          <td>
            <table align="center" border="0" cellpadding="0" cellspacing="0" style="PADDING-BOTTOM: 0px; PADDING-TOP: 0px; PADDING-LEFT: 28px; PADDING-RIGHT: 28px" width="640">
              <tbody>
              <tr>
                <td height="46"></td></tr>"""

html_footer = """
  <tfoot>
  <tr>
    <td>
      <table align="center" border="0" cellpadding="0" cellspacing="0" style="BORDER-COLLAPSE: collapse; BACKGROUND-COLOR: #eee" width="640">
        <tbody>
        <tr>
          <td height="50"><img height="19" src="http://www.easemob.com/themes/official_v3/Public/img/edm/developers_weekly_v2/logo-bottom.png" style="BORDER-LEFT-WIDTH: 0px; BORDER-RIGHT-WIDTH: 0px; BORDER-BOTTOM-WIDTH: 0px; DISPLAY: block; BORDER-TOP-WIDTH: 0px" width="640"  /> </td></tr></tbody></table></td></tr>
  <tr>
    <td>
      <table align="center" border="0" cellpadding="0" cellspacing="0" style="BORDER-COLLAPSE: collapse; BACKGROUND-COLOR: #273140" width="640">
        <tbody>
        <tr>
          <td height="26"></td></tr>
        <tr>
          <td>
            <table border="0" cellpadding="0" cellspacing="0" style="PADDING-BOTTOM: 0px; PADDING-TOP: 0px; PADDING-LEFT: 28px; PADDING-RIGHT: 28px" width="640">
              <tbody>
              <tr>
                <td style="FONT-SIZE: 12px; FONT-WEIGHT: 400; COLOR: #838383" valign="bottom" width="374"><a href="http://jingyu.in" style="FONT-SIZE: 16px; TEXT-DECORATION: none; color:#4183c4;" target="_blank"><span>鲸鱼圈-有料有趣的互联网资讯</span><br/></a><br>
                  <span>鲸鱼圈-科技资讯,故事,书单,创业,乐趣,兴趣,文艺,有料,有趣,互联网资讯,产品经理,程序猿,产品运营,创业报道,科技人物,应用推荐,干货知识</span><br> </td>
                <td align="center" height="100" width="130"><a href="https://weibo.com/zuiwubiaoqing?refer_flag=1001030101_" style="TEXT-DECORATION: none; COLOR: #FFFFFF"; target="_blank"><img height="90" src="http://www.easemob.com/themes/official_v3/Public/img/edm/developers_weekly_v2/qr-weibo.png" style="BORDER-LEFT-WIDTH: 0px; MARGIN-BOTTOM: 11px; BORDER-RIGHT-WIDTH: 0px; BORDER-BOTTOM-WIDTH: 0px; DISPLAY: block; BORDER-TOP-WIDTH: 0px" width="90"  />鲸鱼圈官微</a></td>
                <td align="center" height="100" width="130"><img height="90" src="http://or6fe9yua.bkt.clouddn.com/nangpngqiluo.jpg" style="BORDER-LEFT-WIDTH: 0px; MARGIN-BOTTOM: 11px; BORDER-RIGHT-WIDTH: 0px; BORDER-BOTTOM-WIDTH: 0px; DISPLAY: block; BORDER-TOP-WIDTH: 0px" width="90"  /><a style="TEXT-DECORATION: none; COLOR: #FFFFFF";">关注鲸鱼圈</a></td>
                <td align="center" width="130"><a style="TEXT-DECORATION: none; COLOR: #FFFFFF"; target="_blank" href="https://juejin.im/user/58073413128fe10054ce008c"> <img height="90" src="http://or6fe9yua.bkt.clouddn.com/1520486695.png" style="BORDER-LEFT-WIDTH: 0px; MARGIN-BOTTOM: 11px; BORDER-RIGHT-WIDTH: 0px; BORDER-BOTTOM-WIDTH: 0px; DISPLAY: block; BORDER-TOP-WIDTH: 0px" width="90"  />掘金社区</a></td></tr>
              <tr>
                <td colspan="4" height="18"></td></tr></tbody></table></td></tr>
        <tr>
          <td>
            <table  align="center" border="0" cellpadding="0" cellspacing="0" width="640"><tbody>
              <tr>
                <ul style="FONT-SIZE: 15px; TEXT-ALIGN: center;">
                    <a href="http://jingyu.in" style="color:#4183c4;font-weight:bold;text-decoration:none" target="_blank">鲸鱼圈</a>
                    <span style="color:#999">•</span>
                    <a href="http://jingyu.in" style="color:#4183c4;font-weight:bold;text-decoration:none" target="_blank">首页</a>
                    <span style="color:#999">•</span>
                    <a href="http://jingyu.in/index.php/category/default/" style="color:#4183c4;font-weight:bold;text-decoration:none" target="_blank">科技资讯</a>
                    <span style="color:#999">•</span>
                    <a href="http://jingyu.in/index.php/category/gs/" style="color:#4183c4;font-weight:bold;text-decoration:none" target="_blank">干货知识</a>
                    <span style="color:#999">•</span>
                    <a href="http://jingyu.in/index.php/category/sd/" style="color:#4183c4;font-weight:bold;text-decoration:none" target="_blank">精品书单</a>
                    <span style="color:#999">•</span>
                    <a href="http://jingyu.in/index.php/328.html" style="color:#4183c4;font-weight:bold;text-decoration:none" target="_blank">投稿</a>
                </ul>
                <br>
                <td align="center" style="FONT-SIZE: 11px; COLOR: #838383"><a href="http://jingyu.in" style="TEXT-DECORATION: none; COLOR: #599ccd" target="_blank">鲸鱼圈</a>&nbsp; 豫ICP备16039217号</td></tr>
              <tr>
                <td height="5"></td></tr></tbody></table></td></tr>
        <tr>
          <td height="20"></td></tr></tbody></table></td></tr>
  </tfoot>
</table>"""

html_article = """
              <tr id="headline">
                <td>
                  <table border="0" cellpadding="0" cellspacing="0" width="640">
                    <tbody>
                    <tr>
                      <td style="FONT-SIZE: 14px; FONT-FAMILY: &#39; FONT-WEIGHT: 700; COLOR: #162540; LINE-HEIGHT: 32px">article-label
                      </td>
                    </tr>
                    </tbody>
                  </table>
                </td>
              </tr>
              <tr>
                <td style="vertical-align: top">
                  <table border="0" cellpadding="0" cellspacing="0" width="640">
                    <tbody>
                    <tr>
                      <td style="vertical-align: top">
                        <table cellpadding="0" cellspacing="0" width="100%">
                          <tbody>
                          <tr>
                            <td align="left" width="440"><a href="article-url" style="FONT-SIZE: 14px; TEXT-DECORATION: none; FONT-WEIGHT: bold; COLOR: #143c82; TEXT-ALIGN: justify; LINE-HEIGHT: 1.9" target="_blank">article-title</a>
                          </td>
                          </tr>
                          <tr>
                            <td style="FONT-SIZE: 11px; COLOR: #FFFFFF; LINE-HEIGHT: 1.9" width="440"><a href="article-url" style="FONT-SIZE: 12px; TEXT-DECORATION: none;target="_blank";> article-abstract </a><br/><a href="article-url" style="FONT-SIZE: 11px; TEXT-DECORATION: none; FLOAT: right; COLOR: #348dc8" target="_blank">了解更多&gt;&gt;</a>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                      </td>
                      <td width="10"></td>
                      <td width="144">
                        <a href="article-url" style="FONT-SIZE: 11px; TEXT-DECORATION: none; FLOAT: right; COLOR: #348dc8" target="_blank">
                          <img src="cover-url" style="BORDER-LEFT-WIDTH: 0px; BORDER-RIGHT-WIDTH: 0px; BORDER-BOTTOM-WIDTH: 0px; DISPLAY: block; BORDER-TOP-WIDTH: 0px" width="144"/>
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <td height="25">
                      </td>
                    </tr>
                    </tbody>
                  </table>
                </td>
              </tr>"""


# 'article-url', 'cover-url', 'article-title', 'article-abstract'

# 从数据库中获取期数，然后替换
def replace_header():
    number = get_eid_number()[1]
    return html_header.replace('number', str(number))

# 通过爬取书单部分的分类，获取到书单title和url，然后通过字符串拼接，组成新的书单部分
def replace_booklist():
    html_base = """    <tr id="booklist">
        <td>
          <table border="0" cellpadding="0" cellspacing="0" width="584">
            <tbody>
            <tr>
              <td style="FONT-SIZE: 14px; FONT-FAMILY: &#39;SourceHanSansCN Bold&#39;; FONT-WEIGHT: 700; COLOR: #162540">书单推荐 
              </td></tr></tbody></table></td></tr>
        <tr>
        <td>
          <table border="0" cellpadding="0" cellspacing="0" width="584">
            <tbody>
            <tr>
              <td style="font-size: 12px; font-weight: 500; color: #348dc8">
                <ul style="list-style-type: none; padding-bottom: 0px; padding-top: 0px; padding-left: 0px; line-height: 2; padding-right: 0px">
"""

    html_end = """
            <tr>
              <td height="16"></td></tr></tbody></table></td></tr>"""

    booklist = get_book_list()

    html_li = ""
    for i in booklist:
        html_li =html_li + '<li style="list-style-type: none"><a href=\"' + i[1] + '\" style="FONT-SIZE: 12px; TEXT-DECORATION: none; COLOR: #348dc8" target="_blank">' + i[0] + '</a></li>'

    return html_base + html_li + html_end

# 从数据库中获取阅读量最高的五篇文章，并填充到对应的部分
def replace_url(article):

    h1 = re.sub('article-url', article['article-url'], html_article)

    h2 = re.sub('cover-url', article['cover-url'], h1)

    h3 = re.sub ('article-title', article['article-title'], h2)

    h4 = re.sub('article-abstract', article['article-abstract'], h3)

    h5 = re.sub ('article-label', article['article-label'], h4)


    return h5

# 将邮件html各个部分链接起来
def html_join():
    slug_list = get_slug()

    counter = 0
    html_body = ""
    for url in slug_list:
        article = get_article(url)
        if article and counter < 5:
            temp = replace_url(article)
            html_body = html_body + temp
            counter += 1

    html = replace_header() + html_body + replace_booklist() + html_footer

    return html

# 从数据库中获取邮箱地址，然后发送
def send_email():

    content = html_join()

    eid_max = get_eid_number()[0]

    # 计时器，记录发送的封数，推算时间，超过20min，就等待五分钟
    counter = 0
    for eid in range(1, int(eid_max)):

        addr = get_email(id=eid)

        # 数据录入问题，有些数据中开头是'-'
        if addr:
            sendmail(content,addr.replace('-', ''))

            print("{}th Letter are being sent".format(eid))
            counter += 1
            time.sleep(30)
            if counter % 40 == 0:
                time.sleep(300)

    # 发送完成后将所有flag置为0，代表未发送，并将number期数加 1
    update_all_flag()

    print("All Email Send Success!")

def send_mail_test():
    content = html_join ()

    address = ['520@skyne.cn','2295558248@qq.com']

    for addr in address:
        sendmail (content, addr)
        print ("All Email Send Success!")

if __name__ == "__main__":
    send_email()

   # send_mail_test()
