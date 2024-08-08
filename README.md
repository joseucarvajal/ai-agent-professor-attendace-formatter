# Short description
Langraph agent to support college professor related tasks, specifically to take a CSV file and load a different format of this file to another one with grades calculations, percentajes on Google Sheets.

The code fraction to get the JSON from CSV file is prone to improvements, it should be an automation instead of a prompt in order to save resources and avoid roundtrips to the ChatGPT LLM model, however, it was implemented that way because of demo purposes

# Technical debt
1. Use the LangGraph tools to create a tool for Google SpreadSheets integration instead of node routines
2. Integrate Google Sheets in a seamless way, maybe with a prompt, instead of automation code
3. Build a Graphic UI to interact with the agent
