#_*_encoding:utf-8_*_
"""
@Python -V: 3.X 
@SoftWave: Pycharm
@OS: Win10
@Author: SKYNE
@Contact: 520@skyne.cn
@Time: 2018.3.8
"""
import sqlite3

"""databasename : 59340ae8f2fe0.db"""

# 获取阅读量最高的文章的slug,
def get_slug():
    db_path = "../usr/59340ae8f2fe0.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if cursor:

        VIEWS_SELECT_SQL = "SELECT cid, views FROM typecho_contents ORDER BY created DESC, views DESC "

        cid_views = dict(cursor.execute(VIEWS_SELECT_SQL).fetchmany(50))

        views_max_five = sorted(cid_views.values(), reverse=True)[1:11]

        new_dict = {key:value for value, key in cid_views.items()}

        slug = []
        for i in views_max_five:
            # 本来想着所需要的东西都在数据库中，需要的东西从里面取就好了，知道后来我发现，数据库中没有题图的存储位置。
            # 无奈换种思路，得到最近发表的50篇文章后再按阅读量排序，得到阅读量最高的五篇文章，再写个爬虫，爬取信息就好了。
            # CONTENT_SELECT_SQL = "SELECT slug, title, text FROM typecho_contents WHERE cid =" + '\'' + str(new_dict[i]) + '\''
            #
            # article = list(cursor.execute(CONTENT_SELECT_SQL).fetchone())
            #
            # LABEL_SELECT_SQL = "SELECT mid FROM typecho_relationships WHERE cid = " + '\'' + str(new_dict[i]) + '\''
            #
            # mid = cursor.execute(LABEL_SELECT_SQL ).fetchone()[0]
            #
            # NAME_SELECT_SQL = "SELECT name FROM typecho_metas WHERE mid = " + '\'' + str(mid) + '\''
            #
            # name = cursor.execute(NAME_SELECT_SQL).fetchone()[0]
            #
            # article.append(name)
            #
            # article_list.append(article)
            CONTENT_SELECT_SQL = "SELECT slug FROM typecho_contents WHERE cid =" + '\'' + str(new_dict[i]) + '\''

            url = "http://jingyu.in/index.php/archives/" + cursor.execute(CONTENT_SELECT_SQL).fetchone()[0] + "/"

            slug.append(url)

        conn.close()

        return slug

    else:
        return False

# 判断email表是否存在，不存在解创建。
def create_email_table():
    conn = sqlite3.connect("Email.db")

    # eid 主键，number 期数，email 邮箱, flag 判断是否发送，未发送为0 ，发送为1
    CREATE_SQL = "CREATE TABLE IF NOT EXISTS typecho_email (eid INTEGER Primary Key, number INTEGER, email VARCHAR(20) NOT NULL UNIQUE, flag SMALLINT DEFAULT 0)"

    cursor = conn.cursor ()

    try:
        cursor.execute(CREATE_SQL)
        conn.commit()
        conn.close()
        return True

    except Exception:
        return False

# 插入邮箱地址到数据库
def insert_email(email):
    if create_email_table():
        SELECT_CID_MAX = "SELECT eid FROM typecho_email ORDER BY eid DESC"
        SELECT_NUMBER = "SELECT number FROM typecho_email WHERE eid = '1'"
        INSERT_SQL = "INSERT INTO typecho_email VALUES (?, ?, ?, ?)"

        conn = sqlite3.connect ("Email.db")

        cursor = conn.cursor ()

        if cursor.execute(SELECT_CID_MAX).fetchone():
            eid = str(int(cursor.execute(SELECT_CID_MAX).fetchone()[0]) + 1)
            number = str(cursor.execute(SELECT_NUMBER).fetchone()[0])

        else:
            eid = '1'
            number = '1'

        values = (eid, number, email, '0')
        print(values)

        try:
            cursor.execute(INSERT_SQL, values)
        except sqlite3.IntegrityError:
            print("Insert Into Error! Email is exists! Email = {}".format(email))

        conn.commit()

# 获取eid的最大值，以及期数
def get_eid_number():
    conn = sqlite3.connect("Email.db")
    cursor = conn.cursor ()

    SELECT_CID_MAX = "SELECT eid FROM typecho_email ORDER BY eid DESC"
    SELECT_NUMBER = "SELECT number FROM typecho_email WHERE eid = '1'"

    if cursor.execute (SELECT_CID_MAX).fetchone ():
        eid = str (int (cursor.execute (SELECT_CID_MAX).fetchone ()[0]))
        number = str (int (cursor.execute (SELECT_NUMBER).fetchone ()[0]))

    else:
        eid = '1'
        number = '1'

    conn.close ()

    return (eid,number)

# 根据eid 获取对应的邮件地址
def get_email(id):
    conn = sqlite3.connect("Email.db")
    cursor = conn.cursor ()

    SELECT_EMAIL = "SELECT email FROM typecho_email WHERE eid =" + '\'' + str(id) + '\''

    SELECT_FLAG = "SELECT flag FROM typecho_email WHERE eid = " + '\'' + str(id) + '\''

    UPDATE_FLAG = "UPDATE typecho_email SET flag = '1' WHERE eid = " + '\'' + str(id) + '\''

    flag = cursor.execute(SELECT_FLAG).fetchone()[0]

    if flag == 0:
        eid = cursor.execute (SELECT_EMAIL).fetchone ()[0]

        cursor.execute(UPDATE_FLAG)

        conn.commit ()
        conn.close ()

        return eid

    else:
        return False

# 全部发送后，将所有flag置为0, 并将number加1
def update_all_flag():
    conn = sqlite3.connect("Email.db")
    cursor = conn.cursor ()

    SELECT_NUMBER = "SELECT number FROM typecho_email WHERE eid = '1'"

    number = int(cursor.execute(SELECT_NUMBER).fetchone()[0]) + 1

    UPDATE_FLAG = "UPDATE typecho_email SET flag = '0', number = " + '\'' + str(number) + '\''

    cursor.execute(UPDATE_FLAG)

    conn.commit ()
    conn.close ()

    print("All Flag is 0")

if __name__ == '__main__':
    # print(get_slug())
    # email = '116304694@qq.com'
    # insert_email(email)
    # print(get_eid_number())
    # print(get_email(2))
    # update_all_flag()
    print(get_email(id='179837').replace('-', ''))