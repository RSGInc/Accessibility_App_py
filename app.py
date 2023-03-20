from shiny import App, render, ui
import matplotlib.pyplot as plt
import numpy as np
import folium
import geopandas as gp
from htmltools import css
from shinywidgets import output_widget, reactive_read, register_widget
import ipyleaflet as L

#extent = gp.read_file("C:/Users/reid.haefer/conveyal_app/data/Council_Districts.geojson")

app_ui = ui.page_fluid(
    ui.panel_title("Caltrans Accessibility Metrics Post-Processing Tool"),
    # style ----
    ui.navset_tab(
        # elements ----
        ui.nav("Project Analysis", 
               ui.panel_sidebar(
                   ui.input_text("name", "Project Name"),
                   ui.input_file("base_upload", "Baseline Conveyal .TIFF Output"),
                   ui.input_file("project_upload", "Project Conveyal .TIFF Output"),
                   ui.input_file("weight_upload", "Weight .TIFF (optional)"),
                   ui.input_file("extend_upload", "Project Extent Shapefile"),
                   ui.input_numeric("area", "Analysis Area Buffer (miles)", 1),
                   ui.download_button("download_csv", "Export CSV")
                   #ui.input_slider("n", "Sample size", 0, 1000, 250),
                   #ui.input_numeric("mean", "Mean", 0),
                   #ui.input_numeric("std_dev", "Standard deviation", 1),
                   #ui.input_slider("n_bins", "Number of bins", 0, 100, 20)
               ),

               ui.panel_main(
                   ui.output_plot("plot")
               )
               ),
        ui.nav("Map",
                ui.panel_sidebar(
                    ui.input_select("map_select","Select Raster to Map",choices=["Baseline Accessibility", "Project Accessibility", 
                    "Accessibility Change","Weighted Accessibility Change","Baseline Accessibility (Natural)", "Project Accessibility (Natural)", 
                    "Accessibility Change (Natural)","Weighted Accessibility Change (Natural)"])
                ),
                ui.panel_main(
                    output_widget("map", height='5000')
                )
        )
    )
)


def server(input, output, session):
      # Initialize and display when the session starts (1)
    map = L.Map(center=(38.587726,-121.469245), zoom=12, scroll_wheel_zoom=True)
    # Add a distance scale
    map.add_control(L.leaflet.ScaleControl(position="bottomleft"))
    
    register_widget("map", map)
app = App(app_ui, server)
