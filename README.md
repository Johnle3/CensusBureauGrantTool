# Census Bureau Grants Tool

A web-based application designed to support novice grant applicants (SLaNT users) by providing access to the top 100 relevant Census statistics. Features include filtering, trend visualizations, and exportable graphics.

---

## 🛠 Project Structure

- `ConnectToCensusAPI.ipynb`: Jupyter Notebook for testing API connections
- `DownloadFromDataDownloader.py`: Script to pull ACS data via CLI
- `config.json`: Stores local file paths
- `.env`: Stores your API key securely
- `requirements.txt`: All Python dependencies

---

## ✅ Setup Instructions

### Prerequisites

- Python 3.7+
- Jupyter Notebook
- Valid Census API key

### Clone the Repository

```bash
git clone https://github.com/Johnle3/CensusBureauGrantTool
cd CensusBureauGrantTool
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Your Environment

1. Create a `.env` file with:
   ```
   CENSUS_API_KEY=your_api_key_here
   ```
2. Download `config.json` from the repo and update file paths to match your local directory structure.

---

## ▶️ Running the App Locally

```bash
jupyter notebook
```

- Open and run `ConnectToCensusAPI.ipynb` to test the API connection
- To run the full app, open `app.ipynb` and execute:
  ```python
  app.run_server(jupyter_mode='external', port=8051)
  ```

---

## 🔁 Data Updates

To pull fresh ACS data using the Census Data Downloader:

```bash
cd census-data-downloader
pip install -e .
python DownloadFromDataDownloader.py
```

Data will be saved to the directory specified in your `config.json` file.

---

## 🔧 Future Work

- Improve visualization performance and UI responsiveness
- Implement cloud hosting (e.g., AWS, Ravenna)
- Build NLP-based grant text matching and smart data suggestions
- Add user authentication and saved dashboards

---

## 📂 Notes

- Do not upload large data files to GitHub
- Keep `.env` and local data paths secure
- Refer to shared Box folder for archived project materials and documentation
