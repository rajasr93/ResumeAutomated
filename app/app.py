import streamlit as st
from jobspy import scrape_jobs
import webbrowser

class JobSearchApp:
    def __init__(self):
        self.css = """
        <style>
            /* General styles */
            body {
                font-family: 'Roboto', sans-serif;
                background-color: #f5f5f5;
            }

            /* Header styles */
            .header {
                background-color: #2196f3;
                color: white;
                padding: 20px;
                text-align: center;
            }

            /* Search bar styles */
            .search-bar {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 20px;
            }

            .search-bar input {
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
                margin-right: 10px;
                width: 200px; /* Adjust the width as needed */
            }

            .search-bar button {
                padding: 10px 20px;
                background-color: #4caf50;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }

            /* Job listing styles */
            .job-listing {
                background-color: white;
                padding: 20px;
                border-radius: 4px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
            }

            .job-listing h3 {
                margin-top: 0;
            }

            .job-listing button {
                background-color: #2196f3;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                cursor: pointer;
            }

            .job-listing-container {
                max-height: 500px; /* Adjust the height as needed */
                overflow-y: auto; /* Enable vertical scrolling */
                display: flex;
                flex-direction: column;
            }

            /* Job details styles */
            .job-details {
                background-color: white;
                padding: 20px;
                border-radius: 4px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                max-height: 500px; /* Adjust the height as needed */
                overflow-y: auto; /* Enable vertical scrolling */
            }

            .job-listing {
                background-color: white;
                padding: 20px;
                border-radius: 4px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
            }

            /* Job details styles */
            .job-details {
                background-color: white;
                padding: 20px;
                border-radius: 4px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }

            .job-details h2 {
                margin-top: 0;
            }

            /* Expand layout to full width */
            .main {
                width: 100%;
                /*max-width: 100%;*/
                padding: 0 100px
            }

            /* Remove unnecessary padding */
            .block-container {
                padding: 0;
            }
        </style>
        """
        if "jobs" not in st.session_state:
            st.session_state.jobs = None
        if "selected_job" not in st.session_state:
            st.session_state.selected_job = None
    
    def set_page_config(self):
        st.set_page_config(page_title="Job Search", layout="wide")
        st.markdown(self.css, unsafe_allow_html=True)
        st.markdown("<div class='header'><h1>Job Search</h1></div>", unsafe_allow_html=True)
    
    def display_search_bar(self):
        with st.container():
            st.markdown("<div class='search-bar'>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([4, 4, 2])
            with col1:
                job_title = st.text_input("Job Title", placeholder="Enter job title")
            with col2:
                location = st.text_input("Location", placeholder="Enter location")
            with col3:
                search_button = st.button("Search Jobs")
            st.markdown("</div>", unsafe_allow_html=True)
            return search_button, job_title, location
    
    def search_jobs(self, job_title, location):
        st.session_state.jobs = scrape_jobs(
            site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor"],
            search_term=job_title,
            location=location,
            results_wanted=10,
            country_indeed="USA",
            description_format="markdown",
            description=True
        )
    
    def display_jobs(self):
        col1, col2 = st.columns([2, 3])
        with col1:
            with st.container():
                st.markdown("<div class='job-listing-container'>", unsafe_allow_html=True)
                for index, job in st.session_state.jobs.iterrows():
                    st.markdown("<div class='job-listing'>", unsafe_allow_html=True)
                    st.markdown(f"<h3>{job['title']} - {job['company']}</h3>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Location:</strong> {job['location']}</p>", unsafe_allow_html=True)
                    if st.button("View Job", key=index):
                        st.session_state.selected_job = job
                    st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

         # Display job details in the right column
        with col2:
            if st.session_state.selected_job is not None:
                with st.container():
                    st.markdown("<div class='job-details'>", unsafe_allow_html=True)
                    st.markdown(f"<h2>{st.session_state.selected_job['title']}</h2>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Company:</strong> {st.session_state.selected_job['company']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Location:</strong> {st.session_state.selected_job['location']}</p>", unsafe_allow_html=True)
                    if 'job_url' in st.session_state.selected_job:
                        if st.button("Apply for Job"):
                            webbrowser.open_new_tab(st.session_state.selected_job['job_url'])
                    st.markdown(f"<h3>Description:</h3><p>{st.session_state.selected_job['description']}</p>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
    
    def run(self):
        self.set_page_config()
        search_button, job_title, location = self.display_search_bar()
        if search_button and job_title and location:
            self.search_jobs(job_title, location)
        if st.session_state.jobs is not None:
            self.display_jobs()

if __name__ == "__main__":
    app = JobSearchApp()
    app.run()