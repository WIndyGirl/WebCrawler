from DBHandler import DBHandler

def insert_history_statistics_data(conn, values):
	sql = 'insert into history_statistics_data(insert_date, on_sale, deal_in_90_days, deal_in_yesterday, daikan_in_yesterday, new_added_house_yesterday, new_added_customer_yesterday) values (%s, %s, %s, %s, %s, %s, %s)'
	
	dbHandler = DBHandler()
	dbHandler.insert_single_record(conn, sql, values)