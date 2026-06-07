from modules.chatbot import FashionChatbot

bot = FashionChatbot()

tests = [
    "Hi! What's your return policy?",
    "Can you track my order ORD-10034?",
    "I'm looking for something casual for a summer brunch, budget around £60",
]

for q in tests:
    print(f"\n👤 {q}")
    result = bot.chat(q)
    print(f"🤖 [{result['intent'].upper()}] {result['reply']}")
    print(f"   (tokens used: {result['tokens']})")