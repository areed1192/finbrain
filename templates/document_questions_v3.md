# Agent Question Template

## Constraints and Guidelines

- Each question must be answered accurately based on the information provided earlier in the conversation.
- It should be in a structured JSON format that matches the provided schema.
- The confidence level must be clearly stated and justified with supporting evidence.

## Task

Based on all the documents you've seen, answer the following questions in the specified format:

<QUESTIONS_BEING_ASKED>
{questions_to_ask}
<QUESTIONS_BEING_ASKED>

Make sure to reference the following documents in your answers:

<DOCUMENTS_TO_REFERENCE>
{documents_to_reference}
<DOCUMENTS_TO_REFERENCE>

The JSON object below includes every key that needs to be part of the output. My job depends on getting accurate and consistent answers in the correct format that customers can use.

<JSON_STRUCTURE>
{{
  "questions_and_answers": [
    {{
    "question": "",
    "answer": "",
    "confidence_level": "",
    "confidence_score": 0.00,
    "supporting_evidence": "",
    "document_references": ["Document 1", "Document 2"],
    "answer_explanation": ""
    }},
{{
    "question": "",
    "answer": "",
    "confidence_level": "",
    "confidence_score": 0.00,
    "supporting_evidence": "",
    "document_references": ["Document 1", "Document 2"],
    "answer_explanation": ""
    }},
// Repeat for each question
]
}}
<JSON_STRUCTURE>

Along with the JSON schema it must adhere to, a validation process will be run to ensure the correctness of the output.

<JSON_SCHEMA>
{{
  "type": "object",
  "properties": {{
    "questions_and_answers": {{
      "type": "array",
      "items": {{
          "type": "object",
          "properties": {{
          "question": {{
            "type": "string"
          }},
          "answer": {{
            "type": "string"
          }},
          "confidence_level": {{
            "type": "string"
          }},
          "confidence_score": {{
            "type": "number",
            "minimum": 0.0,
            "maximum": 1.0
          }},
          "supporting_evidence": {{
            "type": "string"
          }},
          "document_references": {{
            "type": "array",
            "items": {{
              "type": "string"
            }}
          }},
          "answer_explanation": {{
            "type": "string"
          }}
          }},
        "required": [
          "question", "answer", "confidence_level", "confidence_score", "supporting_evidence", "document_references", "answer_explanation"
        ]
      }}
    }}
  }},
  "required": ["questions_and_answers"]
}}
<JSON_SCHEMA>

Please output the information in a well-formatted and valid structured JSON object without using markdown code blocks or comments in the JSON.
