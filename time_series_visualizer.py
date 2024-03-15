import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
import locale

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=["date"], index_col="date")


# Clean data
mask = (df["value"] >= df["value"].quantile(0.025)) & (
    df["value"] <= df["value"].quantile(0.975)
)
df = df[mask]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df.index, df.value, color="#960000", linewidth=1)

    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_ylabel("Page Views")
    ax.set_xlabel("Date")
    # Save image and return fig (don't change this part)
    fig.savefig("line_plot.png")
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df["month"] = df.index.month
    df["year"] = df.index.year

    df_bar = df.groupby(["year", "month"])["value"].mean().unstack()

    # Draw bar plot

    fig = df_bar.plot.bar(
        legend=True, xlabel="Years", ylabel="Average Page Views", figsize=(8, 7)
    ).figure
    plt.legend(
        [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ],
        title="Months",
    )

    # Save image and return fig (don't change this part)
    fig.savefig("bar_plot.png")
    return fig


def draw_box_plot():
    locale.setlocale(locale.LC_TIME, "en_US.UTF-8")
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box["year"] = [d.year for d in df_box.date]
    df_box["month"] = [d.strftime("%b") for d in df_box.date]

    # Draw box plots (using Seaborn)
    df_box["month_num"] = df_box["date"].dt.month
    df_box = df_box.sort_values("month_num")
    df_box["month"] = df_box["month"]

    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))
    sns.boxplot(x=df_box["year"], y=df_box["value"], ax=axs[0])
    sns.boxplot(x=df_box["month"], y=df_box["value"], ax=axs[1])

    axs[0].set_title("Year-wise Box Plot (Trend)")
    axs[0].set_ylabel("Page Views")
    axs[0].set_xlabel("Year")

    axs[1].set_title("Month-wise Box Plot (Seasonality)")
    axs[1].set_ylabel("Page Views")
    axs[1].set_xlabel("Month")

    # Save image and return fig (don't change this part)
    fig.savefig("box_plot.png")
    return fig
