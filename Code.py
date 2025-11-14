import requests
import json
import time


contestId = 2169 #replace with contestId 
totalRated = 9249 #replace with your rank
my_handle = "ysuovnii" # replace with your handle 

def download_standings():
    url = f"https://codeforces.com/api/contest.standings?contestId={contestId}&from=1&count={totalRated}"
    response = requests.get(url)
    data = response.json()

    filename = f"{contestId}Standings.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"Saved full standings → {filename}")

def filter_standings():
    filename = f"{contestId}Standings.json"

    with open(filename, 'r') as f:
        data = json.load(f)

    rows = data["result"]["rows"]
    newData = []

    for row in rows:
        handle = row["party"]["members"][0]["handle"]
        rank = row["rank"]
        points = row["points"]

        newData.append({
            "handle": handle,
            "rank": rank,
            "points": points,
        })

    newFile = f"{contestId}FilteredData.json"
    with open(newFile, 'w') as f:
        json.dump(newData, f, indent=4)

    print(f"Saved filtered standings → {newFile}")

def chunk_list(arr, size):
    for i in range(0, len(arr), size):
        yield arr[i:i + size]


def fetch_ratings():
    filename = f"{contestId}FilteredData.json"

    with open(filename, 'r') as f:
        filtered = json.load(f)

    handles = [entry["handle"] for entry in filtered]
    rating_map = {}

    for batch in chunk_list(handles, 200):
        handle_string = ";".join(batch)
        url = f"https://codeforces.com/api/user.info?handles={handle_string}"

        response = requests.get(url).json()

        if response["status"] != "OK":
            print("Rate limit hit. Retrying in 1 second...")
            time.sleep(1)
            response = requests.get(url).json()

        for user in response["result"]:
            rating_map[user["handle"]] = user.get("rating", "Unrated")

        time.sleep(0.5)  

    for entry in filtered:
        entry["rating"] = rating_map.get(entry["handle"], "Unrated")

    with open("FinalStandings.json", "w") as f:
        json.dump(filtered, f, indent=4)

    print("Saved final standings with ratings → FinalStandings.json")

def compute_comparison():
    with open("FinalStandings.json", "r") as f:
        data = json.load(f)

    for e in data:
        if isinstance(e["rating"], str):
            e["rating"] = 0

    for entry in data:
        if entry["handle"] == my_handle:
            my_rank = entry["rank"]
            my_rating = entry["rating"]
            break
    else:
        print("Your handle not found.")
        return

    lower_rating_above = sum(
        1 for e in data
        if e["rank"] < my_rank and e["rating"] < my_rating
    )

    lower_rating_below = sum(
        1 for e in data 
        if e["rank"] > my_rank and e["rating"] < my_rating
    )

    higher_rating_above = sum(
        1 for e in data 
        if e["rank"] < my_rank and e["rating"] > my_rating
    )

    higher_rating_below = sum(
        1 for e in data
        if e["rank"] > my_rank and e["rating"] > my_rating
    )

    print("\n===== RESULT =====")
    print("Lower rating above you:", lower_rating_above)
    print("Lower rating below you: ", lower_rating_below)
    print("Higher rating above you: ", higher_rating_above)
    print("Higher rating below you:", higher_rating_below)


def main():
    print("\n--- Downloading standings ---")
    download_standings()

    print("\n--- Filtering data ---")
    filter_standings()

    print("\n--- Fetching ratings for all participants ---")
    fetch_ratings()

    print("\n--- Computing comparison ---")
    compute_comparison()


if __name__ == "__main__":
    main()
