### Requirements:
- podman or docker
- python3 and pip
- linux (as always)

### Define the environment variables:
Define your environment variables:
```shell
export MYSQL_ROOT_PASSWORD="root"
export MYSQL_EXTERNAL_IP="10.2.1.32"
export MYSQL_EXTERNAL_PORT="3306"
export DATABASE_CONTANER_NAME="mysql"
export GRAFANA_CONTANER_NAME="grafana"
export DATABASE_NAME="db01"

# CSV file separator:
export CSV_SEPARATOR=";"

# Type of all columns:
export COLUMN_TYPE="VARCHAR(255)"
export DB_TABLE_NAME="example"
export CSV_FILE_NAME="example.csv"

# To specify the column index to be chosen as primary key: use -1 to disable this option
export PRIM_KEY_COL_INDEX="0"
```

### Create mariadb container:
```shell

# Remove mysql container, if exists:
podman stop ${DATABASE_CONTANER_NAME} &>/dev/null 
podman rm ${DATABASE_CONTANER_NAME} &>/dev/null

# Start container:
podman run -dt -e MYSQL_ROOT_PASSWORD=root \
    -e MYSQL_DATABASE=${DATABASE_NAME} \
    --name ${DATABASE_CONTANER_NAME} \
    -p ${MYSQL_EXTERNAL_IP}:${MYSQL_EXTERNAL_PORT}:3306 docker.io/mysql:latest
```

Wait until container is UP and check the application (check with `podman logs -f <container name>`):
```shell

mysql -u root -p${MYSQL_ROOT_PASSWORD} -P ${MYSQL_EXTERNAL_PORT} -h ${MYSQL_EXTERNAL_IP} ${DATABASE_NAME}
```


### Create Grafana container:
```shell

# Remove container, if exists:
podman stop ${GRAFANA_CONTANER_NAME} &>/dev/null 
podman rm ${GRAFANA_CONTANER_NAME} &>/dev/null

# Start container:
podman run -dt \
    --name ${GRAFANA_CONTANER_NAME} \
    -p 3000:3000 docker.io/grafana/grafana-enterprise
```

### Create an example csv data:
```shell
cat << EOF > example.csv
date;voltage;power
2020-10-04 15:00:00;10;10
2020-10-04 15:15:00;14;14
2020-10-04 15:30:00;15;20
2020-10-04 15:45:00;16;16
2020-10-04 16:00:00;8;16
2020-10-04 16:15:00;7;17
2020-10-04 16:30:00;5;18
2020-10-04 16:45:00;14;50
2020-10-04 17:00:00;16;10
2020-10-04 17:15:00;19;22
2020-10-04 17:30:00;20;13
2020-10-04 17:45:00;18;44
EOF

```

### Load CSV to mariadb:
```shell
python3 send_data.py
```

