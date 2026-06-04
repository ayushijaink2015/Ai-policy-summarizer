from app.services.summarization_service import summarize_text

sample_text = """
The Government of India has launched a new digital education policy.
The policy aims to improve access to online learning resources,
enhance teacher training, and provide affordable digital infrastructure
to students in rural areas.
"""

summary = summarize_text(sample_text)

print("SUMMARY:")
print(summary)