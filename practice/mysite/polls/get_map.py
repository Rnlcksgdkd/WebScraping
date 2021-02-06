import pandas as pd
import folium

# HTML 로 저장
def get_Map(NAME, Y, X):
    save_dir = "./polls/templates/polls"

    df = pd.DataFrame({"X" : X , "Y" : Y})
    df["X"] = pd.to_numeric(df["X"])
    df["Y"] = pd.to_numeric(df["Y"])
    map_searching = folium.Map(location = [df["Y"].mean() , df["X"].mean()], zoom_start = 13)

    for i in range(len(ADDRESS)):
        folium.Marker((Y[i],X[i]) , radius = 10 , color = "red" , popup = NAME[i]).add_to(map_searching)
    map_searching.save('map.html')