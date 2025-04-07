from dash import Dash, dcc, html
import pandas as pd
import plotly.express as px

all_countries = ['Afghanistan', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola',
 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia',
 'Austria', 'Azerbaijan', 'Bahamas, The', 'Bahrain', 'Bangladesh',
 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan',
 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil',
 'British Virgin Islands', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso',
 'Burundi', 'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada',
 'Cayman Islands', 'Central African Republic', 'Chad', 'Channel Islands',
 'Chile', 'China', 'Colombia', 'Comoros', 'Congo, Dem. Rep.',
 'Congo, Rep.', 'Costa Rica', "Cote d'Ivoire", 'Croatia', 'Cuba',
 'Curacao', 'Cyprus', 'Czechia', 'Denmark', 'Djibouti', 'Dominica',
 'Dominican Republic', 'Ecuador', 'Egypt, Arab Rep.', 'El Salvador',
 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia',
 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Polynesia',
 'Gabon', 'Gambia, The', 'Georgia', 'Germany', 'Ghana', 'Gibraltar',
 'Greece', 'Greenland', 'Grenada', 'Guam', 'Guatemala', 'Guinea',
 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hong Kong SAR, China',
 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran, Islamic Rep.',
 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan',
 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', "Korea, Dem. People's Rep.",
 'Korea, Rep.', 'Kosovo', 'Kuwait', 'Kyrgyz Republic', 'Lao PDR',
 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein',
 'Lithuania', 'Luxembourg', 'Macao SAR, China', 'Madagascar', 'Malawi',
 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands',
 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia, Fed. Sts.', 'Moldova',
 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar',
 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia',
 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Macedonia',
 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau',
 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines',
 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Romania',
 'Russian Federation', 'Rwanda', 'Samoa', 'San Marino',
 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia',
 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten (Dutch part)',
 'Slovak Republic', 'Slovenia', 'Solomon Islands', 'Somalia',
 'South Africa', 'South Sudan', 'Spain', 'Sri Lanka',
 'St. Kitts and Nevis', 'St. Lucia', 'St. Martin (French part)',
 'St. Vincent and the Grenadines', 'Sudan', 'Suriname', 'Sweden',
 'Switzerland', 'Syrian Arab Republic', 'Tajikistan', 'Tanzania',
 'Thailand', 'Timor-Leste', 'Togo', 'Tonga', 'Trinidad and Tobago',
 'Tunisia', 'Turkiye', 'Turkmenistan', 'Turks and Caicos Islands',
 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates',
 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu',
 'Venezuela, RB', 'Viet Nam', 'Virgin Islands (U.S.)',
 'West Bank and Gaza', 'Yemen, Rep.', 'Zambia', 'Zimbabwe']


def render(app: Dash, dataset: pd.DataFrame) -> html.Div:
    refugiee_df = dataset[['country', 'year', 'Refugiee_Population']]
    refugiee_df = refugiee_df[(refugiee_df['year'].isin([2020, 2023])) & (refugiee_df['country'].isin(all_countries))]
    refugiee_df_pivot = refugiee_df.pivot(index='country', columns='year', values='Refugiee_Population').reset_index()
    refugiee_df_pivot['rate growth'] = (refugiee_df_pivot[2023] - refugiee_df_pivot[2020]) / refugiee_df_pivot[2020] * 100
    top_refugiee_countries = refugiee_df_pivot.nlargest(5, 'rate growth')

    fig = px.bar(top_refugiee_countries, x='country', y='rate growth', title='Countries with the highest increase rate in the number of refugees between 2020 and 2023', 
             labels={'rate growth': 'Rate Growth', 'country': 'Country'},
             text='rate growth')

    fig.update_traces(texttemplate='+%{text:.2f}%', textposition='outside', textfont=dict(size=12), marker_color='royalblue')

    fig.update_layout(yaxis=dict(showticklabels=False, zeroline=False, range=[0, max(top_refugiee_countries['rate growth'].values)*1.1]))

    return html.Div(
            dcc.Graph(figure=fig), id='highest_refugiee_growths'
        )
    