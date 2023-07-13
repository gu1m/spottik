# importando bibliotecas
import pandas as pd
import plotly.express as px
import statistics as sts 
import streamlit as st
import plotly.figure_factory as ff
import plotly.graph_objects as go
import seaborn as sns
import numpy as np

df1 = pd.read_csv("C:\\Users\\gguim\\OneDrive\\Desktop\\appdata\\tiktok.csv")
df2 = pd.read_csv("C:\\Users\\gguim\\OneDrive\\Desktop\\appdata\\spotify.csv")

df1 = df1.drop(["date","platform_name","platform_song_id","product_code","album","label_name","sublabel","territory","creations","favorites"], axis=1)
df2 = df2.drop(["free_saves","premium_saves","playlists_algorithmics","date","date_release","album__code","n_discovery_flag","y_discovery_flag","y_streams_offline",
             "n_streams_offline","y_shuffle","n_shuffle","y_repeat_play","n_repeat_play","source__artist","source__radio","source__others","device__personal_computer","device__cell_phone","device__tablet","device__smart_tv",
             "device__connected_audio","device__gaming_console","device__car_application","device__others","os__windows","os__android","os__ios","os__mac","os__linux","browser","os__others","account__paid","account__ad","account__trial",
             "account__partner","account__partner_free","account__deleted","gender__male","gender__female","gender__unknown","free_saves","premium_saves","playlists_algorithmics","source__others_playlist","source__album"],axis=1)


df1 = df1.groupby(df1["isrc"]).first().reset_index()
df1.dropna(inplace=True)
df2 = df2.groupby(df2["isrc"]).first().reset_index()
df2.dropna(inplace=True)


df = pd.merge(df1, df2, on='isrc', how='left')


avg_watchtime = df1["avg_watchtime"]
likes = df1["likes"]
comments = df1["comments"]
shares = df1["shares"]
video_views = df1["video_views"]
corr = df1.corr(numeric_only=True)

# configurando página
st.set_page_config(
    page_title="Dataframe Spotify/Tiktok",
    page_icon="bar_chart:",
    layout="wide"
    
)
st.header("Dataframe Spotify/Tiktok")

st.markdown("""---""")

# configurações da barra lateral
opcoes = ["Tiktok","Spotify","Tiktok/Spotify"]
indi_geral = st.sidebar.selectbox("Escolha quais dados serão analisados", opcoes)

