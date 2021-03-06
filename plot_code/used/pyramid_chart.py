import pandas as pd
import numpy as np
from collections import Counter
from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import dodge
from bokeh.models import ColumnDataSource
from bokeh.plotting import output_notebook, show, gridplot
from bokeh.models import HoverTool
from bokeh.models import FactorRange, Range1d, Plot
from bokeh.models import Rect, CategoricalAxis, LinearAxis, GlyphRenderer


def main():

    df = pd.read_csv('../../university_ranking.csv', index_col=0)

    df2016 = df.loc[df['year'] == 2016].head(200)
    df2017 = df.loc[df['year'] == 2017].head(200)
    df2018 = df.loc[df['year'] == 2018].head(200)

    dfs = [df2016, df2017, df2018]

    i = 2016

    for df in dfs:

        data = {
                'Ranking': df['ranking'],
                'Male': df['male'],
                'Female': df['female'],
                'university': df['university_name'],
                'midFemale': df['female']/2,
                'midMale': df['male']/2
                }

        source = ColumnDataSource(data=data)

        # Set up the ranges, plot, and axes
        bar_height = 0.8
        max_value = 100
        ydr = Range1d(0, 200)
        xdr_left = Range1d(max_value, 0)
        xdr_right = Range1d(0, max_value)
        plot_height = 400
        plot_width = 400

        hover = HoverTool(
                  tooltips=[
                    ('Ranking', '@Ranking'),
                    ('% male students', '@Male%'),
                    ('% female students', '@Female%'),
                    ('University', '@university')
                    ])

        plot_left = figure(tools=[hover], title="male", x_range=xdr_left,
                           y_range=ydr, plot_height=plot_height,
                           plot_width=int(plot_width/2))
        plot_right = figure(tools=[hover], title="female",
                            x_range=xdr_right, y_range=ydr,
                            plot_height=plot_height,
                            plot_width=int(plot_width/2))

        # plot_left.add_layout(CategoricalAxis(), 'left')
        plot_right.yaxis.visible = False

        # Set up the ranges, plot, and axes
        left_rect = Rect(y='Ranking',
                         x='midMale',
                         width='Male',
                         height=bar_height,
                         fill_color="#b3cde3",
                         line_color=None)
        right_rect = Rect(y='Ranking',
                          x='midFemale',
                          width='Female',
                          height=bar_height,
                          fill_color="#fbb4ae",
                          line_color=None)

        left_glyph = GlyphRenderer(data_source=source, glyph=left_rect)
        right_glyph = GlyphRenderer(data_source=source, glyph=right_rect)

        plot_left.renderers.extend([left_glyph])
        plot_right.renderers.extend([right_glyph])

        plot_left.min_border_right = 0
        plot_right.min_border_left = 0

    output_file('docs/male_female.html')
    g = gridplot([[plot_left, plot_right]], border_space=0)
    show(g)


if __name__ == "__main__":
        main()
