import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns


st.sidebar.title('Whatsapp Chat Analyser')
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")  ##to decode data
    ## st.text(data) ## to display text
    df=preprocessor.preprocess(data)



    #fetch unique users
    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user=st.sidebar.selectbox("Show Analysis wrt",user_list) ##dropdown menu
    ##stats area
    if st.sidebar.button("Show Analysis"):
        num_messages,words,num_media_messages,links=helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1,col2,col3,col4=st.columns(4)
        with col1: #to organize content within columns
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(links)
        ## timeline for monthly and yearly analysis
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        ## daily timeline
        st.title("Daily Timeline")
        daily_timeline=helper.daily_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'],color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    ##activity map
        st.title("Activity Map")
        col1,col2=st.columns(2)
        with col1:

            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
         st.header("Most Busy Month")
         busy_month = helper.month_activity_map(selected_user, df)
         fig, ax = plt.subplots()
         ax.bar(busy_month.index, busy_month.values,color='orange')
         plt.xticks(rotation='vertical')
         st.pyplot(fig)

   ##heatmap
        st.title("Weekly Activity Heatmap")
        pivot=helper.activity_heatmap(selected_user,df)
        plt.figure(figsize=(20, 6))
        fig,ax=plt.subplots()
        ax=sns.heatmap(pivot)
        plt.yticks(rotation='horizontal')
        st.pyplot(fig)







    ##most busiest users in the group
        if selected_user=='Overall':
            st.title('Most Busy Users')
            x,new_df=helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1,col2=st.columns(2)


            with col1:
                ax.bar(x.index, x.values,color='red')  ## ax-subplots or set of subplots fig-entire figure
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

    ## word cloud
        st.title("WordCloud")
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

    ##most common words
        st.title("Most Common Words")
        most_common_df=helper.most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1]) ##for horizontal bar graph
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


## emoji analysis
        st.title("Emoji Analysis")
        emoji_df=helper.emoji_helper(selected_user,df)
        col1,col2=st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:

            fig, ax = plt.subplots()

        # Set a font that supports emojis
            prop = fm.FontProperties(fname=fm.findfont(fm.FontProperties(family="Segoe UI Emoji")), size=14)

            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f", textprops={'fontproperties': prop})
            st.pyplot(fig)


