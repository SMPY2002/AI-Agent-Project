# Importing Necessary Libraries
import json
import streamlit as st
import pandas as pd
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re
import requests
import time
from groq import Groq
from dotenv import load_dotenv
import os

# <------------------ Main App ------------------>


# Configuring API Keys and Credentials using .env file
load_dotenv()
# Google OAuth setup variables
# Load client secrets from Streamlit Secrets

client_secret_json = st.secrets["CLIENT_SECRET"]  # Retrieve the string
CLIENT_SECRETS_FILE = json.loads(client_secret_json)  # Parse the string as JSON

# OAuth client secrets file from Google Cloud Console
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
# Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
# API Key for SerpAPI
SERPAPI_KEY = os.getenv("SERP_API_KEY")


# <---------------------------- Helper Functions - 1 (Start)------------------------------------>

# Helper function: Fetch data from Google Sheets

def fetch_google_sheet_data(credentials, spreadsheet_id, sheet_range):
    try:
        service = build("sheets", "v4", credentials=credentials)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=sheet_range).execute()
        data = result.get("values", [])
        if not data:
            st.warning("No data found in the specified range.")
            return None
        df = pd.DataFrame(data[1:], columns=data[0])  # First row is the header
        return df
    except HttpError as error:
        st.error(f"Error loading Google Sheet: {error}")
        return None

# Helper function: Authenticate with Google
def authenticate_with_google():
    try:
        flow = Flow.from_client_config(
            CLIENT_SECRETS_FILE,
            scopes=SCOPES,
            redirect_uri="https://ai-info-retrieval.streamlit.app/"  # using ngrok provided url for https connection
        )
        auth_url, state = flow.authorization_url(prompt='consent')
        st.write(f"[Click here to authenticate with Google Sheets]({auth_url})")

        query_params = st.experimental_get_query_params()
        auth_code = query_params.get("code")
        if auth_code:
            flow.fetch_token(code=auth_code[0])
            st.session_state.credentials = flow.credentials
            st.success("Authentication successful! You can now access your Google Sheet.")
    except Exception as e:
        st.error(f"Authentication failed: {e}")


# Helper function: Extract Google Sheet ID from URL
def extract_sheet_id(sheet_url):
    match = re.search(r"/d/([a-zA-Z0-9-_]+)", sheet_url)
    if match:
        return match.group(1)
    st.error("Invalid Google Sheet URL. Please check the URL and try again.")
    return None

# </---------------------------------- Helper Functions - 1 (end)-------------------------------------->


# <------------------ Helper Functions - 2 (For Web searching using SerpAPI)  (start)------------------>

# Helper function: Perform a web search using SerpAPI
def search_web(query):
    try:
        url = f"https://serpapi.com/search.json?engine=google&q={query}&api_key={SERPAPI_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("organic_results", [])
    except requests.exceptions.RequestException as e:
        st.error(f"Error in web search: {e}")
        return []

# Helper function: Format search results for display
def format_search_results(results):
    formatted_results = ""
    for entity, entity_results in results.items():
        formatted_results += f"\nResults for '{entity}':\n"
        for result in entity_results:
            formatted_results += (
                f"- Title: {result['title']}\n"
                f"  Link: {result['link']}\n"
                f"  Snippet: {result['snippet']}\n"
            )
    return formatted_results

# </------------------------------ Helper Functions - 2 (end)--------------------------------->


# <-------------------------------- Main App Function (start)--------------------------------->

