#!/usr/bin/python
""" Example usage of iRWebStats """
from ir_webstats import constants as ct
from ir_webstats.client import iRWebStats
from ir_webstats.util import clean
from datetime import datetime



user = ''  # iRacing username and password
password = ''
irw = iRWebStats()
irw.login(user, password)
if not irw.logged:
    print (
        "Couldn't log in to iRacing Membersite. Please check your credentials")
    exit()

# Cars driven by user
drivers, total_drv = irw.driver_search(
    race_type=ct.RACE_TYPE_ROAD, active=True, page=1)

print
print("Total drivers found: %s. Showing the first %s" % (total_drv,
                                                         len(drivers)))
print("\n".join(["%s - %s: %s (%s)" % (i + 1, clean(x['displayname']), x['irating'], x['custid'])
                for i, x in enumerate(drivers)]))
print

r = irw.cars_driven()  # Returns cars id
people = list();
tracks = set();
for x in drivers:
    id = int(x['custid'])
    for carId in r:
        if 'Global Mazda MX-5 Cup' in irw.CARS[carId]['name']:
            res = irw.personal_best(custid=id, carid=carId);
            people.append((x['displayname'], (res)));

            # print res
            for track in res:
                tracks.add((track['trackname'], track['trackconfigname']))

for (trackname, trackconfig) in tracks:
    trackFullName = clean(trackname) + ' ' + clean(trackconfig);
    times = list()
    for (username, user_pbs) in people:
        times = list()
        times.append(datetime.strptime('59:59.999', '%M:%S.%f'))
        for pb in user_pbs:
            if pb['trackname'] == trackname and pb['trackconfigname'] == trackconfig:
                time = datetime.strptime('59:59.999', '%M:%S.%f')
                pb_time = clean(pb['bestlaptimeformatted'])
                try:
                    time = datetime.strptime(pb_time, '%M:%S.%f')
                except:
                    pass
                try:
                    time = datetime.strptime(pb_time, '%S.%f')
                except:
                    pass
                if time.minute == 0 and time.second == 0:
                    time = datetime.strptime('59:59.999', '%M:%S.%f')
                times.append(time)

        min_time = min(times);
        if min_time.minute != 59 or min_time.second != 59:
            print clean(username) + '\t' + min_time.strftime('%M:%S.%f') + '\t' + trackFullName
    print

