# TO TEST THE BOT
# def sample_responses(input_text):
# 	user_message = input_text.lower()

# 	# 'hi' in - means if string has hi keyword then 'yo' will be returned for eg: it'll even work for Hi I'm a Student. 
# 	if 'hi' in user_message:
# 		return 'yo'
# 	if 'how are you' in user_message:
# 		return 'I am fine'
# 	else :
# 		return "I do no know what are you talking about"

import requests, json
def sample_responses(input_text):

	# PRINTING USER'S GIVEN INPUT
	user_message = str(input_text).lower()
	print(user_message)

	# 395:24-08-2021 is the format python will understand
	new_data = user_message.split(':')
	pin = new_data[0]
	date = new_data[1]
	try:
		pin = int(pin)
	except Exception as e:
		pass
	if(int(pin)<10000 and int(pin)>0):

		url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={pin}&date={date}'
		browser_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
		print(url)
		response = requests.get(url, headers=browser_header)
		print(response)
		json_data = response.json()
		final_text = ''
		if len(json_data['sessions'])==0:
			print("\nSlots Not Available\n")
		else:
			for slots in json_data['sessions']:
				final_text = final_text + "\nName: "+str(slots['name']) +'\n'+ "Available Capacity: "+str(slots['available_capacity']) +'\n' + "Min Age Limit: "+str(slots['min_age_limit']) +'\n' + "Vaccine: "+str(slots['vaccine'])+ '\n'
				final_text = final_text + '----------------------------------------'

		return final_text
		# try this for tekegram chat
		# if final_text == 'Slots Not Available':
		# 	print('Slots Not Available')
	else:
		return "Invalid input"