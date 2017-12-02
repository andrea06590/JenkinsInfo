#!/usr/bin python3.6

import argparse
import yaml
import requests
import json

# stocke les @ des serveurs en vue d'une autre utilisation
serverList = []
# json response
jsonResp = {}
# après parsing
formattedJenkinsObj = [{}]
formattedJenkinsJobs = [{}]


# utilisation du serveur ALL (server2 du fichier conf)
def getAllJobs(server):
    print('Server requested : ' + server + '...')
    resp = requests.get(server)
    jsonResp = json.loads(resp.text)
    for value in jsonResp['jobs']:
        job = {
            'jobName': value['name'],
            'url': value['url']
        }
        print("Job Name : " + job['jobName'] + "  =>  Job url : " + job['url'])
        formattedJenkinsObj.append(job)


# utilisation de l'url API (server1 du fichier conf) fournie par jenkins
def getJobInfo(server, jobName):
    url = server + jobName + '/api/json?tree=builds[url,timestamp,result]'
    print('Get job : ' + jobName + ' on server : ' + server + '...')
    resp = requests.get(url)
    jsonResp = json.loads(resp.text)
    for value in jsonResp['builds']:
        job = {
            'time': value['timestamp'],
            'node': value['url'],
            'status': value['result']
        }
        print(job)
        formattedJenkinsJobs.append(job)

parser = argparse.ArgumentParser(description="collecte jenkins")
parser.add_argument("-c", dest="filename", help="config file with servers")

options = parser.add_argument_group('options')
options.add_argument("-list", action='store_true', help="get all jobs")
options.add_argument("-info", dest="jobName", help="get specific job info")

args = parser.parse_args()

# on lis le fichier de conf avant toute chose
# TODO gestion d'erreur si mauvais fichier ou inexistant sur le fs
print("Fichier : " + args.filename)
with open(args.filename, 'r') as stream:
    try:
        config = yaml.load(stream)
        for key in config['SERVERS']:
            serverList.append(config['SERVERS'][key])
        print(serverList)
    except yaml.YAMLError as exception:
        print(exception)


# si on requete tous les jobs
if args.list:
    getAllJobs(serverList[1])

# si on veut un job en particulier
if args.jobName:
    getJobInfo(serverList[0], args.jobName)
