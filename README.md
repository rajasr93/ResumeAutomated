# ResumeAutomated

How to run this file:

1. Clone the repository: https://github.com/ris3abh/ResumeAutomated.git
2. Set a virtual environment: `python3 -m venv cenv`
3.  - Activate the virtual environment for macOS: `source cenv/bin/activate`
    - Activate the virtual environment for Windows: `cenv\Scripts\activate`
4. Install the requirements: `pip install -r requirements.txt`
5. Create a `city_title.json` file in the data directory with the following format:

    ```json
    {
        "city": ["city1", "city2", "city3"],
        "title": ["title1", "title2", "title3"]
    }
    ```

### STEP -1: Data Collection/Scrapping, Cleaning and Annotation
1. Go to the `src` directory: `cd src`
2. Run the `main.py` file: `python3 main.py`
3. This will save the scrapped, cleaned and annotated data in the `data` directory as `annotated_data.csv`, if the annotation process `failed` the `data` will be saved as `job_data_cleaned.csv`.

### STEP -2: Training the Model



