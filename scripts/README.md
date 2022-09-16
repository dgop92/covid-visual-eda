# Scripts

Scripts to populate mongo db

Note: Execute from the root folder, and make sure to create the data folder
with the respective [Covid Data](https://ourworldindata.org/covid-deaths)

## Order of Execution

For countries

```
python -m scripts.countries.create_countries_csv
python -m scripts.countries.save_countries
```
