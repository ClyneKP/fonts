from nyct_gtfs import NYCTFeed
from datetime import datetime
from datetime import timedelta
import pandas as pd


# Load the realtime feed from the MTA site
feed = NYCTFeed("1", api_key="5HALW1Qsr378eOdLSBoa43GXXwzI3h5H3HjtsYNp")

#237 = Grand Army Plaza
stop_ids = ["237N","237S"]

trains = feed.filter_trips(line_id=["2","3","4","5"], headed_for_stop_id=stop_ids)

df = pd.DataFrame()
for i,train in enumerate(trains):
    stops = train.stop_time_updates
    filtered = [stop for stop in stops if stop.stop_id in stop_ids]
    train_arr = filtered[0].arrival
    now = datetime.now()
    delta = train_arr - now
    time = delta.total_seconds() / 60
    mins = int(round(time,0))
    #print(train.route_id)
    #print(train.headsign_text)
    #print(mins)
    obj = pd.Series({'Route':train.route_id,'Headsign':train.headsign_text,"Mins":mins})
    df = pd.concat([df,obj.to_frame().T], ignore_index=True)
    
df.sort_values(by=['Mins'])