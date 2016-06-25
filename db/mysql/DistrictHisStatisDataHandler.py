from DBHandler import DBHandler

def insert_district_his_statistics_data(conn, values):
	sql = 'insert into district_his_statistics_data(insert_date, district, district_avarage_price, deal_in_last_month, on_sale, deal_in_90_days, deal_in_yesterday, daikan_in_yesterday, daika_rate) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
	
	dbHandler = DBHandler()
	dbHandler.insert_batch_record(conn, sql, values)