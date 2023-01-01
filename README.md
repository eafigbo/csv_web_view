# csv_web_view
A small hack project for viewing csv files on a browser and assigning a score to each record.
Comes in handy when you have a a large spreadsheet of records that you want to score.

I built this tool when I had to review a spreadsheet of more than 1000 records and had to create a shortlist of about 100 of them.
Doing that on a spreadsheet was very painful and so I built this tool to enable me easily page through them, view the records one by one , page through them with my keyboard and assign scores to them.

It is built with Python and MongoDB.


## Running the tool

To run this tool, you first need to install MongoDB by following the instructions on the [MongoDB website](https://www.mongodb.com/docs/manual/installation/)

Clone this repo and then enter into this directory:
```bash
git clone git@github.com:eafigbo/csv_web_view.git
cd csv_web_view

```
edit project_settings.py to suit your project / platform preferences 

Then install dependencies:

```bash
pip3 install -r requirements.txt
python3 main.py

```
point your browser to http://localhost:8080/




