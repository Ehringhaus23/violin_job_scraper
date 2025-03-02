import argparse
from scraper_functions import save_csv, scrape_musical_chairs

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Scrape musicalchairs.info for orchestra job listings.")
    parser.add_argument(
        '-l', '--location', 
        type=str, 
        default='australia', 
        help="Filter jobs by location. Example: '-l france' (default: 'australia')."
    )
    
    parser.add_argument(
        '-i', '--instrument', 
        type=str, 
        default='violin', 
        help="Specify the instrument category. Example: '-i cello' (default: 'violin')."
    )

    args = parser.parse_args()
    jobs = scrape_musical_chairs(instrument=args.instrument, job_location=args.location)
    if jobs:
      print(f'{len(jobs)} {args.instrument} jobs found in {args.location} found!')
      save_csv(jobs) 
    else:
       print(f'No jobs for {args.instrument} found in {args.location} :(')