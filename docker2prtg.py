#!/usr/bin/python3
# coding: utf-8

import pandas as pd
from jinja2 import Template
import subprocess
from io import StringIO
import re
import sys


#configuration
dockerBinary = "/usr/bin/docker"


#parse docker fields
def parseDockerStatsFields(cmd):
    return re.findall(r'{{\.([a-zA-Z0-9]*)\}}',cmd)

	
#cleanupValues
def cleanupVals(row):
    if row.get('CPUPerc') is not None:
        row['CPUPerc'] = row['CPUPerc'].replace("%","").strip()

    if row.get('MemUsage') is not None:
        row['MemUsage'] = row['MemUsage'].split("/")[0].replace("MiB","").strip()
    return row


#get docker stats
def getDockerStats(fields):
    cmd = dockerBinary + ' stats --no-stream --format "'+fields+'"'
    stats = subprocess.run(cmd.split(), stdout=subprocess.PIPE).stdout.decode('utf-8').replace('"','')
    dockerStatsFields = parseDockerStatsFields(cmd)
    dockerStats = pd.read_csv(StringIO(stats), names = dockerStatsFields, header = None, sep=';', index_col = False)
    dockerStats = dockerStats.apply(cleanupVals,axis=1)
    dockerStats = dockerStats.to_dict(orient='records')
    return {'data':dockerStats}


#define xml template
def buildXML(dockerStats):
    template = Template("""
    <?xml version="1.0" encoding="Windows-1252" ?>
    <prtg>
        {%for stat in dockerStats.data %}<result>
            <channel>{{stat.Name}} {{dockerStats.fieldName}}</channel>
            <value>{{stat[dockerStats.fieldName]}}</value>
        </result>{% endfor %}
    </prtg>
    """)
    rendered = template.render({'dockerStats':dockerStats})
    return rendered

#render xml template
def renderDockerStats(dockerStats,fieldName):
    dockerStats.update({'fieldName':fieldName})
    return buildXML(dockerStats)


#main
def main(argv):
    fields = "{{.Name}};{{.Container}};{{.CPUPerc}};{{.MemUsage}};{{.NetIO}}"

    if len(argv) > 1:
        selectedField = argv[1]
        dockerStats = getDockerStats(fields)
        renderedDockerStats = renderDockerStats(dockerStats,selectedField)
        print(renderedDockerStats)
    else:
        availableFields = parseDockerStatsFields(fields)
        print("Select one of the available fields {} and pass it as an argument to the script".format([x for x in availableFields if x not in ['Name','Container']]))
        print("docker2prtg.py <field>")
if __name__ == "__main__":
    main(sys.argv)
