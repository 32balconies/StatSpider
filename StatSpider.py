# ----------------------------------------------------------------------------
# -------------------------------- StatSpider --------------------------------
# ------------------------------ by Jon Roberts ------------------------------
# ----------------------------------- v0.1 -----------------------------------
# ----------------------------------------------------------------------------

# --- IMPORTS ---

import requests
import json
from bs4 import BeautifulSoup
from gooey import Gooey,GooeyParser

# --- CONSTANTS ---

teams = ["ATL","BOS","BRK","CHO","CHI","CLE","DAL","DEN","DET","GSW","HOU","IND","LAC","LAL","MEM",
         "MIA","MIL","MIN","NOP","NYK","OKC","ORL","PHI","PHO","POR","SAC","SAS","TOR","UTA","WAS"]

stats = ["pos","height","weight","years_experience"]

url_start = "https://www.basketball-reference.com/teams/{}/2024.html"



def updateDatastore(args=None):
    
    # Creates a datastore dictionary for the given teams and stats
    
    datastore = {} 
    for team in teams:
        datastore[team] = {}
        url = url_start.format(team)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        for pl in soup.find_all('tr'):
            for p in pl.find_all('td',attrs={"data-stat": "player"}):
                datastore[team][p.a.string] = {}
            for stat in stats:
                for s in pl.find_all('td',attrs={"data-stat": stat}):
                    datastore[team][p.a.string][stat] = s.string
    
    
    # Formats and saves the json
    
    json_obj = json.dumps(datastore, indent=4)              
    with open(args.file_path, "w") as f:
        f.write(json_obj)

# ----------------------------------------------------------------------------

@Gooey(
    program_description="Update your basketball database",
    default_size=(600, 500),
)
def main(): 
    
    # Uses Gooey to create a filepath argument for user selection
    
    parser = GooeyParser()
    gp = parser.add_argument_group("Output")
    parser.add_argument("-a","--file_path", metavar="Save as...", widget="FileSaver",     
                        help="Choose where to save the new database.",
                            gooey_options={
                                'wildcard': "JavaScript Object Notation (*.json)|*.json",
                                'message': "Pick a location",
                                'default_dir': __file__,
                                'default_file': "database.json"
                            }
                            )
    args = parser.parse_args()
    
    updateDatastore(args)

if __name__ == "__main__":
    main()

# ----------------------------------------------------------------------------