from prompts import prompt_v1
from run_eval import call_claude

task = "Write a Python script to list all S3 buckets in my AWS account"

print("=== PROMPT SENT ===")
print(prompt_v1(task))

print("=== RESPONSE ===")
response = call_claude(prompt_v1(task))
print(response)
