# importing our Constants.py file and keys from it where API_KEY is store
import Constants as keys
import responses as R
from telegram.ext import *
import requests, json

print('Bot is starting')

# When bot starts it prints this
def start_command(update, context):
	update.message.reply_text("Yo, Welcome to this bot ! ")

def vaccine_command(update, context):

	# pin means district_id where 395 is of mumbai
	pin = '170'
	date = '24-8-2021'
	url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={pin}&date={date}'

	# Cowin api wont give back a response without user-agent
	browser_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
	# browser_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
	print(url)
	
	response = requests.get(url, headers=browser_header)
	print(response)
	# convert the response in json
	json_data = response.json()
	final_text = ''
	if len(json_data['sessions'])==0:
		print("\nSlots Not Available\n")
	else:
		for slots in json_data['sessions']:
			final_text = final_text + "\nName: "+str(slots['name']) +'\n'+ "Available Capacity: "+str(slots['available_capacity']) +'\n' + "Min Age Limit: "+str(slots['min_age_limit']) +'\n' + "Vaccine: "+str(slots['vaccine'])+ '\n'
			final_text = final_text + '----------------------------------------'
	update.message.reply_text(final_text)


# to respond
def handle_message(update, context):

	# text is message sent by the user
	text = str(update.message.text).lower()

	# user is the person's who's sending the text
	user = update.effective_user
	print(f'{user["username"]}: {text}')
	
	# give the text message to the response which will go the func sample_responses in responses.py
	response = R.sample_responses(text)
	print(f'Bot: {response}')
	update.message.reply_text(response)

# to handle error
def error(update, context):
	print(f"Update {update} caused error {context.error}")

def main():
	# Updater is the method used by telegram
	updater = Updater(keys.API_KEY, use_context=True)
	dp = updater.dispatcher

	# if "/start" command is given then start_command func pf main.py will work
	dp.add_handler(CommandHandler("start", start_command))

	#dp.add_handler(CommandHandler("help", help_command))
	dp.add_handler(CommandHandler("vaccine", vaccine_command))

	# MessageHandler returns that defult big guide message when irrevelant things are typed
	dp.add_handler(MessageHandler(Filters.text, handle_message))
	dp.add_error_handler(error)


	updater.start_polling()
	updater.idle()

main()