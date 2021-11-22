import matplotlib.pyplot as plt
from src.handwriting_sample.base import HandwritingDataBase


# TODO: First fast version, need to be refactored to use plotly


class HandwritingSampleVisualizer(HandwritingDataBase):
    """Class implementing handwriting data visualizer"""

    # ------------- #
    # Plot methods  #
    # ------------- #
    def plot_on_surface_movement(self, sample, x_label=None, y_label=None, save_as=None):
        """
        Plot task on surface only

        :param sample: instance of handwriting sample
        :type sample: HandwritingSample
        :param x_label: label of X axis
        :param y_label: label of Y axis
        :param save_as: setup save location if you want to save a file
        """

        # Plot task on surface only without line connections between in_air gaps
        ax, plot = self._plot_strokes(sample,
                                      x_label=x_label,
                                      y_label=y_label,
                                      on_surface_movement=True,
                                      on_surface_color='darkblue',
                                      save_as=save_as)
        return ax, plot

    def plot_in_air_movement(self, sample, x_label=None, y_label=None, save_as=None):
        """
        Plot task with in air movement

        :param sample: instance of handwriting sample
        :type sample: HandwritingSample
        :param x_label: label of X axis
        :param y_label: label of Y axis
        :param save_as: setup save location if you want to save a file
        """
        # Plot task with in air data
        ax, plot = self._plot_strokes(sample,
                                      x_label=x_label,
                                      y_label=y_label,
                                      in_air_movement=True,
                                      in_air_color='plum',
                                      save_as=save_as)

        return ax, plot

    def plot_separate_movements(self, sample, x_label=None, y_label=None, save_as=None):
        """
        Plot task with separate movements

        :param sample: instance of handwriting sample
        :type sample: HandwritingSample
        :param x_label: label of X axis
        :param y_label: label of Y axis
        :param save_as: setup save location if you want to save a file
        """
        # Plot task with in air data
        ax, plot = self._plot_strokes(sample,
                                      x_label=x_label,
                                      y_label=y_label,
                                      in_air_movement=True,
                                      on_surface_movement=True,
                                      on_surface_color='darkblue',
                                      in_air_color='plum',
                                      save_as=save_as)

        return ax, plot

    def plot_strokes(self, sample, x_label=None, y_label=None, save_as=None):
        """
        Plot task separate strokes

        :param sample: instance of handwriting sample
        :type sample: HandwritingSample
        :param x_label: label of X axis
        :param y_label: label of Y axis
        :param save_as: setup save location if you want to save a file
        """
        # Plot task with in air data
        ax, plot = self._plot_strokes(sample,
                                      x_label=x_label,
                                      y_label=y_label,
                                      in_air_movement=True,
                                      on_surface_movement=True,
                                      save_as=save_as)

        return ax, plot

    def _plot_strokes(
            self,
            sample,
            x_label=None,
            y_label=None,
            in_air_movement=False,
            on_surface_movement=False,
            on_surface_color=None,
            in_air_color=None,
            fig_show=True,
            save_as=None,
            fig_kwargs=None):
        """
        Plot line plots for input data

        :param sample: instance of handwriting sample
        :type sample: handwriting_sample.HandwritingSample
        :param x_label: label of X axis
        :param y_label: label of Y axis
        :param in_air_movement: show in air movements
        :param on_surface_movement: show on surface movements
        :param fig_show: True/False value to show the figure
        :param save_as: setup save location if you want to save a file
        :return: axis and figure of the plot
        """

        # Prepare the figure settings
        fig_kwargs = fig_kwargs if fig_kwargs else {
            "fig_size": (10, 6),
            "show_ticks": True,
            "x_label": "X [mm]",
            "y_label": "Y [mm]",
            "title": "Strokes XY",
            "shade": True,
            "colors": ["red", "blue"]
        }

        # Get strokes
        stroke_data = sample.get_strokes(on_surface_only=on_surface_movement,
                                         in_air_only=in_air_movement)

        if not stroke_data:
            self.log(f"No data to plot!")
            return

        # Create figure if axes not inserted
        fig, axis = plt.subplots(1, 1, figsize=fig_kwargs.get("fig_size"))

        # Set labels
        x_label = fig_kwargs["x_label"] if not x_label else x_label
        y_label = fig_kwargs["y_label"] if not y_label else y_label

        # Plot strokes
        for stroke in stroke_data:
            self._plot_task(stroke,
                            x_label=x_label,
                            y_label=y_label,
                            ax=axis,
                            on_surface_color=on_surface_color,
                            in_air_color=in_air_color)

        # Set tight layout
        fig.tight_layout()

        # Save the graph
        if save_as:
            plt.savefig(save_as, bbox_inches="tight")

        # Show the graph
        if fig_show:
            plt.show()
        else:
            plt.close()

        return axis, plt

    @staticmethod
    def _plot_task(
            stroke,
            x_label=None,
            y_label=None,
            on_surface_color=None,
            in_air_color=None,
            ax=None,
            fig=None,
            fig_show=True,
            save_as=None,
            fig_kwargs=None):
        """
        Plot line plots for input data

        :param stroke: instance of handwriting sample
        :param x_label:           label of X axis
        :param y_label:           label of Y axis
        :param on_surface_color:  color of on surface movement
        :param in_air_color:      color of in air movement
        :param ax:                axis to plot on
        :param fig:               figure to show on
        :param fig_show:          True/False value to show the figure
        :param save_as:           setup save location if you want to save a file

        :return:                  axis and figure of the plot
        """

        # Prepare the figure settings
        fig_kwargs = fig_kwargs if fig_kwargs else {
            "fig_size": (10, 6),
            "show_ticks": True,
            "x_label": "X [mm]",
            "y_label": "Y [mm]",
            "title": "Task XY",
            "shade": False,
            "colors": ["red", "blue"]
        }

        # Split movements to on surface and in air
        # on_surface, in_air = split_movement(data)

        # Create figure if axes not inserted
        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=fig_kwargs.get("fig_size"))

        # Plot on surface
        color = on_surface_color if stroke[0] == "on_surface" else in_air_color
        ax.plot(stroke[1].x, stroke[1].y, color=color)

        # Plot in air if True
        # if in_air_movement:
        #     ax.plot(in_air['X'], in_air['Y'], color=in_air_color)

        # Set Grid to ture
        ax.yaxis.grid(True)
        ax.xaxis.grid(True)

        # Set labels
        title = fig_kwargs.get("title")
        x_label = fig_kwargs.get("x_label") if not x_label else x_label
        y_label = fig_kwargs.get("y_label") if not y_label else y_label

        ax.set_xlabel(x_label if x_label else "", fontname="Times New Roman", fontsize=16)
        ax.set_ylabel(y_label if y_label else "", fontname="Times New Roman", fontsize=16)

        # If figure is created set layout and store if wanted
        if fig:
            fig.tight_layout()

            # Save the graph
            if save_as:
                plt.savefig(save_as, bbox_inches="tight")

            # Show the graph
            if fig_show:
                plt.show()
            else:
                plt.close()

        # Return
        return ax, plt

    def plot_all_modalities(self, sample, x_label=None, save_as=None):
        """
        Plot separate line plots with all modalities of data

        :param sample: instance of handwriting sample
        :type sample: handwriting_sample.HandwritingSample
        :param x_label: label of X axis
        :param save_as: setup save location if you want to save a file
        """

        # Go over modalities and plot them
        df_data = sample.data_pandas_dataframe
        for col in df_data:
            # Set labels
            x_label = "sample" if not x_label else x_label
            y_label = col

            # Plot lines
            self.plot_line(df_data[col], x_label, y_label, save_as=save_as)

    @staticmethod
    def plot_line(data, x_label, y_label, fig_show=True, save_as=None, fig_kwargs=None):
        """
        Plot line plots for input data

        :param data: input data array
        :param x_label: label of X axis
        :param y_label: label of Y axis
        :param fig_show: True/False value to show the figure
        :param save_as: setup save location if you want to save a file
        :return: axis and figure of the plot
        """

        # Prepare the figure settings
        fig_kwargs = fig_kwargs if fig_kwargs else {
            "fig_size": (15, 4),
            "show_ticks": True,
            "x_label": x_label,
            "y_label": y_label,
            "shade": True,
            "title": f"{y_label}",
            "colors": ["red", "blue", "green"]
        }

        # Create figure if axes not inserted
        fig, ax = plt.subplots(1, 1, figsize=fig_kwargs.get("fig_size"))

        # Plot
        ax.plot(data, linewidth=2, alpha=0.7)

        # Set labels
        title = fig_kwargs.get("title")
        x_label = fig_kwargs.get("x_label")
        y_label = fig_kwargs.get("y_label")

        ax.set_title(title if title else "", fontname="Times New Roman", fontsize=12)
        ax.set_xlabel(x_label if x_label else "", fontname="Times New Roman", fontsize=16)
        ax.set_ylabel(y_label if y_label else "", fontname="Times New Roman", fontsize=16)

        # Set grid
        ax.yaxis.grid(True)
        ax.xaxis.grid(True)

        # Set tight layout
        fig.tight_layout()

        # Save the graph
        if save_as:
            plt.savefig(save_as, bbox_inches="tight", quality=100)

        # Show the graph
        if fig_show:
            plt.show()
        else:
            plt.close()

        return ax, plt