if indi_geral == "Tiktok":

    # vendo o total de músicas no Dataframe
    total_musicas = len(df1["isrc"])

    # analisando o total de artistas no Dataframe
    data = df1.drop_duplicates(subset="artist", keep='first')
    total_artistas = len(data["artist"])

    col1,col2,col3 = st.columns(3)

    col1.metric("Total de músicas", total_musicas)
    col3.metric("Número de artistas", total_artistas)

    st.subheader("""Amostra de Dados""")
    st.write(df1.head())
    st.markdown("---")

    col4, col5, col6 =st.columns(3)
    
    media_views = round(sts.mean(df1["video_views"]),2)
    media_avgwatch= round(sts.mean(df1["avg_watchtime"]),2)
    media_likes = round(sts.mean(df1["likes"]),2)
    media_comments = round(sts.mean(df1["comments"]),2)
    media_shares = round(sts.mean(df1["shares"]),2)
    moda_art = sts.mode(df1["artist"])
    moda_genre = sts.mode(df1["label_provided_genre"])
    moda_genrepla = sts.mode(df1["platform_classified_genre"])
    moda_content = sts.mode(df1["content_type"])
    
    
    
    
    with col4:
        # vendo qual o artista mais popular no dataframe
        st.write("""Música mais popular no Tiktok:""")
        df.nlargest(1, 'video_views')[['song_title','artist',"video_views","likes","avg_watchtime"]]
    
    col5.metric("Média de views", media_views)
    
    col6.metric("Média de tempo assistido",media_avgwatch)
    
    col7, col8, col9 = st.columns(3)

    col7.metric("Média de likes",media_likes)
    
    col8.metric("Média de comentarios",media_comments)
    
    col9.metric("Artista que mais aparece",moda_art)

    col10,col11,col12 = st.columns(3)

    col10.metric("Moda do estilo músical", moda_genre)

    col11.metric("Moda do gênero", moda_genrepla)

    col12.metric("Content que mais aparece",moda_content)


    st.markdown("---")

    st.subheader("Gráficos gerais Tiktok")


    col13 , col14 = st.columns(2)


    with col13:
        fig = go.Scatter(x=df1.video_views ,name="Views",mode="markers", marker=dict(color="#5e9fa3"))
        data = [fig]
        layout = go.Layout(title="Número de músicas relacionada com o total de views")
        figure = go.Figure(data=data, layout=layout)
        figure.update_layout(
            xaxis_title="views",
            yaxis_title="Número de Músicas"
        )
        st.write(figure)
    
    with col14:
        fig = go.Scatter(x=avg_watchtime ,name="Views",mode="markers", marker=dict(color="#73626e"))
        data = [fig]
        layout = go.Layout(title="Número de músicas relacionada com o número de avg_watchtime")
        figure = go.Figure(data=data, layout=layout)
        figure.update_layout(
            xaxis_title="avg_watchtime",
            yaxis_title="número de músicas"
        )
        st.write(figure)

    col15 , col16 = st.columns(2)

    with col15:
        fig = go.Scatter(x=video_views,y=avg_watchtime ,name="Views",mode="markers", marker=dict(color="#9e0c39"))
        data = [fig]
        layout = go.Layout(title="Avg_watchtime relacionada com o número de views")
        figure = go.Figure(data=data, layout=layout)
        figure.update_layout(
            xaxis_title="views",
            yaxis_title="avg_watchtime"
        )
        st.write(figure)
    
    with col16:
        fig = go.Scatter(x=likes,y=avg_watchtime ,name="Views",mode="markers", marker=dict(color="#5e9fa3"))
        data = [fig]
        layout = go.Layout(title="Avg_watchtime relacionada com o número de Likes")
        figure = go.Figure(data=data, layout=layout)
        figure.update_layout(
            xaxis_title="Likes",
            yaxis_title="avg_watchtime"
        )
        st.write(figure)
    
    col17, col18 =  st.columns(2)

    with col17:
        fig = go.Scatter(x=comments,y=avg_watchtime ,name="Views",mode="markers", marker=dict(color="#333333"))
        data = [fig]
        layout = go.Layout(title="Avg_watchtime relacionada com o número de comentarios")
        figure = go.Figure(data=data, layout=layout)
        figure.update_layout(
            xaxis_title="comentarios",
            yaxis_title="avg_watchtime"
        )
        st.write(figure)
    
    with col18:
        fig = go.Scatter(x=shares,y=avg_watchtime ,name="Views",mode="markers", marker=dict(color="#9e0c39"))
        data = [fig]
        layout = go.Layout(title="Avg_watchtime relacionada com o número de compartilhamentos")
        figure = go.Figure(data=data, layout=layout)
        figure.update_layout(
            xaxis_title="shares",
            yaxis_title="avg_watchtime"
        )
        st.write(figure)
    
    st.write(corr)

