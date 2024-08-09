import pandas as pd
from datetime import datetime
import seaborn as sns

df = pd.read_csv("C:\\Users\\hazal\\Downloads\\SentimentyBot-230523-162404\\SentimentyBot\\tweets_labeled.csv")
df.head()
df.info()
df.isnull().sum()
df.shape

# adım 3
# date değişkeninin zaman diliminin İstanbul zaman dilimine çevrilmesi
df["date"] = pd.to_datetime(df["date"])
df["date"] = df["date"].dt.tz_convert("Europe/Istanbul")
df["date"] = df["date"].dt.tz_localize(None)

# "month" değişkeninn oluşturulması ve düzenlenmesi
df["month"] = df["date"].dt.month_name()
df["tweet"] = df["tweet"].str.lower()
df["month"] = df["month"].replace({"December":"Aralık",
                                   'January': 'Ocak',
                                   'February': 'Şubat',
                                   'March': 'Mart',
                                   'April': 'Nisan',
                                   'May': 'Mayıs',
                                   'June': 'Haziran',
                                   'July': 'Temmuz',
                                   'August': 'Ağustos',
                                   'September': 'Eylül',
                                   'October': 'Ekim',
                                   'November': 'Kasım'
                                   })

# "seasons" değişkeninin oluşturulması
seasons = {"Ocak":"Kış",
           "Şubat":"Kış",
           'Mart': 'İlkbahar',
           'Nisan': 'İlkbahar',
           'Mayıs': 'İlkbahar',
           'Haziran': 'Yaz',
           'Temmuz': 'Yaz',
           'Ağustos': 'Yaz',
           'Eylül': 'Sonbahar',
           'Ekim': 'Sonbahar',
           'Kasım': 'Sonbahar',
           'Aralık': 'Kış'
           }

df["seasons"] = df["month"].map(seasons)

# gün değişkeninin oluşturulması

df["days"] = [date.strftime("%A") for date in df["date"]]
df["days"] = df["days"].replace({"Monday" : "Pazartesi",
                                 "Tuesday" : "Salı",
                                 "Wednesday" : "Çarşamba",
                                 "Thursday": "Perşembe",
                                 "Friday" : "Cuma",
                                 "Saturday" : "Cumartesi",
                                 "Sunday": "Pazar"})


# 4 saatlik aralıklarla günü 6'ya bölmesi
df["hour"] = df["date"].dt.hour
df["4hour_interval"] = (df["hour"] // 2) * 2
interval = {0:"0-2",
            2:"2-4",
            4: '4-6',
            6: '6-8',
            8: '8-10',
            10: '10-12',
            12: '12-14',
            14: '14-16',
            16: '16-18',
            18: '18-20',
            20: '20-22',
            22: '22-24'}

df.drop(["4hour_interval","hour"], axis =1, inplace=True )

cols = ["time_interval", "days", "seasons"]


def summary(dataframe, col_name, plot=False):
    # negatif tweetler için hedef değişken analizi
    dataframe = dataframe.loc[df["Durum"] == -1]
    print(pd.DataFrame({col_name: dataframe[col_name].value_counts(),
                        "Ratio": 100 * dataframe[col_name].value_counts() / len(dataframe)}))
    print("---------------------------------------------")

    if plot:
        sns.countplot(x=dataframe[col_name], data=dataframe)
        plt.show(block=True)

for col in cols:
    summary(df, col, plot=True)



