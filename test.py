from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=True, google_api_key="AIzaSyB8N9kT_rrcNVyYTwdzQYfJGM0YkmOc32Y")


print(model.invoke(
    [
        SystemMessage(content="Answer only yes or no."),
        HumanMessage(content="Is apple a fruit?"),
    ]
))

#print(model.invoke('monday is before tuesday ?').content)

