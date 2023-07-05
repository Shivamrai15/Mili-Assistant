import os
import customtkinter
from location import Route
from location import reverseGeocoding, GPS
from tkintermapview import TkinterMapView

# Current directory of the application
application_directory = os.getcwd()


class APP(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Mili")
        self.GUI_geometry()
        self.iconbitmap(application_directory + "\\Data\\Images\\GUI\\logo.ico")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        # Frames of the app
        # ---------------------------------------------------------------
        self.distanceFrame = customtkinter.CTkFrame(
            self, fg_color="#252525", corner_radius=0
        )
        self.distanceFrame.grid(row=0, column=0, sticky="nsew")
        self.locationFrame = customtkinter.CTkFrame(
            self, fg_color="#252525", corner_radius=0
        )
        self.locationFrame.grid(row=0, column=0, sticky="nsew")
        # ---------------------------------------------------------------

    # Function which sets the window in the center of screen
    # ---------------------------------------------------------------------------------------------------

    def GUI_geometry(self):
        w = 1100
        h = 650
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.geometry("%dx%d+%d+%d" % (w, h, x, y))

    # ---------------------------------------------------------------------------------------------------

    def showFrame(self, frame):
        frame.tkraise()

    def currentLocation(self):
        gps = GPS.getLocation()
        latitude = gps[0]
        longitude = gps[1]
        address = reverseGeocoding(latitude, longitude)

        # adding markers to a place by right click
        def add_marker_event(coords):
            print("Add marker:", coords)
            new_marker = map_widget.set_marker(coords[0], coords[1], text="new marker")

        # Function to change the view of the map
        # --------------------------------------------------------------------------------------------------
        def changeTileServer(mode):
            if mode == "Default":
                map_widget.set_tile_server(
                    "https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga",
                    max_zoom=22,
                )  # (default)
                self.locationFrame.update()
            elif mode == "Satellite":
                map_widget.set_tile_server(
                    "https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga",
                    max_zoom=22,
                )  # google satellite
                self.locationFrame.update()
            elif mode == "Open Street":
                map_widget.set_tile_server(
                    "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"
                )  # OpenStreetMap
                self.locationFrame.update()

        # ----------------------------------------------------------------------------------------------------

        footerFrame = customtkinter.CTkFrame(
            self.locationFrame, fg_color="#252525", height=150, corner_radius=0
        )
        footerFrame.pack(side="bottom", anchor="center", fill="x", padx=20)
        map_widget = TkinterMapView(self.locationFrame, corner_radius=10)
        map_widget.pack(
            side="top", anchor="center", expand=True, fill="both", padx=20, pady=20
        )
        map_widget.set_position(deg_x=latitude, deg_y=longitude)
        map_widget.set_marker(deg_x=latitude, deg_y=longitude)
        map_widget.set_tile_server(
            "https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22
        )
        viewOption = customtkinter.CTkOptionMenu(
            footerFrame,
            values=["Default", "Satellite", "Open Street"],
            width=200,
            height=40,
            font=("Sitka Small", 14, "normal"),
            fg_color="#171717",
            button_color="#111",
            button_hover_color="#202020",
            dropdown_font=("Sitka Small", 14, "normal"),
            dropdown_fg_color="#303030",
            dynamic_resizing=True,
            command=changeTileServer,
        )
        viewOption.pack(side="right", anchor="ne", pady=(0, 60))
        customtkinter.CTkLabel(
            footerFrame,
            text="Current Location",
            text_color="#7f7f7f",
            fg_color="#252525",
            font=("Sitka Small", 16, "normal"),
            wraplength=350,
        ).pack(side="top", anchor="nw", padx=30, pady=5)
        customtkinter.CTkLabel(
            footerFrame,
            text=f"{address}",
            text_color="#fff",
            fg_color="#252525",
            font=("Sitka Small", 16, "normal"),
            wraplength=350,
        ).pack(side="left", anchor="nw", padx=30)
        map_widget.add_right_click_menu_command(
            label="Add Marker", command=add_marker_event, pass_coords=True
        )
        self.showFrame(self.locationFrame)

    def distanceAndRoute(self, origin, destination):
        location, route = Route(origin, destination).route()
        if location is not None and route is not None:
            origin = location.get("origin")
            destination = location.get("destination")
            distance = route.get("distance")
            time = route.get("time")
            route_coordinates = route.get("route")

            # adding markers to a place by right click
            def add_marker_event(coords):
                print("Add marker:", coords)
                new_marker = map_widget.set_marker(
                    coords[0], coords[1], text="new marker"
                )

            # Function to change the view of the map
            # --------------------------------------------------------------------------------------------------
            def changeTileServer(mode):
                if mode == "Default":
                    map_widget.set_tile_server(
                        "https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga",
                        max_zoom=22,
                    )  # (default)
                    self.distanceFrame.update()
                elif mode == "Satellite":
                    map_widget.set_tile_server(
                        "https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga",
                        max_zoom=22,
                    )  # google satellite
                    self.distanceFrame.update()
                elif mode == "Open Street":
                    map_widget.set_tile_server(
                        "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    )  # OpenStreetMap
                    self.distanceFrame.update()

            # ----------------------------------------------------------------------------------------------------

            footerFrame = customtkinter.CTkFrame(
                self.distanceFrame, fg_color="#252525", height=150, corner_radius=0
            )
            footerFrame.pack(side="bottom", anchor="center", fill="x", padx=20)
            map_widget = TkinterMapView(self.distanceFrame, corner_radius=10)
            map_widget.pack(
                side="top", anchor="center", expand=True, fill="both", padx=20, pady=20
            )
            map_widget.set_position(deg_x=origin[0], deg_y=origin[1])
            map_widget.set_marker(deg_x=origin[0], deg_y=origin[1], text="Origin")
            map_widget.set_marker(
                deg_x=destination[0], deg_y=destination[1], text="Destination"
            )
            map_widget.set_path(route_coordinates)
            map_widget.set_tile_server(
                "https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga",
                max_zoom=22,
            )
            viewOption = customtkinter.CTkOptionMenu(
                footerFrame,
                values=["Default", "Satellite", "Open Street"],
                width=200,
                height=40,
                font=("Sitka Small", 14, "normal"),
                fg_color="#171717",
                button_color="#111",
                button_hover_color="#202020",
                dropdown_font=("Sitka Small", 14, "normal"),
                dropdown_fg_color="#303030",
                dynamic_resizing=True,
                command=changeTileServer,
            )
            viewOption.pack(side="right", anchor="ne", pady=(0, 60))
            customtkinter.CTkLabel(
                footerFrame,
                text=f"Distance {distance}",
                text_color="#7f7f7f",
                fg_color="#252525",
                font=("Sitka Small", 16, "normal"),
                wraplength=350,
            ).pack(side="top", anchor="nw", padx=30, pady=5)
            customtkinter.CTkLabel(
                footerFrame,
                text=f"Time {time}",
                text_color="#fff",
                fg_color="#252525",
                font=("Sitka Small", 16, "normal"),
                wraplength=350,
            ).pack(side="left", anchor="nw", padx=30)
            map_widget.add_right_click_menu_command(
                label="Add Marker", command=add_marker_event, pass_coords=True
            )
            self.showFrame(self.distanceFrame)
