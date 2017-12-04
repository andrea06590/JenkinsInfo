#!/usr/bin python3.6

import argparse
import yaml
import requests
import json
import datetime

# stocke les @ des serveurs en vue d'une autre utilisation
serverList = []
# json response
jsonResp = {}
# après parsing
formattedJenkinsObj = [{}]
formattedJenkinsJobs = [{}]


def printInfo():
    print("Run jenkins-list.py -c config.yaml -list to see all Jobs")
    print("or run jenkins-list.py -c config.yaml -info [jobName]")


def dispatchRequest():
    # si on requete tous les jobs
    if args.list:
        getAllJobs(serverList[1])

    # si on veut un job en particulier
    if args.jobName:
        getJobInfo(serverList[0], args.jobName)


# utilisation du serveur ALL (server2 du fichier conf)
def getAllJobs(server):
    print('Server requested : ' + server + '...')
    resp = requests.get(server)
    jsonResp = json.loads(resp.text)
    for value in jsonResp['jobs']:
        getJobInfo(serverList[0], value['name'])

# utilisation de l'url API (server1 du fichier conf) fournie par jenkins
def getJobInfo(server, jobName):
    url = server + jobName + '/api/json?tree=builds[fullDisplayName,url,timestamp,result,runs[builtOn]]'
    print('Get job : ' + jobName + ' on server : ' + server + '...')
    resp = requests.get(url)
    jsonResp = json.loads(resp.text)

    if 'builds' in jsonResp:
        for value in jsonResp['builds']:
            time = value['timestamp']/1000
            pattern = '%Y-%m-%d %H:%M:%S'
            formatted = datetime.datetime.fromtimestamp(time).strftime(pattern)
            if 'runs' in value:
                for run in value['runs']:
                    job = {
                        'time': formatted,
                        'build url': value['url'],
                        'status': value['result'],
                        'name': value['fullDisplayName'],
                        'node': run['builtOn']
                    }
                    formattedJenkinsJobs.append(job)
            else:
                job = {
                    'time': formatted,
                    'build url': value['url'],
                    'status': value['result'],
                    'name': value['fullDisplayName'],
                    'node': 'master'
                }
                formattedJenkinsJobs.append(job)
            print(job)

parser = argparse.ArgumentParser(description="collecte jenkins")
parser.add_argument("-c", dest="filename", help="config file with servers")

options = parser.add_argument_group('options')
options.add_argument("-list", action='store_true', help="get all jobs")
options.add_argument("-info", dest="jobName", help="get specific job info")

args = parser.parse_args()

# on lis le fichier de conf avant toute chose
# TODO gestion d'erreur si mauvais fichier ou inexistant sur le fs
if args.filename is not None:
    print("Fichier : " + args.filename)
    with open(args.filename, 'r') as stream:
        try:
            config = yaml.load(stream)
            for key in config['SERVERS']:
                serverList.append(config['SERVERS'][key])
            printInfo()
            dispatchRequest()
            print(serverList)
        except yaml.YAMLError as exception:
            print(exception)
else:
    print('Config file required\n')
    printInfo()
