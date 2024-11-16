# **Automated Web Search and Data Retrieval System**

## **Overview**
This project automates information retrieval from the web for entities listed in a dataset. Designed with simplicity and efficiency in mind, it provides a user-friendly interface to upload datasets or connect to a Google Sheet, define custom prompts, and retrieve structured results dynamically.

The project is built using cutting-edge technologies like Groq API for natural language understanding, SerpAPI for web searches, and Streamlit for the user interface.

---

**Loom-Video:-**  A short video walkthrough of the Project.
https://drive.google.com/file/d/1y00rkDAoB-2vFliS5QKaN2I_4h6CHKKT/view?usp=drivesdk

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

### **Step 3: Run the Application**
Start the Streamlit application:
```bash
streamlit run app/main_app.py
```

---

## API Keys and Environment Variables

To ensure the smooth functioning of the application, you need to set up your API keys and environment variables. Follow these steps:

### 1. **Locating the `.env` File**
   - The repository contains an example `.env.example` file in the root directory.
   - Rename this file to `.env`.

### 2. **Adding API Keys**
   - Open the `.env` file in a text editor.
   - Add the required API keys and credentials for third-party integrations.
   - Example:
     ```plaintext
     GOOGLE_SHEETS_API_KEY=<Your Google Sheets API Key>
     GOOGLE_OAUTH_CLIENT_ID=<Your OAuth 2.0 Client ID>
     ```

### 3. **NGROK Configuration (If Applicable)**
   - For exposing your local server to the internet using ngrok, add the ngrok token in the `.env` file.
   - Example:
     ```plaintext
     NGROK_AUTH_TOKEN=<Your ngrok Auth Token>
     ```

### 4. **Usage**
   - The application will automatically read the environment variables from the `.env` file during runtime.
   - Ensure the `.env` file is stored securely and not shared or uploaded publicly to maintain the confidentiality of your API keys.
**Note:-** Google Cloud secret file is not present in the .env file you should just download your secret_file(JSON Format) from google cloud and place in your root directory and paste it path to the code just below the .env configuration.

---

## Usage Guide

Follow these instructions to utilize the dashboard efficiently:

### 1. **Uploading CSV Files**
   - Click the **"Upload CSV File"** button on the dashboard.
   - Choose a valid CSV file from your local system.
   - Once uploaded, the file will be processed, and a preview of the data will be displayed in an interactive table.

### 2. **Connecting to Google Sheets**
   - Click the **"Connect Google Sheet"** button.
   - Authenticate with your Google account to grant access to your Google Sheets.
   - After authentication, provide the URL of the Google Sheet you want to connect.
   - Select the required sheet from the dropdown menu to load its data into the dashboard for processing.
   - The app maintains a real-time connection with the Google Sheet for live updates.

### 3. **Setting Up Search Queries**
   - Use the **"Primary Column Selection"** dropdown to choose the column containing the entities (e.g., company names).
   - Input your custom search prompt in the **"Custom Prompt"** text box.
   - Click **"Run Query"** to initiate the information retrieval process.
   - The results will appear in a separate section and can be downloaded as a CSV file.

### 4. **Extracted Results**
   - Once the query completes, view the extracted results in an interactive preview table.
   - Download the results as a CSV file for further analysis or use.

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
_"Retrieve the latest market share data of {Company}."_

### **Output**
| Company       | Market Share (%) |
|---------------|------------------|
| Tesla         |       45%        |
| Samsung       |       38%        |
| BMW           |       32%        |

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
```
---

## **Contributing**
Contributions are welcome! To contribute:
  1. Fork the repository.
  2. Create a feature branch:
    ```bash
    git checkout -b feature-name
    ```
  3. Commit your changes:
     ```bash
     git commit -m "Add feature-name"
     ```
  4. Push to your branch:
     ```bash
     git push origin feature-name
     ```
  5. Open a pull request.

---

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **Contact**

For any queries or feedback, reach out via email at smpy1405@gmail.com.

---
