START = """
Hello {user_name}! Im <b>{bot_name}</b>, your personal AI chatbot.

Here are the list of commands you can use to manage multiple chats:

/chats - List, view, or modify multiple chats.
/newchat - Start a new chat.
/switchchat - Switch to different chat.
"""

NEW_CHAT = 'Tell me the name of the new chat.'

CHAT_NAME_INVALID = "That's not a valid chat name!"

CHAT_NAME_EXISTS = '<b>{chat_name}</b> already exists!'

NEW_CHAT_DONE = '<b>{chat_name}</b> has been created! Do you want to use this chat?'

SWITCH_CHAT = 'Choose a chat you want to use:'

SWITCHED_CHAT = 'Switched to <b>{chat_name}</b>.'

NO_CHAT = 'You are currently not in a chat. Use /switchchat to switch to other chat.'

NO_CHATS = "You currently don't have any chat. Create one using /newchat."

LIST_CHATS = 'Here are the list of your chats:'

VIEW_CHAT = """
Here is the <b>{chat_name}</b> chat.

<b>INFORMATION</b>
Total Messages - {total_messages}

What do you want to do with this chat?
"""

RENAME_CHAT = 'Tell me the new chat name.'

RENAME_CHAT_DONE = '{chat_name} has been renamed to <b>{new_chat_name}</b>.'

DELETE_CHAT = 'Are you sure you want to delete <b>{chat_name}</b>?'

DELETE_CHAT_DONE = '<b>{chat_name}</b> has been deleted!'
