import psycopg2
import json
import csv

conn = psycopg2.connect(dbname="tesloop", user="tesread", password="tesread", \
						host="tesla-vehicle-api-db.ct6ob3lecz50.us-west-2.rds.amazonaws.com", port="5432")

print("Opened database successfully")

cur = conn.cursor()

########################################	vehicle_data 	########################################
#      Column     |            Type             | Modifiers | Storage  | Stats target | Description 
# ----------------+-----------------------------+-----------+----------+--------------+-------------
#  vehicle        | integer                     | not null  | plain    |              | 
#  timestamp      | timestamp without time zone | not null  | plain    |              | 
#  mobile_enabled | boolean                     | not null  | plain    |              | 
#  charge_state   | json                        | not null  | extended |              | 
#  climate_state  | json                        | not null  | extended |              | 
#  drive_state    | json                        | not null  | extended |              | 
#  gui_settings   | json                        | not null  | extended |              | 
#  vehicle_state  | json                        | not null  | extended |              | 
#  charger        | character varying           |           | extended |              | 
# Indexes:
#     "vehicle_timestamp" btree (vehicle, "timestamp")
# Foreign-key constraints:
#     "vehicle_data_vehicle_fkey" FOREIGN KEY (vehicle) REFERENCES vehicle(id)
####################################################################################################

# json object charge_state has 41 features:
		 # charge_enable_request
		 # battery_level
		 # charger_phases
		 # usable_battery_level
		 # managed_charging_start_time
		 # charger_actual_current
		 # managed_charging_active
		 # charger_pilot_current
		 # charging_state
		 # charge_port_door_open
		 # fast_charger_type
		 # user_charge_enable_request
		 # charge_miles_added_ideal
		 # scheduled_charging_start_time
		 # managed_charging_user_canceled
		 # scheduled_charging_pending
		 # charger_power
		 # fast_charger_present
		 # charge_energy_added
		 # charger_voltage
		 # battery_range
		 # charge_rate
		 # time_to_full_charge
		 # charge_limit_soc
		 # battery_current

	# which ones to use?

# json object climate_state has 16 features:
		 # driver_temp_setting
		 # passenger_temp_setting
		 # smart_preconditioning
		 # seat_heater_rear_left
		 # is_auto_conditioning_on
		 # is_front_defroster_on
		 # seat_heater_rear_right_back
		 # seat_heater_rear_left_back
		 # fan_status
		 # outside_temp
		 # seat_heater_rear_center
		 # seat_heater_left
		 # seat_heater_rear_right
		 # inside_temp
		 # is_rear_defroster_on
		 # seat_heater_right

	# which ones to use?

# json object vehicle_state has 39 fields
		 # car_type
		 # autopark_style
		 # sun_roof_installed
		 # rt
		 # odometer
		 # valet_pin_needed
		 # api_version
		 # pr
		 # dark_rims
		 # df
		 # has_spoiler
		 # roof_color
		 # autopark_state
		 # center_display_state
		 # perf_config
		 # remote_start
		 # rhd
		 # homelink_nearby
		 # wheel_type
		 # car_version
		 # calendar_supported
		 # rear_seat_heaters
		 # exterior_color
		 # autopark_state_v2
		 # ft
		 # sun_roof_percent_open
		 # spoiler_type
		 # remote_start_supported
		 # pf
		 # third_row_seats
		 # notifications_supported
		 # locked
		 # valet_mode
		 # sun_roof_state
		 # parsed_calendar_supported
		 # last_autopark_error
		 # seat_type
		 # vehicle_name
		 # dr

	# which ones to use?

# json object drive_state has 6 features:
		 # shift_state
		 # speed
		 # gps_as_of
		 # heading
		 # longitude
		 # latitude
	# Which ones to use?
# 
cur.execute("SELECT * FROM vehicle_data LIMIT 1;")
row = cur.fetchone()
charge_features = row[3]
climate_features = row[4]
drive_features = row[5]

# header = ["vehicle", "timestamp", "mobile_bool"]
header = charge_features.keys()
print(header)
# header += climate_features.keys()
# header += drive_features.keys()
# header.append("third_row_seats")
# header.append("odometer")
# header.append("charger")

cur.execute("SELECT * FROM vehicle_data ORDER BY timestamp LIMIT 1000")
rows = cur.fetchall()
for row in rows:
	print(row[3]['usable_battery_level'])


# with open('battery_data_v2.csv', 'w') as csvfile:
# 	writer = csv.writer(csvfile)
# 	writer.writerow(header)
# 	for row in rows:
# 		toWrite = []
		# toWrite += list(row[3].values())
	# 	print(list(row[3].values())[0:5])
		# print(list(row[3].values())[22])

		# toWrite.append(list(row[3].values()))
		# toWrite.append(row[1])
		# toWrite.append(row[2])
		# toWrite += list(row[3].values()) + list(row[4].values()) + list(row[5].values())
		# toWrite.append(row[7]["third_row_seats"])
		# toWrite.append(row[7]["odometer"])		
		# toWrite.append(row[8])
		# writer.writerow(toWrite)


