# **Automated Web Search and Data Retrieval System**

## **Overview**
This project automates information retrieval from the web for entities listed in a dataset. Designed with simplicity and efficiency in mind, it provides a user-friendly interface to upload datasets or connect to a Google Sheet, define custom prompts, and retrieve structured results dynamically.

The project is built using cutting-edge technologies like Groq API for natural language understanding, SerpAPI for web searches, and Streamlit for the user interface.

---

## **Features**
- **Data Input Options**: Upload a CSV file or connect to a Google Sheet for real-time data processing.
- **Dynamic Querying**: Define custom search prompts using placeholders (e.g., `{company}`) to extract relevant information dynamically.
- **Seamless Information Retrieval**: Uses Groq API and SerpAPI to perform searches and return accurate, structured data.
- **User-Friendly Dashboard**: View extracted results in a clean tabular format and download them as a CSV file.
- **Error Handling**: Provides user-friendly feedback for invalid inputs or configuration errors.

---

## **Tech Stack**
- **Frontend/UI**: Streamlit
- **Backend**: Python
- **APIs**: 
  - Groq API for natural language processing.
  - SerpAPI for performing web searches.
  - Google Sheets API for real-time spreadsheet integration.

---

## **Prerequisites**
Ensure the following are installed and configured:
1. **Python**: Version 3.8 or higher.
2. **API Access**: 
   - Groq API Key.
   - SerpAPI Key.
3. **Google Cloud Project**: 
   - Enable Google Sheets API and Google Drive API.
   - Download the OAuth credentials JSON file.
4. **Libraries**: Listed in the `requirements.txt` file.

---

## **Setup Instructions**

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```
---

### **Step 2: Install Dependencies**
Install the required Python libraries using:
```bash
pip install -r requirements.txt
```
---

### **Step 3: Configure Environment Variables**
1. Create a .env file in the root directory.
2. Add the following details:
   ```plaintext
   GROQ_API_KEY=your_groq_api_key
   SERP_API_KEY=your_serp_api_key
   GOOGLE_CLIENT_SECRET=your_google_client_secret_file.json
   ```
3. Ensure .env is listed in .gitignore to avoid exposing sensitive data.
---

### **Step 4: Run the Application**
Start the Streamlit application:
```bash
streamlit run app/main_app.py
```

---

## **Usage Guide**
1. Choose Data Source:
  - Upload a CSV file or connect to a Google Sheet.
2. Define a Query:
  - Use a placeholder (e.g., {entity_name}) for dynamic searches.
  - Example Prompt: "Find the latest revenue details of {company}".
3. View Results:
  - The dashboard displays extracted data in a table.
  - Use the "Download" button to save the results as a CSV file.

---

## **Working Example**

### **Input**
#### Uploaded CSV:
| Company       | Country       |
|---------------|---------------|
| Tesla         | USA           |
| Samsung       | South Korea   |
| BMW           | Germany       |

#### Query:
_"Retrieve the latest market share data for {Company} in {Country}."_

### **Output**
| Company       | Country       | Market Share (%) |
|---------------|---------------|------------------|
| Tesla         | USA           | 68%              |
| Samsung       | South Korea   | 25%              |
| BMW           | Germany       | 10%              |

---

## **Third-Party Tools**

1. **Groq API**:
   - Used for understanding and dynamically generating search queries.
   - [Groq API Documentation](https://groq.com/docs)

2. **SerpAPI**:
   - Enables search engine queries with structured JSON responses.
   - [SerpAPI Documentation](https://serpapi.com/docs)

3. **Google Sheets API**:
   - Integrates live data from Google Sheets into the app.
   - [Google Sheets API Documentation](https://developers.google.com/sheets)

---

## **Project Structure**
```plaintext
Project/
├── app/
│   ├── main_app.py          # Streamlit application code
│   ├── helper_functions.py  # Utility functions (included in the main_app.py already)
├── resources/
│   ├── ngrok.exe            # Optional HTTPS support
├── requirements.txt         # Python dependencies
├── .env.example             # Template for environment variables
├── README.md                # Project documentation
├── LICENSE                  # Open-source license
├── .gitignore               # Files to ignore in Git


