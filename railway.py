import matplotlib.pyplot as plt
import math



def fare_price(distance, different_regions, hubs_in_dest_region):
    """
    This function calculates the fare price from two stations according to their distance, 
    whether the journey involves different regions, and the number of hubs in the destination region.
    
    """
    
    e = math.e
    fare = 1 + distance * math.exp(-distance / 100) * (1 + (different_regions * hubs_in_dest_region) / 10)

    return fare


class Station:
    def __init__(self, name, region, crs, lat, lon, hub):

        if not all(isinstance(argu,str) for argu in [name, region, crs]):
            raise TypeError('Name, region and CRS muct have format of strings')
        
        if len(crs) != 3 or not crs.isupper() or not crs.isalpha():
            raise ValueError("CRS code must be a 3-character string with uppercase letters only.")
        
        if not (-90 <= lat <= 90):
            raise ValueError("Latitude must be within the range -90 to 90 degrees.")
        if not (-180 <= lon <= 180):
            raise ValueError("Longitude must be within the range -180 to 180 degrees.")
        
        if not isinstance(hub, bool):
            raise TypeError("Hub flag must be a boolean value.")

        self.name = name
        self.region = region
        self.crs = crs
        self.lat = lat
        self.lon = lon
        self.hub = hub

        

        
    def distance_to(self):
        pass



class RailNetwork:
    def __init__(self, stations_list):
        self.stations = {}
        for station in stations_list:
            if station.crs in self.stations:
                raise ValueError(f"Duplicate CRS code found: {station.crs}")
            self.stations[station.crs] = station

            
    def regions(self):
        raise NotImplementedError

    def n_stations(self):
        raise NotImplementedError

    def hub_stations(self, region):
        raise NotImplementedError

    def closest_hub(self, s):
        raise NotImplementedError

    def journey_planner(self, start, dest):
        raise NotImplementedError

    def journey_fare(self, start, dest, summary):
        raise NotImplementedError

    def plot_fares_to(self, crs_code, save, ADDITIONAL_ARGUMENTS):
        raise NotImplementedError

    def plot_network(self, marker_size: int = 5) -> None:
        """
        A function to plot the rail network, for visualisation purposes.
        You can optionally pass a marker size (in pixels) for the plot to use.

        The method will produce a matplotlib figure showing the locations of the stations in the network, and
        attempt to use matplotlib.pyplot.show to display the figure.

        This function will not execute successfully until you have created the regions() function.
        You are NOT required to write tests nor documentation for this function.
        """
        fig, ax = plt.subplots(figsize=(5, 10))
        ax.set_xlabel("Longitude (degrees)")
        ax.set_ylabel("Latitude (degrees)")
        ax.set_title("Railway Network")

        COLOURS = ["b", "r", "g", "c", "m", "y", "k"]
        MARKERS = [".", "o", "x", "*", "+"]

        for i, r in enumerate(self.regions):
            lats = [s.lat for s in self.stations.values() if s.region == r]
            lons = [s.lon for s in self.stations.values() if s.region == r]

            colour = COLOURS[i % len(COLOURS)]
            marker = MARKERS[i % len(MARKERS)]
            ax.scatter(lons, lats, s=marker_size, c=colour, marker=marker, label=r)

        ax.legend()
        plt.tight_layout()
        plt.show()
        return

    def plot_journey(self, start: str, dest: str) -> None:
        """
        Plot the journey between the start and end stations, on top of the rail network map.
        The start and dest inputs should the strings corresponding to the CRS codes of the
        starting and destination stations, respectively.

        The method will overlay the route that your journey_planner method has found on the
        locations of the stations in your network, and draw lines to indicate the route.

        This function will not successfully execute until you have written the journey_planner method.
        You are NOT required to write tests nor documentation for this function.
        """
        # Plot railway network in the background
        network_lats = [s.lat for s in self.stations.values()]
        network_lons = [s.lon for s in self.stations.values()]

        fig, ax = plt.subplots(figsize=(5, 10))
        ax.scatter(network_lons, network_lats, s=1, c="blue", marker="x")
        ax.set_xlabel("Longitude (degrees)")
        ax.set_ylabel("Latitude (degrees)")

        # Compute the journey
        journey = self.journey_planner(start, dest)
        plot_title = f"Journey from {journey[0].name} to {journey[-1].name}"
        ax.set_title(f"Journey from {journey[0].name} to {journey[-1].name}")

        # Draw over the network with the journey
        journey_lats = [s.lat for s in journey]
        journey_lons = [s.lon for s in journey]
        ax.plot(journey_lons, journey_lats, "ro-", markersize=2)

        plt.show()
        return
