import sqlite3

conn = sqlite3.connect('Backend\PeriodTracker.db') #database path
cur = conn.cursor()

def reg_recommender(type):
    '''
    takes 'doctor' or 'ngo' as argument
    returns list of regions
    '''
    regions = []

    #######
    
    district1 = 'Pune'
    district2 = 'Chandrapur'

    if type == 'doctor':
        #sort by DOCTOR COUNT
        cur.execute("select name from regionInfo where district = ? OR district = ? order by doctor_count", (district1, district2))
    else:
        cur.execute("select name from regionInfo where district = ? OR district = ? order by ngo_count", (district1, district2))
    
    x = cur.fetchall()
    for i in x[0:10]:
        regions.append(i[0])

    return regions

lst1 = region_rec('ngo')
print(lst1)
lst2 = region_rec('doctor')
print(lst2)

