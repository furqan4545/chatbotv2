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

        response = requests.get(f"http://localhost:5000/order_status/{order_n}")
        print(response)
        print(response[0]["particular"])

        respon = f'Here are the tracking detail of your product: {response[0]["particular"]}'
        dispatcher.utter_message(respon)
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






