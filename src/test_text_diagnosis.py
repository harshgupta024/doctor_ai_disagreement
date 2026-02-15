from text_diagnosis import extract_text_diagnosis

report1 = "No acute cardiopulmonary abnormality."
report2 = "Patchy opacity in the right lower lobe suggestive of pneumonia."

print(extract_text_diagnosis(report1))
print(extract_text_diagnosis(report2))
