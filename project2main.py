import os
import MySQLdb
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


def connectDB():
    db = MySQLdb.connect(host="localhost", user="root", passwd="",
                         db="db2project")
    cur = db.cursor()
    return db, cur


def runSQL(filename):
    cnx = {'host': ' 127.0.0.1', 'username': 'root', 'password': '',
           'db': 'db2project    '}
    db, cur = connectDB()
    for line in open(filename):
        print ''
        print line
        cur.execute(line)
        col_names = [desc[0] for desc in cur.description]
        print col_names
        print ''
        for item in cur.fetchall():
            print item
        db.commit()
    db.close()


# INSERT statements.Loding the data
# runSQL('PROJECT2SQL.sql')

# to display the inserted data
# runSQL('displayData.sql')

@app.route('/')
def showLandingPage():
    return render_template('webpage.html')


@app.route('/newuser', methods=['POST'])
def addnewuser():
    id_num = request.form['idnum']
    acc_name = request.form['acname']
    phone = request.form['phone']
    db, cur = connectDB()
    print id_num
    print  acc_name
    print  phone
    # query = "insert into user_account values (%s, %s, %s)", (id_num,
    # acc_name,phone))
    cur.execute(
        """insert into user_account(ID_NUM, USER_ACCOUNT_NAME, PHONE_NUMBER,
        ROLE_NAME) values (%s, %s, %s,null)""",
        (id_num, acc_name, phone))
    for item in cur.fetchall():
        print item
    db.commit()
    db.close()
    return 'Success'


@app.route('/addnewrole', methods=['POST'])
def addnewrole():
    rolename = request.form['rolename']
    desc = request.form['desc']
    db, cur = connectDB()
    print rolename
    print  desc
    cur.execute(
        """insert into user_role(ROLE_NAME, DESCRIPTION) values (%s, %s)""",
        (rolename, desc))
    for item in cur.fetchall():
        print item
    db.commit()
    db.close()
    return 'Success'


@app.route('/addnewtable', methods=['POST'])
def addnewtable():
    tablename = request.form['tablename']
    owner = request.form['owner']
    db, cur = connectDB()
    print tablename
    print  owner
    cur.execute("""insert into tables(TABLE_NAME, ID_NUM) values (%s, %s)""",
                (tablename, owner))
    for item in cur.fetchall():
        print item
    db.commit()
    db.close()
    return 'Success'


@app.route('/addnewprivilege', methods=['POST'])
def addnewprivilege():
    privname = request.form['privname']
    privtype = request.form['privtype']
    db, cur = connectDB()
    print privname
    print  privtype
    cur.execute(
        """insert into privilege(PRIVILEGE_NAME, PRIVILEGE_TYPE) values (%s,
        %s)""",
        (privname, privtype))
    for item in cur.fetchall():
        print item
    db.commit()
    db.close()
    return 'Success. Check console for results.'


@app.route('/roleaccount', methods=['POST'])
def roleaccount():
    acidnum = request.form['acidnum']
    rolename = request.form['rolename']
    db, cur = connectDB()
    print acidnum
    print  rolename
    cur.execute("""UPDATE USER_ACCOUNT SET ROLE_NAME = %s  WHERE ID_NUM = %s""",
                (rolename, acidnum))
    for item in cur.fetchall():
        print item
    db.commit()
    db.close()
    return 'Success. Check console for results.'


@app.route('/privaccount', methods=['POST'])
def privaccount():
    rolename = request.form['rolename']
    privname = request.form['privname']
    privtype = request.form['privtype']
    db, cur = connectDB()
    print rolename
    print  privname
    # cur.execute("""UPDATE USER_ACCOUNT SET ROLE_NAME = %s  WHERE ID_NUM =
    # %s""", (rolename, acidnum))
    cur.execute(
        """insert into ROLE_HAS_PRIVILEGES(ROLE_NAME, PRIVILEGE_NAME,
        PRIVILEGE_TYPE) values (%s, %s, %s)""",
        (rolename, privname, privtype))

    for item in cur.fetchall():
        print item
    db.commit()
    db.close()
    return 'Success. Check python console for results.'


