import re
from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime

def scrape_musical_chairs(instrument = 'violin', job_location = 'australia'):
  URL = f"https://www.musicalchairs.info/{instrument}/jobs"
  page = requests.get(URL)
  soup = BeautifulSoup(page.content, "html.parser")
  jobs = soup.find_all("li", class_="preview")
  results = []
  for job in jobs:
    try:
        location = job.find("div", class_="post_item_location")
        posted_date = job.find("div", class_="post_item_date")
        position = job.find("div", class_="post_item_info")
        orchestra = job.find("div", class_="post_item_name")
        job_link = job.find("a", href=True)
        
        location_text = location.get_text(strip=True).replace(',', '') if location else "N/A"
        if re.search(job_location, location_text.lower()):
          posted_date_text = posted_date.get_text(strip=True).replace("Posted: ", "") if posted_date else "N/A"
          position_text = position.get_text(strip=True) if position else "N/A"
          orchestra_text = orchestra.get_text(strip=True) if orchestra else "N/A"
          job_url = f"https://www.musicalchairs.info{job_link['href']}" if job_link else "N/A"
          results.append((location_text, posted_date_text, position_text, orchestra_text, job_url))
          print(location_text)
    except Exception as e:
        print(f"Error processing a job listing: {e}")
        continue  # Skip this job listing and move to the next one
  return results


def save_csv(job_list, file_name=f"orchestra_jobs_{datetime.today().strftime('%Y-%m-%d')}.csv"):
   with open(file_name,'w', newline='', encoding='utf-8') as out:
    csv_out=csv.writer(out, quoting=csv.QUOTE_MINIMAL)
    csv_out.writerow(['Location','Posted Date', 'Position', 'Orchestra', 'Link'])
    for row in job_list:
        csv_out.writerow(row)