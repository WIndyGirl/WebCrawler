from DBHandler import DBHandler

def insert_jianwei_deal_data(conn, values):
	sql = 'insert into jianwei_deal_data(insert_date, verify_num, verify_area, house_verify_num, house_verify_area, sign_num, sign_area, house_sign_num, house_sign_area) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
	
	dbHandler = DBHandler()
	dbHandler.insert_batch_record(conn, sql, values)