import prices
from shiny import reactive, render
from shiny.express import input,ui
import random
from datetime import datetime
from faicons import icon_svg
from collections import deque
import pandas as pd
import plotly.express as px
from scipy import stats
from shinywidgets import render_plotly
from shinyswatch import theme
import pathlib

DEQUE_SIZE: int = 5
reactive_value_wrapper_aapl= reactive.value(deque(maxlen=DEQUE_SIZE))
reactive_value_wrapper_nvda= reactive.value(deque(maxlen=DEQUE_SIZE))
reactive_value_wrapper_msft= reactive.value(deque(maxlen=DEQUE_SIZE))


stocks={"NVDA":"NVDA","AAPL":"AAPL","MSFT":"MSFT"}


file=pathlib.Path(__file__).parent / "nfl_2024.csv"

# ------------------------------------------------
# This refreshes the page
# ------------------------------------------------

UPDATE_INTERVAL_SECS: int = 30


@reactive.file_reader(file)
def read_file():
        return pd.read_csv(file)


# ------------------------------------------------
# Define the Shiny UI Page layout - Page Options
# ------------------------------------------------


ui.page_opts(title="Stock Price Page Live", fillable=True, theme=theme.lumen)

# ------------------------------------------------
# Define the Shiny UI Page layout - Sidebar
# ------------------------------------------------

with ui.sidebar(open="open"):
    ui.h2("Stock prices", class_="text-center")
    ui.p(
        "A demonstration of real-time stock quotes.",
        class_="text-center",
    )

    ui.p(
        "Data refreshes in 30 second intervals.",
        class_="text-center",
    )

    ui.input_selectize("stocks","Choose a stock",stocks, multiple=False)
    
   

#---------------------------------------------------------------------
# In Shiny Express, everything not in the sidebar is in the main panel
#---------------------------------------------------------------------

with ui.layout_columns(min_height="200px"):
    with ui.value_box( theme="bg-gradient-blue-purple"):
        @render.text
        def value():
            return "You choose: " + str(input.stocks())

        @render.text
        def display_aapl2():
            """Get the latest reading"""
            deque_snapshot,df, latest_price= reactive_calc_combined()
            return f"${str(latest_price['price'])}"


    with ui.card(full_screen=True):
       

        @render.text
        def value2():
            return "You choose: " + str(input.stocks())
          
        @render.data_frame
        def display_df2():
            """Get the latest reading and return a dataframe with current readings"""
            deque_snapshot,df, latest_price= reactive_calc_combined()
            pd.set_option('display.width', None)        # Use maximum width
            return render.DataGrid( df,width="100%")

with ui.layout_columns(max_height="400px"):    
    with ui.card(full_screen=False,height="200px"):
       
        @render_plotly
        def display_plott():

            deque_snapshot,df, latest_price = reactive_calc_combined()

            if not df.empty:
            # Convert the 'timestamp' column to datetime for better plotting
                fig=px.line(df,x="timestamp", y="price", title="Chart")
                return fig
    with ui.card(full_screen=False,height="200px"):
        @render.table
        def result():
            return read_file()

@reactive.calc()
def reactive_calc_combined():
 
    # Invalidate this calculation every UPDATE_INTERVAL_SECS to trigger updates
    reactive.invalidate_later(UPDATE_INTERVAL_SECS)

    # call the methods to get the data
    
    
    
    new_price=prices.get_price(str(input.stocks()))

    if str(input.stocks())=="NVDA":

        reactive_value_wrapper_nvda.get().append(new_price)
        deque_snapshot=reactive_value_wrapper_nvda.get()
        df=pd.DataFrame(deque_snapshot)
        latest_price=new_price
        
        return deque_snapshot,df, latest_price
    
    elif str(input.stocks())=="AAPL":

        reactive_value_wrapper_aapl.get().append(new_price)
        deque_snapshot=reactive_value_wrapper_aapl.get()
        df=pd.DataFrame(deque_snapshot)
        latest_price=new_price
        
        return deque_snapshot,df, latest_price
    
    elif str(input.stocks())=="MSFT":

        reactive_value_wrapper_msft.get().append(new_price)
        deque_snapshot=reactive_value_wrapper_msft.get()
        df=pd.DataFrame(deque_snapshot)
        latest_price=new_price
        
        return deque_snapshot,df, latest_price
    