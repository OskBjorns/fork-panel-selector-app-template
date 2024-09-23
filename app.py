import threading
import panel as pn
import time
import pandas as pd

# Ensure Panel extensions are loaded
pn.extension('tabulator')

# Sample machine data
machines = [
    {
        "Name": "Unit 500",
        "Flow": 0.5,
        "Minimum flow": 0.1,
        "Maximum flow": 0.9,
        "Height": 1.850,
        "Depth": 1.850,
        "Length": 2.995
    },
    {
        "Name": "Unit 1000",
        "Flow": 1.0,
        "Minimum flow": 0.4,
        "Maximum flow": 1.8,
        "Height": 2.350,
        "Depth": 1.800,
        "Length": 3.950
    },
    {
        "Name": "Module 2000",
        "Flow": 2.0,
        "Minimum flow": 0.5,
        "Maximum flow": 4.0,
        "Height": 2.800,
        "Depth": 3.200,
        "Length": 6.000
    },
    {
        "Name": "Module 3000",
        "Flow": 3.0,
        "Minimum flow": 1.0,
        "Maximum flow": 6.0,
        "Height": 3.300,
        "Depth": 3.600,
        "Length": 7.000
    },
    {
        "Name": "Module 4000",
        "Flow": 4.0,
        "Minimum flow": 1.0,
        "Maximum flow": 8.0,
        "Height": 3.800,
        "Depth": 4.000,
        "Length": 8.000
    },
    {
        "Name": "Module 5000",
        "Flow": 5.0,
        "Minimum flow": 1.0,
        "Maximum flow": 10.0,
        "Height": 4.300,
        "Depth": 4.400,
        "Length": 9.000
    },
    {
        "Name": "Module 7500",
        "Flow": 7.5,
        "Minimum flow": 1.0,
        "Maximum flow": 15.0,
        "Height": 4.800,
        "Depth": 4.900,
        "Length": 10.000
    },
    {
        "Name": "Module 10000",
        "Flow": 10.0,
        "Minimum flow": 1.0,
        "Maximum flow": 20.0,
        "Height": 5.300,
        "Depth": 5.400,
        "Length": 11.000
    },
    {
        "Name": "Module 15000",
        "Flow": 15.0,
        "Minimum flow": 1.0,
        "Maximum flow": 30.0,
        "Height": 5.800,
        "Depth": 5.900,
        "Length": 12.000
    },
    {
        "Name": "Module 20000",
        "Flow": 20.0,
        "Minimum flow": 1.0,
        "Maximum flow": 40.0,
        "Height": 6.300,
        "Depth": 6.400,
        "Length": 13.000
    },

]

# Convert the list of dictionaries to a DataFrame
machines_df = pd.DataFrame(machines)

class SelectorApp:
    def __init__(self):
        # Flow Range Slider
        self.flow_range = pn.widgets.RangeSlider(
            name="Optimal Flow Rate (m³/s)",
            start=0,
            end=20,
            step=0.1,
            value=(0, 16),
            format="0.0 m³/s"
        )
        
        # Machine Size Inputs
        self.height_input = pn.widgets.FloatInput(name="Max Height (m)", value=3.0, start=0)
        self.depth_input = pn.widgets.FloatInput(name="Max Depth (m)", value=3.0, start=0)
        self.length_input = pn.widgets.FloatInput(name="Max Length (m)", value=6.0, start=0)
        
         
        # Buttons
        self.submit_button = pn.widgets.Button(name="Submit", button_type="primary")

        
        # Machine Data Table
        self.machine_table = pn.widgets.Tabulator(
            machines_df,
            height=300,
            selectable=True,
            pagination='local',
            page_size=5
        )
        
        # Layout
        self.layout = pn.Column(
            pn.pane.Markdown("### Filter"),
            pn.Row(
                pn.Column("**Size Allowance**", 
                          self.height_input, 
                          self.depth_input, 
                          self.length_input),
                pn.Column("**Flow Range**", self.flow_range)
            ),
            pn.Row(self.submit_button),
            pn.pane.Markdown("### Available Machines"),
            self.machine_table,
            pn.pane.Markdown("*All machines can be customized to fit your demand - contact us to learn more about our custom solutions.*"),
     
        )
        
        # Assign event handlers
        self.submit_button.on_click(self.submit)
    
    def submit(self, event):
        flow_min, flow_max = self.flow_range.value
        max_height = self.height_input.value
        max_depth = self.depth_input.value
        max_length = self.length_input.value
        
        filtered_machines = machines_df[
            (machines_df["Flow"] >= flow_min) & (machines_df["Flow"] <= flow_max) &
            (machines_df["Height"] <= max_height) &
            (machines_df["Depth"] <= max_depth) &
            (machines_df["Length"] <= max_length)
        ]
        
        self.machine_table.value = filtered_machines
        print(f"Filtered Machines: {filtered_machines}")
    


app_instance = SelectorApp()

app = pn.template.BootstrapTemplate(
    title="Template Selector App",
    main=[app_instance.layout],
)

app.servable()

if __name__ == "__main__":
    # Serve the app on a local Panel server
    pn.serve(app, port=5006)  # You can specify the port if needed