@app.route('/ternary', methods=['POST'])
def ternary():
    rolename = request.form['rolename']
    privname = request.form['privname']
    privtype = request.form['privtype']
    tablename = request.form['tablename']
    db, cur = connectDB()
    print rolename
    print  privname
    # cur.execute("""UPDATE USER_ACCOUNT SET ROLE_NAME = %s  WHERE ID_NUM =
    # %s""", (rolename, acidnum))
    cur.execute(
        """insert into roles_has_relational_privileges_on_tables(ROLE_NAME,
        TABLE_NAME, PRIVILEGE_NAME,PRIVILEGE_TYPE) values (%s, %s, %s, %s)""",
        (rolename, tablename, privname, privtype))
    for item in cur.fetchall():
        print item
    db.commit()
    db.close()
    return 'Query executed. Check the python console for results'


@app.route('/rolesprivquery', methods=['POST'])
def rolesprivquery(rolename=None):
    if rolename is None:
        rolename = request.form['rolename']
    db, cur = connectDB()
    fileList = []
    print "Roles Name is"
    print rolename
    cur.execute("""select * from role_has_privileges where ROLE_NAME = %s""",
                (rolename,))
    for item in cur.fetchall():
        fileList.append(item)
    query = 'SELECT DISTINCT ROLE_NAME, PRIVILEGE_NAME, PRIVILEGE_TYPE from ' \
            'roles_has_relational_privileges_on_tables'
    cur.execute(
        """SELECT DISTINCT ROLE_NAME, PRIVILEGE_NAME, PRIVILEGE_TYPE from
        roles_has_relational_privileges_on_tables where ROLE_NAME = %s""",
        (rolename,))
    for item in cur.fetchall():
        fileList.append(item)
    print "Privileges for the above role are"

    print ' '
    print "(ROLE NAME  --- PRIVILEGE NAME --- PRIVILEGE TYPE)"

    for item in fileList:
        print item
    db.commit()
    db.close()
    return 'Query executed. Check the python console for results'


@app.route('/accountprivuquery', methods=['POST'])
def accountprivuquery():
    db, cur = connectDB()
    accntnum = request.form['accntnum']
    usr_role = 'none'
    cur.execute("""select ROLE_NAME from user_account where ID_NUM = %s""",
                (accntnum,))
    for item in cur.fetchall():
        usr_role = item[0]
    print 'Account Num is'
    print accntnum
    return rolesprivquery(usr_role)


@app.route('/specificaccountprivuquery', methods=['POST'])
def specificaccountprivuquery():
    db, cur = connectDB()
    accntnum = request.form['accntnum']
    priv = request.form['priv']

    usr_role = 'none'

    cur.execute("""select ROLE_NAME from user_account where ID_NUM = %s""",
                (accntnum,))
    for item in cur.fetchall():
        usr_role = item[0]
        rolename = usr_role
    db, cur = connectDB()
    fileList = []
    print "Roles Name is"
    print rolename
    cur.execute("""select * from role_has_privileges where ROLE_NAME = %s""",
                (rolename,))
    for item in cur.fetchall():
        fileList.append(item)
    query = 'SELECT DISTINCT ROLE_NAME, PRIVILEGE_NAME, PRIVILEGE_TYPE from ' \
            'roles_has_relational_privileges_on_tables'
    cur.execute(
        """SELECT DISTINCT ROLE_NAME, PRIVILEGE_NAME, PRIVILEGE_TYPE from
        roles_has_relational_privileges_on_tables where ROLE_NAME = %s""",
        (rolename,))
    for item in cur.fetchall():
        fileList.append(item)
    print fileList
    for item in fileList:
        for everitem in item:
            if everitem.lower() == priv.lower():
                print rolename + " has " + priv + " privilege"
                return 'Query executed. Check the python console for results.'

    print rolename + " does not have " + priv + " privilege"
    return 'Query executed. Check the python console for results.'


port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(debug=True)
