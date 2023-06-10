import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statistics as s

st.title("Stats 21 Streamlit Project")

file = st.file_uploader("Upload a csv file")

if file is not None:
    df = pd.read_csv(file, encoding = 'unicode_escape')
    st.dataframe(data = df)

    # Statistics
    st.header("Overall Data Statistics:")
    st.text("Number of rows: " + str(df.shape[0]))
    st.text("Number of columns : " + str(df.shape[1]))

    categorical = df.select_dtypes(include=['object']).columns
    st.text("Categorical columns: " + ", ".join(categorical))
    st.text("Number of categorical columns: " + str(len(categorical)))

    numerical = df.select_dtypes(include=['int', 'float']).columns
    st.text("Numerical columns: " + ", ".join(numerical))
    st.text("Number of numerical columns: " + str(len(numerical)))

    boolean = df.select_dtypes(include=['bool']).columns
    st.text("Boolean columns: " + ", ".join(boolean))
    st.text("Number of boolean columns: " + str(len(boolean)))

    # Choosing a column
    st.header("Column Statistics:")
    option = st.selectbox("Select a column", df.columns)

    st.write('You selected:', option)

    column = df[option]
    st.dataframe(data = column)

    # column variable is numeric
    if option in numerical:
        five_num = pd.DataFrame({"Minimum": min(list(column)), 
                                 "Lower Quartile": list(column.quantile([0.25]))[0], 
                                 "Median": s.median(list(column)),
                                 "Upper Quartile": list(column.quantile([0.75]))[0],
                                 "Maximum": max(list(column))
                                 }, index=[0]
                                 )

        five_num.index = ["Value"]

        st.subheader("Five Number Summary:")
        st.table(five_num)

        st.subheader("Distribution Plot:")

        plot_list = ["Histogram", "Box Plot"]
        plot = st.selectbox("Select type of graph", plot_list)

        st.subheader(plot)

        if plot == "Histogram":
            # Parameter "hue" to group the column
            hue_list = [str(x) for x in list(categorical)]
            hue_list.insert(0, None)
            hue_option = st.selectbox("Select a categorical variable to group by: ", hue_list)

            # Parameter "kind" to change graph
            kind_list = ["hist", "kde", "ecdf"]
            kind_option = st.selectbox("Select a type of graph", kind_list)

            # Plot the histogram
            fig = plt.figure(figsize = (10, 5))
            fig = sns.displot(data = df, x = option, hue = hue_option, kind = kind_option)
            st.pyplot(fig)

        elif plot == "Box Plot":
            # Parameter "x" to compare to a categorical variable
            x_list = [str(i) for i in list(categorical)]
            x_list.insert(0, None)
            x_option = st.selectbox("Select a categorical variable to group by: ", x_list)

            # Vertical or Horizontal Box Plots
            orientation = ["Vertical", "Horizontal"]
            orientation_option = st.selectbox("Select the box plot's orientation", orientation)

            y_option = option
            if orientation_option == "Horizontal":
                if x_option == None:     
                    x_option = option
                    y_option = None
                else:
                    temp = x_option
                    x_option = option
                    y_option = temp

            # Plot the box plot
            fig, ax = plt.subplots()
            fig.ax = sns.boxplot(data = df, x = x_option, y = y_option)
            st.pyplot(fig)
        
    # column variable is categorical
    elif option in categorical:
        proportion = column.value_counts(normalize=True)
        st.table(proportion)

        # Adjust width
        width_option = st.slider("Select a width", 0.0, 1.5, 0.5)

        # Choose color
        color_list = ["red", "orange", "yellow", "green", "blue", "purple", "gray", "black"]
        color_option = st.selectbox("Select color of bar graph", color_list)

        # Plot the bar graph
        fig, ax = plt.subplots()
        fig.ax = plt.bar(x = proportion.index, height = proportion, width = width_option, color = color_option)
        plt.xlabel(option)
        plt.ylabel("Proportion")
        st.pyplot(fig)

    



