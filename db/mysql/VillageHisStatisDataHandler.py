from DBHandler import insert_single_record

def insert_village_his_statistics_data(conn, values):
	sql = 'insert into village_his_statistics_data(insert_date, village_name, village_avarage_price, on_sale, deal_in_90_days, daikan_in_30_days) values (%s, %s, %s, %s, %s, %s)'
	insert_single_record(conn, sql, values)