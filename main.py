import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

# Define a function to fetch and parse the server info data
def fetch_and_parse_server_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    parsed_info = {}
    core_version_found = False

    for tr in soup.find_all('tr'):
        td_elements = tr.find_all('td')
        if len(td_elements) >= 2:
            key = td_elements[0].get_text(strip=True).lower()
            value = td_elements[1].get_text(strip=True)
            if core_version_found:
                if key.lower() == "guilds created":  # Stop parsing after "Guilds Created" section
                    break
                parsed_info[key] = value
            if key.lower() == "server core version":
                core_version_found = True

    return parsed_info

# Define a function to fetch and parse the online list data
def fetch_and_parse_playerlist(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    parsed_info = []

    for tr in soup.find_all('tr'):
        td_elements = tr.find_all('td')
        if len(td_elements) >= 2:
            parsed_info.append([td.text for td in td_elements])

    return parsed_info

# Define the main fetch_data function
def fetch_data():
    try:
        # Fetch server info
        server_info_url = "http://game.endless-online.com/server.html"
        server_info = fetch_and_parse_server_info(server_info_url)
        display_server_info(server_info)



    except requests.exceptions.SSLError as e:
        display_error("An error occurred while fetching data. Please try again later.")

# Define a function to display the server info
# Define a function to display the server info
# Define a function to display the server info
def display_server_info(info):
    info_text.delete(1.0, tk.END)  # Clear previous content
    for key, value in info.items():
        info_text.insert(tk.END, f"{key}: {value}\n")

    # Add a button for downloading the client
    download_button = ttk.Button(tab1, text="Download Client", command=lambda: open_link("https://www.endless-online.com/downloads.html"))
    download_button.pack(pady=10)



# Define other functions for displaying info and error messages
def display_error(message):
    info_text.delete(1.0, tk.END)  # Clear previous content
    info_text.insert(tk.END, message)

# Function to handle search button click
def search_button_click():
    query = search_entry.get()
    search_endless_online_recharged_wiki(query)

# Function to handle pressing the Enter key in the search entry
def bind_enter(event):
    search_button_click()
# Function to fetch and parse the search results
def search_endless_online_recharged_wiki(query):
    base_url = "https://endlessonlinerecharged.fandom.com/wiki/Special:Search"
    params = {
        "query": query,
        "scope": "internal",
        "navigationSearch": "true",
        "so": "trending"
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        search_results = soup.find_all("li", class_="unified-search__result")

        if search_results:
            results_text.delete(1.0, tk.END)
            for idx, result in enumerate(search_results, start=1):
                title_elem = result.find("a", class_="unified-search__result__title")
                url_elem = result.find("a", class_="unified-search__result__link")
                if title_elem and url_elem:
                    title = title_elem.text.strip()
                    url = url_elem["href"]
                    results_text.insert(tk.END, f"{title}: {url}\n\n")
                    # Make the link clickable
                    link_tag = f"link_{idx}"
                    results_text.tag_add(link_tag, f"{idx}.0", f"{idx}.end")
                    results_text.tag_config(link_tag, foreground="blue", underline=True)
                    results_text.tag_bind(link_tag, "<Button-1>", lambda event, link=url: open_link(link))
        else:
            results_text.delete(1.0, tk.END)
            results_text.insert(tk.END, "No search results found.")
    else:
        results_text.delete(1.0, tk.END)
        results_text.insert(tk.END, "Error: Failed to retrieve search results.")

# Function to open the clicked link in the browser
def open_link(url):
    import webbrowser
    webbrowser.open_new(url)
  
# Create the main window and tabs
root = ThemedTk(theme="ubuntu")
root.title("Game Server Info")

# Create a style object
style = ttk.Style()

# Increase the row height
style.configure('Treeview', rowheight=50)  # Adjust the value as needed

tab_control = ttk.Notebook(root)
tab_control.pack(expand=1, fill="both")

tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Server Info')


tab3 = ttk.Frame(tab_control)
tab_control.add(tab3, text='Wiki Search')

# Create the widgets for the first tab
info_text = tk.Text(tab1, wrap=tk.WORD, width=50)
info_text.pack(fill="both", expand=True, padx=10, pady=10)

# Create the widgets for the second tab

# Create the widgets for the third tab
search_label = ttk.Label(tab3, text="Enter search query:")
search_label.pack(pady=5)
search_entry = ttk.Entry(tab3, width=50)
search_entry.pack(pady=5)

# Bind the <Return> key to the search entry to trigger search_button_click
search_entry.bind('<Return>', bind_enter)

search_button = ttk.Button(tab3, text="Search", command=search_button_click)
search_button.pack(pady=5)
results_text = tk.Text(tab3, wrap=tk.WORD, width=50)
results_text.pack(fill="both", expand=True, padx=10, pady=10)


# Create the "Helpful Links" tab

# Function to add clickable links to the text widget
def add_link(text_widget, label, url):
    text_widget.tag_config(label, foreground="blue", underline=True)
    text_widget.insert(tk.END, label, label)
    text_widget.insert(tk.END, "\n")
    text_widget.tag_bind(label, "<Button-1>", lambda event, url=url: open_link(url))

# Create the "Helpful Links" tab
tab4 = ttk.Frame(tab_control)
tab_control.add(tab4, text='Helpful Links')

# Function to open link
def open_link(url):
    import webbrowser
    webbrowser.open_new(url)

# Dictionary containing label and URL pairs
links = {
    "EOBud": "https://eobud.boards.net",
    "EODash": "https://www.eodash.com/guides",
    "EOMix": "https://www.eomix.com",
    "SinTV": "https://www.youtube.com/user/SiinTV",
     "Eoserv": "https://eoserv.net/",
    "EORadio": "https://www.eoradio.co.uk/",
  "Endless Reddit": "https://www.reddit.com/r/EndlessOnline/?rdt=61294",
  "Endless Discord": "https://www.endless-online.com/link/endlessonlinediscord.html",

}

# Function to add clickable links as buttons in two rows
def add_links():
    row = 0
    col = 0
    for label, url in links.items():
        button = ttk.Button(tab4, text=label, command=lambda url=url: open_link(url))
        button.grid(row=row, column=col, padx=5, pady=5)
        col += 1
        if col > 1:
            col = 0
            row += 1

# Add clickable links as buttons in two rows
add_links()

import json

# Define function to fetch data from API
def fetch_online_players():
    try:
        response = requests.get("https://www.eodash.com/api/online")
        if response.status_code == 200:
            data = response.json()
            display_online_players(data)
        else:
            display_error("Failed to fetch online players data. Please try again later.")
    except requests.exceptions.RequestException as e:
        display_error("An error occurred while fetching data. Please try again later.")

# Define function to display online players in Treeview
def display_online_players(data):
    online_players_treeview.delete(*online_players_treeview.get_children())
    for player in data["players"]:  # Access the "players" list in the JSON data
        online_players_treeview.insert("", "end", values=(player["name"], player["level"], player["exp"]))


# Create the new tab
tab6 = ttk.Frame(tab_control)
tab_control.add(tab6, text='Online Players')

# Create widgets for the new tab
online_players_treeview = ttk.Treeview(tab6, columns=("Name", "Level", "Exp"))
online_players_treeview.heading("Name", text="Name")
online_players_treeview.heading("Level", text="Level")
online_players_treeview.heading("Exp", text="Experience")
online_players_treeview.grid(row=0, column=0, columnspan=1, padx=1, pady=1, sticky="nsew")

# Add a button to fetch online players
fetch_button = ttk.Button(tab6, text="Fetch Online Players", command=fetch_online_players)
fetch_button.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

# Fetch data when the program starts
fetch_online_players()

# Fetch data when the program starts
fetch_data()

root.mainloop()
