import sqlite3

conn = sqlite3.connect('PeriodTracker.db', check_same_thread=False) #database path
cur = conn.cursor()


def regions(type, id):
    '''
    takes 'doctor' or 'ngo' as argument
    returns list of regions
    '''
    reg_list = []

    if type == 'doctor':
        cur.execute("select region from doctor where id = ?", (id,))
        district1 =  cur.fetchone()[0]
        cur.execute("select region2 from doctor where id = ?", (id,))
        district2 =  cur.fetchone()[0]
        cur.execute("select region3 from doctor where id = ?", (id,))
        district3 =  cur.fetchone()[0]

        cur.execute("select name from regionInfo where district = ? OR district = ? OR district = ? order by doctor_count", (district1, district2, district3))
        
           
    elif type == 'ngo':
        cur.execute("select region from ngo where id = ?", (id,))
        district1 =  cur.fetchone()[0]
        cur.execute("select region2 from ngo where id = ?", (id,))
        district2 =  cur.fetchone()[0]
        cur.execute("select region3 from ngo where id = ?", (id,))
        district3 =  cur.fetchone()[0]

    cur.execute("select name from regionInfo where district = ? OR district = ? OR district = ? order by ngo_count", (district1, district2, district3))
        
    x = cur.fetchall()
    for i in x[0:10]:
        reg_list.append(i[0])
    return reg_list


def update_visit(type, region, date):
    if type == 'doctor':
        cur.execute("UPDATE regionInfo SET doctor_count = doctor_count + 1 WHERE name = ?",(region,))
        cur.execute("UPDATE regionInfo SET doctor_visit = ? WHERE name = ?",(date, region))
    elif type == 'ngo':
        cur.execute("UPDATE regionInfo SET ngo_count = ngo_count + 1 WHERE name = ?",(region,))
        cur.execute("UPDATE regionInfo SET ngo_visit = ? WHERE name = ?",(date, region))
    conn.commit()