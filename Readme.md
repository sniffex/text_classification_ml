Create a python venv:
>python -m venv venv

or run Accaconda environment using:
>conda activate Assignment

Then install all of the dependencies/libraries to use in this project:

>pip install -r requirements.txt

You can use any website to get the test dataset by adding the URL in urls_list and add a new function. Then call the function in scrape_data function to scrape data.

    def scrape_data(urls):
        all_news_data = []  # Initialize a new list for each scrape operation

        for url in urls:
            scraped_data = []  # Initialize scraped_data within the loop
            if "cnn" in url:
                scraped_data = scrape_cnn_data(url)
            elif "bbc" in url:
                scraped_data = scrape_bbc_data(url)
            elif "apnews.com/entertainment" in url:
                scraped_data = scrape_ap_entertainment_data(url)
            elif "apnews.com/business" in url:
                scraped_data = scrape_ap_business_data(url)
            elif "apnews.com/technology" in url:
                scraped_data = scrape_ap_tech_data(url)
            elif "apnews.com/health" in url:
                scraped_data = scrape_ap_health_data(url)
            elif "nbcnews.com/science" in url:
                scraped_data = scrape_nbc_science_data(url)
            elif "nbcnews.com/health" in url:
                scraped_data = scrape_nbc_health_data(url)
            elif "nbcnews.com/business" in url:
                scraped_data = scrape_nbc_business_data(url)
            elif "nbcnews.com/tech-media" in url:
                scraped_data = scrape_nbc_tech_data(url)
            ################ Add new line here ####################
            else:
                scraped_data = []  # Handle other websites
                
            all_news_data.extend(scraped_data)
    
        return all_news_data
