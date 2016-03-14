from DBHandler import insert_batch_record

def insert_deal_data(conn, values):
	sql = 'insert into deal_data(village_name, house_type, size, orientation, floor, five_only, deal_date, unit_price, total_price) values (%s, %s, %s, %s, %s, %s, %s, %f, %f)'
	insert_batch_record(conn, sql, values)

