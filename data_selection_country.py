import pandas as pd
import simplejson as json

df = pd.read_csv("winter.csv")

df_c = pd.read_csv("dictionary.csv")

#df_unique = df['Discipline'].value_counts()

#df_unique = df.groupby(['Discipline']).sum()


#print(df_unique)

#df_unique_array = df['Discipline'].unique()

#df_unique = df['Discipline'].value_counts()
#print(df_unique)
#print(df_unique_array)

#print(df['Discipline'].unique())


'''
csv = open("discipline.csv", "w") 
#"w" indicates that you're writing strings to the file

columnTitleRow = "discipline\n"
csv.write(columnTitleRow)

for item in df_unique_array:
	row = item + "\n"
	csv.write(row)
'''
unique_array = df['Country'].unique()

for item in unique_array:
	replace_country = df_c[df_c['Code'] == item]['Country']
	#print(replace_country)
	print(item)
	if len(replace_country.values)>0:
		print(replace_country.values[0])
		df['Country']=df['Country'].replace(item, replace_country.values[0])

print(df['Country'])




df_discipline = df.groupby(["Discipline","Year","Country","Medal"])
#df_discipline.to_dict('list')
#print(df_discipline)

dfs=[]
dfs_new=[]


for key, item in df_discipline:
    dfs.append(df_discipline.get_group(key).drop(["City","Sport","Athlete","Gender","Event"],axis=1))
for df_item in dfs:
	df_item['Count']=df_item['Medal'].count()
	df_item=df_item.drop_duplicates()
	dfs_new.append(df_item)

df_combined = dfs_new[0]
for i in range(1,len(dfs_new)):
	#print(dfs_new[i])
	df_combined = pd.concat([df_combined,dfs_new[i]])

#print(df_combined['Medal'])

j=df_combined.groupby(['Discipline','Year','Country','Medal'],as_index=False).apply(lambda y:y[['Medal','Count']].to_dict("records")).reset_index().rename(columns={0:'Children'})
#j = j.groupby(['Discipline','Country'],as_index=False).agg(lambda x: x[['Children']].to_dict('r')).to_json(orient='records')       #.apply(lambda x: x[['Country','Children']].to_dict('records')).reset_index().rename(columns={0:'Children1'}).to_json(orient='records')


for i in range(0,len(j['Children'])):
	#print(j['Children'][i])
	j['Children'][i] = j['Children'][i][0]
#j['Children'] = j['Children'][0][0]
#print(j.head())

j=j.drop('Medal',axis=1)

#print(j.head())

j = j.groupby(['Discipline','Year','Country'],as_index=False)['Children'].apply(list)
#print(type(j.reset_index()))
j=j.reset_index().rename(columns={0:'Children'})

#print(j.head())


j=j.groupby(['Discipline','Year','Country'],as_index=False).apply(lambda y:y[['Country','Children']].to_dict("records")).reset_index().rename(columns={0:'Children'})
#j = j.groupby(['Discipline','Country'],as_index=False).agg(lambda x: x[['Children']].to_dict('r')).to_json(orient='records')       #.apply(lambda x: x[['Country','Children']].to_dict('records')).reset_index().rename(columns={0:'Children1'}).to_json(orient='records')


for i in range(0,len(j['Children'])):
	#print(j['Children'][i])
	j['Children'][i] = j['Children'][i][0]
#j['Children'] = j['Children'][0][0]
#print(j.head())


j=j.drop('Country',axis=1)

j = j.groupby(['Discipline','Year'],as_index=False)['Children'].apply(list)
#print(type(j.reset_index()))
j=j.reset_index().rename(columns={0:'Children'})

#print(j.head())

j = j.groupby(['Discipline','Year'],as_index=False).apply(lambda x: x[['Year','Children']].to_dict('records')).reset_index().rename(columns={0:'Children'})


for i in range(0,len(j['Children'])):
	j['Children'][i] = j['Children'][i][0]

#print(j.head())



#j=j.drop('Country',axis=1)

j = j.groupby(['Discipline'],as_index=True)['Children'].apply(list)
#print(type(j.reset_index()))
j=j.reset_index().rename(columns={0:'Children'})

#print(j.head())
j = j.groupby(['Discipline'],as_index=True).apply(lambda x: x[['Discipline','Children']].to_dict('records')).reset_index().rename(columns={0:'Children'}).to_json(orient='records')


print(json.dumps(json.loads(j), indent=2, sort_keys=True))


with open('data_bubble_year_country.json', 'w') as outfile:
    json.dump(json.loads(j), outfile)










