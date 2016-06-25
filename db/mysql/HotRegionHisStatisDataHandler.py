from DBHandler import DBHandler

def insert_host_region_his_statistics_data(conn, values):
	sql = 'insert into hot_region_his_statistics_data(insert_date, region_name, region_avarage_price, on_sale, deal_in_90_days, added_in_7_days, daikan_in_7_days, deal_in_last_month, deal_compare_last_month, deal_compare_last_year) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
	
	dbHandler = DBHandler()
	dbHandler.insert_batch_record(conn, sql, values)