import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn import linear_model
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

df = pd.read_csv('times2023_reduced.csv')
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)


def sec_func(time):
    if pd.isna(time):
        return time
    else:
        time = str(time)
        time = time.split(':')
        min_sec = float(time[0]) * 60
        sec_sec = float(time[1])
        return min_sec + sec_sec


df['Time1500Sec'] = df['Time1500'].apply(sec_func)
df['TimeMileSec'] = df['TimeMile'].apply(sec_func)
df['Time3000Sec'] = df['Time3000'].apply(sec_func)
df['Time5000Sec'] = df['Time5000'].apply(sec_func)

df['Time1500Sec'].fillna(value=df['Time1500Sec'].mean(), inplace=True)
df['TimeMileSec'].fillna(value=df['TimeMileSec'].mean(), inplace=True)
df['Time3000Sec'].fillna(value=df['Time3000Sec'].mean(), inplace=True)
df['Time5000Sec'].fillna(value=df['Time5000Sec'].mean(), inplace=True)

corrFrame = df[['Time1500Sec', 'TimeMileSec', 'Time3000Sec', 'Time5000Sec', '3kSteepleSec']]
corrFrame = pd.DataFrame(corrFrame)
corrFrame = corrFrame.corr(method='pearson')

corrMatrix = px.imshow(corrFrame, text_auto=True)
corrMatrix.show()

scatter_1500 = px.scatter(x=df['Time1500Sec'], y=df['3kSteepleSec'],
                      trendline='ols')
scatter_1500.show()

###########################################################
scatter_3000 = px.scatter(x=df['Time3000Sec'], y=df['3kSteepleSec'],
                      trendline='ols')
scatter_3000.show()

#########################################################
scatter_5000 = px.scatter(x=df['Time5000Sec'], y=df['3kSteepleSec'],
                      trendline='ols')
scatter_5000.show()
########################################################

X = df[['Time1500Sec']]
y = df[['3kSteepleSec']]

reg = linear_model.LinearRegression()
model1 = reg.fit(X, y)

print('\nVariance score for 1500: {}'.format(reg.score(X, y)))
######################################################

X = df[['Time1500Sec', 'Time3000Sec']]

model2 = reg.fit(X, y)
print(f'Variance score for 1500 and 3k: {reg.score(X, y)}')
######################################################

X = df[['Time3000Sec', 'Time5000Sec']]

model3 = reg.fit(X, y)
print(f'Variance score for 3k and 5k: {reg.score(X, y)}')
######################################################

X = df[['Time1500Sec', 'Time3000Sec', 'Time5000Sec']]
model4 = LinearRegression(fit_intercept=True)
model4.fit(X, y)
print(f'Variance score for 1500, 3k, and 5k: {model4.score(X, y)}')

######################################################

X = df[['Time1500Sec', 'TimeMileSec', 'Time3000Sec', 'Time5000Sec']]

model5 = reg.fit(X, y)
print(f'Variance score for 1500, Mile, 3k and 5k: {reg.score(X, y)}\n')
#######################################################

print(f'Coefficients for our linear regression with 1500, 3k, and 5k: {model4.coef_}')
print(f'Intercept for our linear regression with 1500, 3k, and 5k: {model4.intercept_}')