elif indi_geral == "Spotify":

    # vendo o total de músicas no Dataframe
    total_musicas = len(df2["isrc"])

    # analisando o total de artistas no Dataframe
    data = df2.drop_duplicates(subset="artist__name", keep='first')
    total_artistas = len(data["artist__name"])

    col19,col20,col21 = st.columns(3)

    col19.metric("Total de músicas", total_musicas)
    col21.metric("Número de artistas", total_artistas)

    st.subheader("""Amostra de Dados""")
    st.write(df2.head())
    st.markdown("---")

    media_streams = round(sts.mean(df2["streams"]),2)
    media_avgwatch= round(sts.mean(df2["stream_seconds_avg"]),2)/60
    moda_art = sts.mode(df2["artist__name"])
    media_idade = round(sts.mean(df2["age__35_44"]),2)
    media_lister = round(sts.mean(df2["listeners"]),2)
    
    col22, col23, col24 = st.columns(3)

    with col22:
        # vendo qual o artista mais popular no dataframe
        st.write("""Música mais popular no Tiktok:""")
        df.nlargest(1, 'video_views')[['song_title','artist',"video_views","likes","avg_watchtime"]]
    
    col23.metric("Média de streams", media_streams)
    col24.metric("Média de minutos ouvidos",media_avgwatch)

    col25, col26, col27 = st.columns(3)

    col25.metric("Artista que mais aparece", moda_art)
    col26.metric("Faixa de idade que mais escuta [35-44] e a média de ouvintes", media_idade)
    col27.metric("Média de ouvintes", media_lister)

    st.markdown("---")

    st.subheader("Gráficos gerais Spotify")

    col28, col29 = st.columns(2)

    with col28:
        fig = go.Scatter(x=df.streams ,name="Views",mode="markers", marker=dict(color="#5e9fa3"))
        data = [fig]
        layout = go.Layout(title="Número de músicas relacionada com o total de streams")
        figure = go.Figure(data=data, layout=layout)
        figure.update_layout(
            xaxis_title="streams",
            yaxis_title="Número de Músicas"
        )
        st.write(figure)
    
    avg_watchtime  = df["stream_seconds_avg"]/60
    with col29:
        fig = go.Scatter(x=avg_watchtime ,name="Views",mode="markers", marker=dict(color="#73626e"))
        data = [fig]
        layout = go.Layout(title="Avg_watchtime em minutos relacionada com o número de músicas")
        figure = go.Figure(data=data, layout=layout)
        figure.update_layout(
            xaxis_title="avg_watchtime",
            yaxis_title="Número de músicas"
        )
        st.write(figure)
    col30 , col31 = st.columns(2)
    with col30:
        fig = go.Scatter(x=avg_watchtime,y=df.streams ,name="Views",mode="markers", marker=dict(color="#333333"))
        data = [fig]
        layout = go.Layout(title="Avg_watchtime em minutos relacionada com o número de streams")
        figure = go.Figure(data=data, layout=layout)
        figure.update_layout(
            xaxis_title="avg_watchtime",
            yaxis_title="streams"
        )
        st.write(figure)
    
    with col31:
        fig = go.Scatter(x=df.listeners,y=df.streams ,name="Views",mode="markers", marker=dict(color="#333333"))
        data = [fig]
        layout = go.Layout(title="Ouvintes relacionada com o número de streams")
        figure = go.Figure(data=data, layout=layout)
        figure.update_layout(
            xaxis_title="ouvintes",
            yaxis_title="streams"
        )
        st.write(figure)
    
   
    corr = df2.corr(numeric_only=True)
    st.write(corr)

elif indi_geral == "Tiktok/Spotify":
    # vendo o total de músicas no Dataframe
    total_musicas = len(df["isrc"])

    # analisando o total de artistas no Dataframe
    data = df.drop_duplicates(subset="artist", keep='first')
    total_artistas = len(data["artist"])

    col1,col2,col3 = st.columns(3)

    col1.metric("Total de músicas", total_musicas)
    col3.metric("Número de artistas", total_artistas)

    st.subheader("""Amostra de Dados""")
    st.write(df1.head())
    st.markdown("---")

    st.subheader("Gráficos gerais Spotify/Tiktok")

    col32, col33 = st.columns(2)

    with col32:
        fig = go.Box(y=df.video_views ,name="Tiktok", marker=dict(color="#bd3737"))
        fig2 = go.Box(y=df.streams ,name="Spotify", marker=dict(color="#98c3a1"))
        data = [fig,fig2]
        layout = go.Layout(title="Número de músicas em relação a visibilidade da música nas plataformas")
        figure = go.Figure(data = data, layout=layout)
        figure.update_layout(
            xaxis_title="número de músicas",
            yaxis_title="visibilidade"
        )
        st.write(figure)
    
    with col33:
        fig = go.Scatter(x=df.streams,y=df.video_views, mode="markers",name="Tiktok", marker=dict(color="#bd3737"))
        data=[fig]
        layout = go.Layout(title="Comparando a visibilidade nas duas plataformas")
        figure = go.Figure(data=data, layout=layout)
        figure.update_layout(
            xaxis_title="streams",
            yaxis_title="video_views"
        )
        st.write(figure)
    
    corr = df.corr(numeric_only=True)
    st.write(corr)
    










    
