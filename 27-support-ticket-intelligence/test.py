from app import classify

assert classify("Payment charged twice")["category"] == "billing"
assert classify("The app has a critical error")["priority"] == "high"
assert classify("I am frustrated with delivery")["tone"] == "negative"
assert classify("Please share more information")["category"] == "general"
print("Support ticket intelligence tests passed")
