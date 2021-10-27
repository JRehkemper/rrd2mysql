# rrd2mysql
This Tool uses the RRD Files From Smokeping and imports them into a SQL Database.

## Prerequisite
* Running Smokeping Service
* Running SQL Database
* rrdtool
* mysql-connector-python

### Database Table Structure
| Name      | Type      | Default             | Auto Increment |
|-----------|-----------|---------------------|----------------|
| timestamp | timestamp | current_timestamp() |                |
| id        | int       |                     | yes            |
| median    | float     |                     |                |
| ping1     | float     |                     |                |
| ping2     | float     |                     |                |
| ping3     | float     |                     |                |

Add as many ping-columns as you set pings in your Smokeping Config.

## Usage
Edit the Script and add your Database Credentials and the location of the RRD File at the top. You also need to set the amount of step (How often does your Smokeping ping).
After that you can simply run the Programm.
```bash
python3 rrd2mysql.py
```
The Programm will now write the newest entry in the RRD File into the Database. To exit use `Ctrl+C`  
__Only the last entry will be imported. Old Data will not be used__
