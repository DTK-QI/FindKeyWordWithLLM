def get_keyword_extraction_prompt(keywords: list, report: str) -> str:
    return f"""
        You are an information extraction system. Your task is to extract sentences that contain the specified keywords from the given text.

        ### Keywords:
        - {", ".join(keywords)}

        ### Text for Analysis:
        ---------------------
        {report}
        ---------------------
        
        ### Matching Rules:
        - **Perform case-insensitive, partial phrase matching.**
        - **Extract the entire sentence that contains the keyword.**
        - **Only include keywords that appear in the text.**
        - **Do not include keywords with empty matches.**
        - **Only include the first matching sentence for each keyword.**
        - **matches must be a string, not a list.**

        ### Output Constraints:
        - **Strictly output only valid JSON format.**
        - **Do not include explanations, analysis, or additional text.**
        - **Each JSON object must have exactly one keyword field.**
        - **Ensure the JSON output is properly formatted.**
        - **Only include keywords that have at least one match.**

        ### Expected Output Format:
        ```
        [
            {{
                "keyword": "[Identified Pattern]",
                "matches": "[Full matching sentence]"
            }}
        ]
        ```
        """
