import re
import tkinter
from tkinter import Button, Label, Radiobutton, IntVar, filedialog, messagebox, Text, Entry,Scrollbar, Checkbutton, OptionMenu
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandastable import Table, TableModel

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

class GUI:
    def __init__(self):
        self.main_window = tkinter.Tk()
        self.file_frame = tkinter.Frame(self.main_window)
        self.outlier_frame = tkinter.Frame(self.main_window)
        self.duplicate_frame = tkinter.Frame(self.main_window)
        self.middle_frame = tkinter.Frame(self.main_window)
        self.visualize_frame = tkinter.Frame(self.main_window)
        self.bottom_frame = tkinter.Frame(self.main_window)

        self.main_window.title('Data Cleaning and Analysis')
        self.main_window.geometry('1400x500')

        self.csv_upload_btn = Button(
            self.file_frame,
            text='Choose File',
            command=lambda: self.open_file()
        )
        self.csv_upload = Label(
            self.file_frame,
            text='Upload data in csv format '
        )
        self.csv_upload.pack(side='left')
        self.csv_upload_btn.pack(side='left')

        self.file_frame.pack()
        self.main_window.mainloop()

    def open_file(self):
        #for frame in [self.outlier_frame,self.duplicate_frame,self.middle_frame]:
        #    for widget in frame:
        #        widget.destroy()
        file_path = filedialog.askopenfile(mode='r', filetypes=[('CSV', '*.csv')])
        if file_path is not None:
            pass
        self.data = pd.read_csv(file_path, header=0)

        self.data_label = Label(self.file_frame,text = re.findall("/(\w+.csv)'",f"{file_path}")[0])
        self.data_label.pack(side='bottom')
        self.file_frame.pack()

        self.statistics = pd.DataFrame(data=self.data.describe())
        iqr = pd.DataFrame({'iqr': self.statistics.iloc[6] - self.statistics.iloc[4]}, index=self.statistics.columns)
        median = pd.DataFrame({'median':self.data.median(numeric_only=True)}, index=self.statistics.columns)
        self.statistics = pd.concat([self.statistics, iqr.transpose(),median.transpose()])
        self.statistics.round(3)

        wordCounts = {}
        self.textDataButton = ([],[])
        self.wordCols=list(set(self.data.columns)-set(self.statistics.columns))
        for column in self.wordCols:
            List_of_words = self.data[column].str.split()
            counts = dict()
            for word in List_of_words:
                counts[str(word)] = counts.get(str(word), 0) + 1
            wordCounts[column]=counts

            ##initialize intvars for text button while in the loop
            self.textDataButton[1].append(IntVar())
            self.textDataButton[1][-1].set(0)
            self.textDataButton[0].append(Checkbutton(self.visualize_frame, text=column, variable=self.textDataButton[1][-1], \
                         onvalue=1, offvalue=0))
            self.textDataButton[0][-1].pack(side=tkinter.LEFT)

        self.word_counts = pd.DataFrame(wordCounts)

        self.csv_upload_btn.grid_forget()
        self.csv_upload.grid_forget()

        # display data analysis tools:

        # top frame
        self.outlier_radio_var = IntVar()
        self.outlier_radio_var.set(1)
        self.outlier_buttons = []
        self.outlier_detection = Label(
            self.outlier_frame,
            text="Detect Outliers in Selected Column"
        )
        self.outlier_detection.pack(side='top')
        i = 0
        self.visualizeButton = ([],[])
        for column in self.statistics.columns:
            self.outlier_buttons.append(
                Radiobutton(self.outlier_frame, text=column, variable=self.outlier_radio_var, value=i + 1))
            self.outlier_buttons[i].pack(side='left')
            i += 1

            ## initialize the button intvars for visualizebutton while in the for loop.
            self.visualizeButton[1].append(IntVar())
            self.visualizeButton[1][-1].set(0)
            self.visualizeButton[0].append(Checkbutton(self.visualize_frame, text=column, variable=self.visualizeButton[1][-1], \
                         onvalue=1, offvalue=0))
            self.visualizeButton[0][-1].pack(side=tkinter.LEFT)

        self.ok_outliers = Button(self.outlier_frame, text='OK', command=self.perform_outlier_detection)
        self.ok_outliers.pack(side='left')

        self.missing_value_detection_button = Button(self.middle_frame, text='Missing Value Detection',
                                                     command=self.detect_missing_values)
        self.missing_value_detection_button.pack(side='left')

        self.duplicate_detection = Label(
            self.duplicate_frame,
            text="Detect Duplicates in Selected Columns"
        )
        self.duplicate_detection.pack(side='top')
        self.dupeRowButton = ([],[])
        for column in self.data.columns:
            self.dupeRowButton[1].append(IntVar())
            self.dupeRowButton[1][-1].set(0)
            self.dupeRowButton[0].append(Checkbutton(self.duplicate_frame, text=column, variable=self.dupeRowButton[1][-1], \
                         onvalue=1, offvalue=0))
            self.dupeRowButton[0][-1].pack(side=tkinter.LEFT)


        self.duplicate_row_detection_button = Button(self.duplicate_frame, text='Duplicate Row Detection',
                                                     command=self.detect_duplicate_rows)
        self.duplicate_row_detection_button.pack(side='left')

        self.visualize_data_button = Button(self.visualize_frame, text='Histogram for Selected Columns',
                                            command=self.visualise_data)
        self.visualize_data_button.pack(side='left')


        self.column_naming_button = Button(self.middle_frame, text='Column Naming/Renaming',
                                           command=self.show_column_naming_window)
        self.column_naming_button.pack(side='left')

        self.add_transformed_column_button = Button(self.middle_frame, text='Add Transformed Data Column',
                                                    command=self.show_add_transformed_column_window)
        self.add_transformed_column_button.pack(side='left')

        self.show_basic_statistics_button = Button(self.bottom_frame, text='Show Basic Statistics',
                                                   command=self.show_basic_statistics)
        self.show_basic_statistics_button.pack(side='left')

        self.handle_missing_values_button = Button(self.middle_frame, text='Handle Missing Values',
                                                   command=self.handle_missing_values)
        self.handle_missing_values_button.pack(side='left')

        self.cor_matrix_button = Button(self.bottom_frame, text='Show Correlation Matrix', command=self.display_correlation_matrix)
        self.cor_matrix_button.pack(side='left')

        self.scatter_plot_button = Button(self.bottom_frame, text='Create Scatter Plot', command=self.create_scatter_plot)
        self.scatter_plot_button.pack(side='left')

        self.save_csv_button = Button(self.bottom_frame, text='Save as CSV', command=self.save_data_as_csv)
        self.save_csv_button.pack(side='left')

        self.restart_button = Button(self.bottom_frame, text='Restart and Upload New Dataset',
                                     command=self.restart_program)
        self.restart_button.pack(side='left')

        self.outlier_frame.pack()
        self.duplicate_frame.pack()
        self.middle_frame.pack()
        self.visualize_frame.pack()
        self.bottom_frame.pack()

    def perform_outlier_detection(self):
        threshold1 = {'lower': (self.statistics.loc['mean'] - 1.5 * self.statistics.loc['iqr']),
                                   'upper': (self.statistics.loc['mean'] + 1.5 * self.statistics.loc['iqr'])}

        column = self.statistics.columns[self.outlier_radio_var.get() - 1]
        datakey=[]

        for i in range(0,len(self.data[column])) :
            if int(self.data[column][i]) > threshold1['upper'][column]:
                datakey.append(True)
            elif int(self.data[column][i]) < threshold1['lower'][column]:
                datakey.append(True)
            else:
                datakey.append(False)

        outlier_data = self.data[column][datakey]
        outlierDisplayBox = tkinter.Tk()
        outlierDisplayBox.geometry('800x400')
        textWidget = Text(outlierDisplayBox, wrap='none', height=20, width=50)
        textWidget.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Create a Scrollbar for the Text widget
        scroll_y = Scrollbar(outlierDisplayBox, command=textWidget.yview)
        scroll_y.grid(row=0, column=1, sticky='ns')
        textWidget.config(yscrollcommand=scroll_y.set)

        # Display the series content in the Text widget
        series_content = outlier_data.astype(str)
        textWidget.insert(tkinter.END, series_content)

        # Make the Text widget read-only
        textWidget.config(state=tkinter.DISABLED)
        outlierDisplayBox.title(f'Outliers within {column}')

        # Allow resizing of the window
        outlierDisplayBox.columnconfigure(0, weight=1)
        outlierDisplayBox.rowconfigure(0, weight=1)
        outlierDisplayBox.mainloop()

    def detect_missing_values(self):
        missing_values = self.data.isnull()
        missing_rows = self.data[missing_values.any(axis=1)]
        missingValueWindow = tkinter.Tk()
        if len(missing_rows[self.data.columns[0]])==0:
            missing_rows = 'No Missing Values'

        textWidget = Text(missingValueWindow, wrap='none', height=20, width=50)
        textWidget.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Create a Scrollbar for the Text widget
        scroll_y = Scrollbar(missingValueWindow, command=textWidget.yview)
        scroll_y.grid(row=0, column=1, sticky='ns')
        textWidget.config(yscrollcommand=scroll_y.set)

        # Display the series content in the Text widget
        series_content = missing_rows.astype(str)
        textWidget.insert(tkinter.END, series_content)

        # Make the Text widget read-only
        textWidget.config(state=tkinter.DISABLED)
        missingValueWindow.title("Missing Value Detection")

        # Allow resizing of the window
        missingValueWindow.columnconfigure(0, weight=1)
        missingValueWindow.rowconfigure(0, weight=1)
        missingValueWindow.mainloop()

    def detect_duplicate_rows(self):

        dupeRows=[]
        for i in range(0,len(self.dupeRowButton[1])):
            if self.dupeRowButton[1][i].get()==1:
                dupeRows.append(self.data.columns[i])
        duplicate_rows = self.data[self.data.duplicated(subset = dupeRows, keep=False)]

        duplicateRowsWindow = tkinter.Tk()
        if len(duplicate_rows[self.data.columns[0]])==0:
            duplicate_rows = 'No Duplicate Rows'

        textWidget = Text(duplicateRowsWindow, wrap='none', height=20, width=50)
        textWidget.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Create a Scrollbar for the Text widget
        scroll_y = Scrollbar(duplicateRowsWindow, command=textWidget.yview)
        scroll_y.grid(row=0, column=1, sticky='ns')
        textWidget.config(yscrollcommand=scroll_y.set)

        # Display the series content in the Text widget
        series_content = str(duplicate_rows)
        textWidget.insert(tkinter.END, series_content)

        # Make the Text widget read-only
        textWidget.config(state=tkinter.DISABLED)
        duplicateRowsWindow.title("Duplicate Row Detection")

        # Allow resizing of the window
        duplicateRowsWindow.columnconfigure(0, weight=1)
        duplicateRowsWindow.rowconfigure(0, weight=1)
        duplicateRowsWindow.mainloop()

    def show_column_naming_window(self):
        self.column_naming_window = tkinter.Toplevel(self.main_window)
        self.column_naming_window.title("Column Naming/Renaming")

        self.column_naming_label = Label(self.column_naming_window, text="Select Column to Rename:")
        self.column_naming_label.pack()

        self.column_naming_radio_var = IntVar()
        self.column_naming_buttons = []
        for i in range(0, len(self.data.columns)):
            self.column_naming_buttons.append(
                Radiobutton(self.column_naming_window, text=self.data.columns[i], variable=self.column_naming_radio_var,
                            value=i + 1))
            self.column_naming_buttons[i].pack(side='left')

        self.new_column_name_label = Label(self.column_naming_window, text="Enter New Column Name:")
        self.new_column_name_label.pack()

        self.new_column_name_entry = Entry(self.column_naming_window)
        self.new_column_name_entry.pack()

        self.column_naming_ok_button = Button(self.column_naming_window, text='OK', command=self.rename_column)
        self.column_naming_ok_button.pack()

    def rename_column(self):
        selected_column_index = self.column_naming_radio_var.get() - 1
        new_column_name = self.new_column_name_entry.get()

        if new_column_name and 0 <= selected_column_index < len(self.data.columns):
            old_column_name = self.data.columns[selected_column_index]
            self.data.rename(columns={old_column_name: new_column_name}, inplace=True)
            messagebox.showinfo(title="Column Naming/Renaming",
                                message=f"Successfully changed column from '{old_column_name}' to '{new_column_name}'.")
            self.column_naming_window.destroy()

    def show_add_transformed_column_window(self):
        self.add_transformed_column_window = tkinter.Toplevel(self.main_window)
        self.add_transformed_column_window.title("Add Transformed Data Column")

        self.transformed_column_label = Label(self.add_transformed_column_window, text="Select Column to Transform:")
        self.transformed_column_label.pack()

        self.transformed_column_radio_var = IntVar()
        self.transformed_column_buttons = []

        for i in range(0, len(self.statistics.columns)):
            self.transformed_column_buttons.append(
                Radiobutton(self.add_transformed_column_window, text=self.statistics.columns[i],
                            variable=self.transformed_column_radio_var, value=i + 1))
            self.transformed_column_buttons[i].pack(side='left')

        self.transformation_label = Label(self.add_transformed_column_window, text="Select Transformation:")
        self.transformation_label.pack()

        self.transformation_options = ["Square", "Square Root", "Log"]
        self.transformation_var = tkinter.StringVar()
        self.transformation_var.set(self.transformation_options[0])

        self.transformation_menu = tkinter.OptionMenu(self.add_transformed_column_window, self.transformation_var,
                                                      *self.transformation_options)
        self.transformation_menu.pack()

        self.add_transformed_column_ok_button = Button(self.add_transformed_column_window, text='OK',
                                                       command=self.add_transformed_column)
        self.add_transformed_column_ok_button.pack()

    def add_transformed_column(self):
        selected_column_index = self.transformed_column_radio_var.get() - 1
        transformation_type = self.transformation_var.get()

        if 0 <= selected_column_index < len(self.statistics.columns):
            selected_column = self.statistics.columns[selected_column_index]

            if transformation_type == "Square":
                new_column = self.data[selected_column] ** 2
            elif transformation_type == "Square Root":
                new_column = math.sqrt(self.data[selected_column])
            elif transformation_type == "Log":
                new_column = np.log(self.data[selected_column] + 1)  # Adding 1 to avoid log(0)

            new_column_name = f"{transformation_type.lower()}_{selected_column}"
            self.data[new_column_name] = new_column

            messagebox.showinfo(title="Add Transformed Data Column",
                                message=f"Successfully created column '{new_column_name}' as {transformation_type} of column '{selected_column}'.")

            self.add_transformed_column_window.destroy()

    def show_basic_statistics(self):
        statistics_text = str(self.statistics.round(3))
        messagebox.showinfo(title="Basic Statistics", message=statistics_text)
        for column in self.word_counts:
            word_count_text = str(self.word_counts[column].dropna())
            messagebox.showinfo(title='Text Summary',message=word_count_text)

    def handle_missing_values(self):
        missing_values = self.data.isnull().sum()

        if missing_values.any():
            # Ask the user how to handle missing values
            choice = messagebox.askquestion("Handle Missing Values",
                                            "Do you want to delete rows with missing values? or they will be replaced with the mean.")
            if choice == 'yes':
                # Delete rows with missing values
                self.data.dropna(inplace=True)
                messagebox.showinfo("Handling Missing Values", "Rows with missing values deleted.")
            else:
                # Replace missing values with the mean
                for column in self.data.columns:
                    if self.data.dtypes[column] is float or int:
                        self.data.fillna(self.data[column].mean(), inplace=True)
                    else:
                        self.data.fillna('N/A', inplace=True)

                messagebox.showinfo("Handling Missing Values", "Missing values replaced with the mean if numeric, or N/A else.")
        else:
            messagebox.showinfo("Handling Missing Values", "No missing values found.")

    def visualise_data(self):
        visualize = []
        for i in range(0, len(self.visualizeButton[1])):
            if self.visualizeButton[1][i].get() == 1:
                visualize.append(self.data[self.statistics.columns[i]])
        if visualize:
            plt.figure(figsize=(10, 6))
            for column in visualize:
                plt.hist(column, bins=20, alpha=0.5, label=column.name)
            plt.legend(loc='upper right')
            plt.title('Data Visualization')

            plt.show()

        for i in range(0,len(self.textDataButton[1])):
            if self.textDataButton[1][i].get()==1:
                plt.figure(figsize=(10, 6))
                plt.hist(self.data[self.wordCols[i]], bins=20, alpha=0.5, label=self.wordCols[i])
                plt.title('Data Visualization')
                plt.show()



    def display_correlation_matrix(self):
        correlation_matrix = self.data[self.statistics.columns].corr()

        # Display correlation matrix in a pandastable widget
        correlation_matrix_window = tkinter.Tk()
        correlation_matrix_window.title("Correlation Matrix")

        frame = tkinter.Frame(correlation_matrix_window)
        frame.pack(fill='both', expand=True)

        # Create a TableModel and a Table widget
        model = TableModel(correlation_matrix)
        table = Table(frame, model=model)

        table.show()

        correlation_matrix_window.mainloop()

    def create_scatter_plot(self):
        scatter_plot_window = tkinter.Tk()
        scatter_plot_window.title("Scatter Plot")
        scatter_plot_window.geometry('200x200')

        # Create dropdown menus for x and y columns
        x_column_label = Label(scatter_plot_window, text="Select X Column:")
        x_column_label.pack()

        x_columns = list(self.statistics.columns)
        self.x_column_var = tkinter.StringVar()
        x_column_menu = OptionMenu(scatter_plot_window, self.x_column_var, *x_columns)
        x_column_menu.pack()

        y_column_label = Label(scatter_plot_window, text="Select Y Column:")
        y_column_label.pack()

        y_columns = list(self.statistics.columns)
        self.y_column_var = tkinter.StringVar()
        y_column_menu = OptionMenu(scatter_plot_window, self.y_column_var, *y_columns)
        y_column_menu.pack()

        plot_button = Button(scatter_plot_window, text="Plot", command=self.plot_scatter)
        plot_button.pack()

        scatter_plot_window.mainloop()

    def plot_scatter(self):
        x_column = self.x_column_var.get()
        y_column = self.y_column_var.get()

        if x_column and y_column:
            scatter_plot_window = tkinter.Toplevel(self.main_window)
            scatter_plot_window.title("Scatter Plot")

            fig, ax = plt.subplots()
            ax.scatter(self.data[x_column], self.data[y_column])
            ax.set_xlabel(x_column)
            ax.set_ylabel(y_column)
            ax.set_title(f"Scatter Plot: {x_column} vs {y_column}")

            canvas = FigureCanvasTkAgg(fig, master=scatter_plot_window)
            canvas.get_tk_widget().pack()
            canvas.draw()

            scatter_plot_window.mainloop()
        else:
            messagebox.showwarning("Warning", "Please select both X and Y columns.")

    def save_data_as_csv(self):
        if not self.data.empty:
            # Save current data as a CSV file
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if file_path:
                self.data.to_csv(file_path, index=False)
                messagebox.showinfo("Save as CSV", f"Data saved as {file_path}")
            else:
                messagebox.showwarning("Warning", "Please provide a valid file name.")
        else:
            messagebox.showwarning("Warning", "No data to save.")

    def restart_program(self):
        # Destroy all frames within the main window
        for frame in [self.file_frame, self.outlier_frame,self.visualize_frame,self.duplicate_frame, self.middle_frame, self.bottom_frame]:
            frame.destroy()

        # Rebuild the main window with the option to upload a new CSV
        self.file_frame = tkinter.Frame(self.main_window)
        self.outlier_frame = tkinter.Frame(self.main_window)
        self.duplicate_frame = tkinter.Frame(self.main_window)
        self.middle_frame = tkinter.Frame(self.main_window)
        self.visualize_frame = tkinter.Frame(self.main_window)
        self.bottom_frame = tkinter.Frame(self.main_window)

        self.csv_upload_btn = Button(
            self.file_frame,
            text='Choose File',
            command=self.open_file
        )
        self.csv_upload = Label(
            self.file_frame,
            text='Upload data in csv format '
        )
        self.csv_upload.pack(side='left')
        self.csv_upload_btn.pack(side='left')

        self.file_frame.pack()
        self.main_window.mainloop()

GUI()