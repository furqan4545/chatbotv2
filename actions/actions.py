# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests
import json
import datetime
from rasa_sdk.events import ReminderScheduled

class ActionCheckWeather(Action):
   def name(self) -> Text:
      return "action_check_weather"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         loc = tracker.get_slot('location')

         if loc == None:
            response = f'Can you please provide the location for which you want to check weather?'
         else:
            response = f'The weather in {loc} is good'
         dispatcher.utter_message(response)
         return []

class ActionCheckName(Action):
   def name(self) -> Text:
      return "action_check_name"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot('PERSON')

        response = f'Hi Mr. {name}, How are you? I am Jarvis, your ecom support. Welcome to our website, how may I help you today?'
        dispatcher.utter_message(response)
        return []

class ActionTrackOrder(Action):
   def name(self) -> Text:
      return "action_fetch_OD"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        order_n = tracker.get_slot('order_n')
        print("here is on : ", order_n)

        response = requests.get(f"http://localhost:5000/order_status/{order_n}")
        response = response.json()
        print(response["particular"])

        respon = f'Here are the tracking detail of your product: {response["particular"]}'
        dispatcher.utter_message(respon)
        return []

class ActionOfferDiscount(Action):
   def name(self) -> Text:
      return "action_offer_discount"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        product = tracker.get_slot('product')
        reason = tracker.get_slot('reason_expensive')
        print("here is on : ", product)
        print("here is 2 : ", reason)

        if product != None and reason != None:
            response = f"I am glad that you are interested in buying {product} from us. Would you be happy if offer you 10% discount?"
        elif product != None and reason == None:
            response = f"I am happy to hear that. Please tell me how can I help you with buying {product}"
        elif product == None and reason != None:
            response = f"I see. Would you be happy if offer you 10% discount on {product}"

        # respon = f'Here are the tracking detail of your product: {response["particular"]}'
        dispatcher.utter_message(response)
        return []

class ActionSearchProduct(Action):
   def name(self) -> Text:
      return "action_search_product"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        product = tracker.get_slot('product')
        cx_range = tracker.get_slot('cx_range')
        print("here is on : ", product)
        print("here is 2 : ", cx_range)

        if product == None and cx_range == None:
            response = f"What product would you like to buy?"
        elif product != None and cx_range != None:
            response = f"I would love to help you in finding {product} within a range of {cx_range}. Let me quickly search it for you."
        elif product != None and cx_range == None:
            response = f"I will help in finding the {product}. Could you please tell me your price range?"
        elif product == None and cx_range != None:
            response = f"Thanks for telling me your range. Let me quickly search the product for you"

        # respon = f'Here are the tracking detail of your product: {response["particular"]}'
        dispatcher.utter_message(response)
        return []

class ActionSuggestProduct(Action):
   def name(self) -> Text:
      return "action_suggest_product"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        product = tracker.get_slot('product')
        cx_range = tracker.get_slot('cx_range')
        print("here is on : ", product)
        print("here is on : ", cx_range)

        response = requests.get(f"http://localhost:5000/products/{product}/{cx_range}")
        response = response.json()
        product_id = []
        pr_price = []
        for i in range(len(response)):
            product_id.append(response[i]["id_product"])
            pr_price.append(response[i]["product_price"])
            print(response[i]["id_product"])
            print(response[i]["product_price"])

        respon = f'Here are list of some product IDs : {product_id} with price range {pr_price}. Please search them in search bar.'
        dispatcher.utter_message(respon)
        return []

class ActionEmailAddress(Action):
   def name(self) -> Text:
      return "action_ask_email"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        order = tracker.get_slot('order_n')
        c_need = tracker.get_slot('c_need')
        print("here is on : ", order)
        print(c_need)
        
        if order == None and c_need != None:
            response= "Can you please provide me the order number?"
        elif c_need == None and order != None:
            response= "Can you please tell me whether you like refund or replacement for the order?"
        elif order != None and c_need != None:
            response= "Thanks for the information. May I also have your contact number and email address please?"    
        else:
            response = "Sorry I didn't get your message, can you please rephrase"

        dispatcher.utter_message(response)
        return []


class ActionJotComplain(Action):
   def name(self) -> Text:
      return "action_jot_complain"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        c_reason = tracker.get_slot('c_reason')
        order = tracker.get_slot('order_n')
        c_need = tracker.get_slot('c_need')
        email = tracker.get_slot('email')
        cn = tracker.get_slot('cn')
        msg = c_reason +" need "+ c_need 
        print("here is on : ", order)
        print(c_reason)
        print("here is on : ", c_need)
        print("here is on : ", email)
        print("here is on : ", cn)
        print(msg)

        if email == None and cn != None:
            response= "May I know your email address Please?"
        elif email != None and cn == None:
            response= "Can you please provide me your contact number?"
        elif order != None and c_need != None and email != None and cn != None:
            header = {'Content-Type': 'application/json'}
            payload = {
                    "email": email,
                    "cn": cn,
                    "msg": msg,
                    "order_n": order 
                }
            res = requests.post("http://localhost:5000/file_complain", headers=header, data=json.dumps(payload))
            print(res.text)
            response= "Thanks for the data. I have jotted down your complain and resolution. Our customer support team will reach out to you with resolution within 48 hours"
        
        else:
            response = "Sorry I didn't get your message, can you please rephrase"

        dispatcher.utter_message(response)
        return []

class ActionSetReminder(Action):
    """Schedules a reminder, supplied with the last message's entities."""

    def name(self) -> Text:
        return "action_set_reminder"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("I will remind you in 5 seconds.")

        date = datetime.datetime.now() + datetime.timedelta(seconds=20)
        entities = tracker.latest_message['text']
        # entities = tracker.get_slot('PERSON')

        reminder = ReminderScheduled(
            "EXTERNAL_reminder",
            trigger_date_time=date,
            entities=entities,
            name="my_reminder",
            kill_on_user_message=False,
        )

        return [reminder]


class ActionReactToReminder(Action):
    """Reminds the user to call someone."""

    def name(self) -> Text:
        return "action_react_to_reminder"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        name = tracker.get_slot("PERSON")
        print("sdaSAd"+ name)
        dispatcher.utter_message(f"Remember to call {name}")

        return []


class ActionPullOD(Action):
    """Schedules a reminder, supplied with the last message's entities."""

    def name(self) -> Text:
        return "action_pull_OD"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("Let me go ahead and pull up your order details.")

        date = datetime.datetime.now() + datetime.timedelta(seconds=20)
        entities = tracker.latest_message['text']
        # entities = tracker.get_slot('PERSON')

        reminder = ReminderScheduled(
            "EXTERNAL_reminder",
            trigger_date_time=date,
            entities=entities,
            name="my_reminder",
            kill_on_user_message=False,
        )

        return [reminder]

class ActionReactToOD(Action):
    """Reminds the user to call someone."""

    def name(self) -> Text:
        return "action_react_to_OD"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        name = tracker.get_slot("PERSON")
        print("sdaSAd"+ name)
        dispatcher.utter_message(f"Remember to call {name}")

        return []