# Main function
def main():
    st.title("Automated Web Search and Data Retrieval")
    
    # Step 1: Choose between CSV upload or Google Sheets connection
    option = st.radio("Choose your data source:", ("Upload CSV", "Connect to Google Sheets"))
    df = None

    # Upload CSV file option selected
    if option == "Upload CSV":
        csv_file = st.file_uploader("Upload a CSV file", type="csv")
        if csv_file is not None:
            try:
                value = st.number_input("Enter the number of rows to fetch from CSV: (min:1 is required)", min_value=1, max_value=1000)
                df = pd.read_csv(csv_file).head(value)
                st.write("### CSV Data Preview")
                st.dataframe(df)        # Displaying the data in tabular format
            except Exception as e:
                st.error(f"Error reading CSV file: {e}")

    # Connect to Google Sheets option selected
    elif option == "Connect to Google Sheets":
        if "credentials" not in st.session_state:
            authenticate_with_google()

        if "credentials" in st.session_state and st.session_state.credentials:
            sheet_url = st.text_input("Enter Google Sheet URL:")
            sheet_range = st.text_input("Enter sheet range (e.g., 'Sheet1!A1:D10'):").strip()

            if sheet_url and sheet_range:
                spreadsheet_id = extract_sheet_id(sheet_url)
                if spreadsheet_id:
                    df = fetch_google_sheet_data(st.session_state.credentials, spreadsheet_id, sheet_range)
                    if df is not None:
                        st.write("### Google Sheet Data Preview")
                        st.dataframe(df.head(10)) # Displaying the data in tabular format

    # If data is loaded, proceed with the rest of the app
    if df is not None:
        # Step 2: Dynamic Query Input by user
        dynamic_query = st.text_input("Enter your query (use placeholders like {company} to select any column on which search will work):")
        if dynamic_query:
            match = re.search(r"{(.*?)}", dynamic_query)
            if match:
                column_name = match.group(1)
                if column_name in df.columns:
                    st.info(f"Detected column for query: {column_name}")

                    # Step 3: Perform Web Search and Groq query for extracted responses (LLM integration for information extraction)
                    def query_groq_with_results(results, user_query):
                        formatted_results = format_search_results(results)
                        messages = [
                            {"role": "system", "content": "You are a highly intelligent assistant specializing in extracting exact information from search results,based on the user_query. Analyze the provided results and extract the exact and concise information. Include only details directly related to the query, avoiding unrelated or excessive information.If information is not available, then simply show Information not found!."},
                            {"role": "user", "content": f"Search Results:\n{formatted_results}\n\nUser Query: {user_query}"},
                        ]
                        response = client.chat.completions.create(
                            model="gemma2-9b-it",  # Google LLM model
                            messages=messages,
                            temperature=0.7,
                            max_tokens=512,
                            stream=True,
                        )
                        final_response = "".join(chunk.choices[0].delta.content or "" for chunk in response)
                        return final_response

                    # Create results for all entities of the main column and prepare the final output
                    if df is not None and dynamic_query:
                        match = re.search(r"{(.*?)}", dynamic_query)
                        if match:
                            column_name = match.group(1)
                            if column_name in df.columns:
                                st.info(f"Compiling Result for each entity of : {column_name}..")

                                # Perform search and extraction
                                extracted_data = []
                                results = {}
                                for entity in df[column_name]:
                                    query = dynamic_query.replace(f"{{{column_name}}}", str(entity))
                                    search_results = search_web(query)
                                    entity_results = [
                                        {"title": res.get("title"), "link": res.get("link"), "snippet": res.get("snippet")}
                                        for res in search_results[:3]
                                    ]
                                    results[entity] = entity_results

                                    # Query Groq for the specific entity
                                    extracted_response = query_groq_with_results(results, query)
                                    extracted_data.append({
                                        "Entity": entity,
                                        "Extracted Information": extracted_response.strip()
                                    })
                                    time.sleep(2)  # Avoid overloading the API

                                # Convert to DataFrame and display
                                extracted_df = pd.DataFrame(extracted_data)
                                st.write("### Displaying the Data in Tabular Format")
                                st.dataframe(extracted_df)

                                # Provide CSV download option
                                csv_data = extracted_df.to_csv(index=False).encode('utf-8')
                                st.download_button(
                                    label="Download Retrived Information as CSV",
                                    data=csv_data,
                                    file_name=f"extracted_data_for_{column_name}.csv",
                                    mime="text/csv" 
                                )
                                # Show this message after click on download button
                                if st.button("Download Retrived Information as CSV"):
                                    st.success("Downloaded Successfully")
                            else:
                                st.warning(f"Column '{column_name}' not found in the data.")
                        else:
                            st.warning("Please include a placeholder like {column_name} in your query.")
                    else:
                        st.info("Enter a query to generate results.")

if __name__ == "__main__":
    main()

# <-------------------------------- Main App Function (end)--------------------------------->

