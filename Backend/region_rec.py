import sqlite3

conn = sqlite3.connect('Backend\PeriodTracker.db') #database path
cur = conn.cursor()


def doctor_region(id):
    cur.execute("select region from doctor where id = ?", (id,))
    district1 =  cur.fetchone()[0]
    cur.execute("select region2 from doctor where id = ?", (id,))
    district2 =  cur.fetchone()[0]
    cur.execute("select region3 from doctor where id = ?", (id,))
    district3 =  cur.fetchone()[0]

    cur.execute("select name from regionInfo where district = ? OR district = ? OR district = ? order by doctor_count", (district1, district2, district3))
    return cur

def ngo_region(id):
    cur.execute("select region from ngo where id = ?", (id,))
    district1 =  cur.fetchone()[0]
    cur.execute("select region2 from ngo where id = ?", (id,))
    district2 =  cur.fetchone()[0]
    cur.execute("select region3 from ngo where id = ?", (id,))
    district3 =  cur.fetchone()[0]
    print(district1, district2, district3)
    cur.execute("select region from ngo where id = ?", (id,))
    district1 =  cur.fetchone()[0]

    cur.execute("select name from regionInfo where district = ? OR district = ? OR district = ? order by ngo_count", (district1, district2, district3))
    return cur

def region_rec(type, id):
    '''
    takes 'doctor' or 'ngo' as argument
    returns list of regions
    '''
    regions = []

    if type == 'doctor':
        doctor_region(id)
           
    elif type == 'ngo':
        ngo_region(id)
        
    x = cur.fetchall()
    for i in x[0:10]:
        regions.append(i[0])

    return regions

#take 3 regions and update
def update_region(type, id, region, region2, region3):
    if type == 'doctor':
        cur.execute("UPDATE doctor SET region = ?, region2 = ?, region3 = ? WHERE  id = ? ", (region, region2, region3, id))
    elif type == 'ngo':
        cur.execute("UPDATE ngo SET region = ?, region2 = ?, region3 = ? WHERE  id = ? ", (region, region2, region3, id))
    conn.commit()


def update_visit(type, region, date):
    if type == 'doctor':
        cur.execute("UPDATE regionInfo SET doctor_count = doctor_count + 1 WHERE name = ?",(region,))
        cur.execute("UPDATE regionInfo SET doctor_visit = ? WHERE name = ?",(date, region))
    elif type == 'ngo':
        cur.execute("UPDATE regionInfo SET ngo_count = ngo_count + 1 WHERE name = ?",(region,))
        cur.execute("UPDATE regionInfo SET doctor_visit = ? WHERE name = ?",(date, region))


update_region_db('doctor', 'D4360', 'Pune', 'Yavatmal', 'Satara')
update_region_db('ngo', 'N5389', 'Sangli', 'Thane', 'Bid')