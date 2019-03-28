#!/usr/bin/python
# -*- coding: utf-8 -*-


#Получение кластеров /opt/1C/v8.3/x86_64/rac cluster list
# Получение всех ИБ /opt/1C/v8.3/x86_64/rac infobase --cluster=92355c60-7ca1-11e8-6e92-005056aa5d96 --cluster-user=Администратор --cluster-pwd= summary list
#
# info
#        получение информации об информационной базе
#        --infobase=<uuid>
#            (обязательный) идентификатор информационной базы
#        --infobase-user=<name>
#            имя администратора информационной базы
#        --infobase-pwd=<pwd>
#            пароль администратора информационной базы
#
# summary
#        управление краткой информацией об информационных базах
#        Дополнительные команды:
#            info
#                получение краткой информации об указанной информационной базе
#                --infobase=<uuid>
#                    (обязательный) идентификатор информационной базы
#
#
# /opt/1C/v8.3/x86_64/rac infobase
#    --cluster=92355c60-7ca1-11e8-6e92-005056aa5d96
#    --cluster-user=Администратор
#    --cluster-pwd=
# info
#    --infobase=254bc53a-19e5-11e9-9c9a-005056aab707
#    --infobase-user=
#    --infobase-pwd=


import subprocess
import argparse
import sys
import re

def parse_infobases(response, filter, pass_dict):


    dict_id = []
    dict_name = []
    filtreddict = {}
    res = response.split("\n",)

    for str in res:
        s = str.replace(" ","")
        s = s.split(":")
        if s[0] == "infobase":
          dict_id.append(s[1])
    for str in res:
        s = str.replace(" ","")
        s = s.split(":")
        if s[0] == "name":
          dict_name.append(s[1])

    basedict = dict(zip(dict_name,dict_id))



    for list in basedict:
        if len(re.findall(filter,list)) > 0:
            lst = basedict.get(list)
            value = []
            value.append(lst)
            try:
              value.append(pass_dict[list][0])
            except:
              value.append("KBS")
            try:  
              value.append(pass_dict[list][1])
            except:
              value.append("pirania117KBS")  
            filtreddict.update({list:value})



    return filtreddict


def get_cluster_id():
    cluster_id_list = []
    result = None
    try:
      result = subprocess.check_output([prog, "cluster", "list",host]).decode("utf8").replace(" ","").split("\n")
    except:
      print(Exception)
    if result is not None:
      for str in result:
        cluster = str.split(":")
        if cluster[0] == "cluster":
          cluster_id_list.append(cluster[1])
    return cluster_id_list

def create_parameter_list(module, cluster_id, cluster_user_param,
                          cluster_pw_param, action, action2, ib, ib_user_param, ib_pw_param, additional_param, host):
  parameter_list = []
  parameter_list.append(prog)
  parameter_list.append(module)
  parameter_list.append("--cluster="+cluster_id)

  if cluster_user_param != "":
      parameter_list.append("--cluster-user="+cluster_user_param)

  if cluster_pw_param != "":
      parameter_list.append("--cluster-pwd="+cluster_pw_param)

  parameter_list.append(action)

  if action2 != "":
      parameter_list.append(action2)

  if ib != "":
      parameter_list.append("--infobase="+ib)

  if ib_user_param != "":
      parameter_list.append("--infobase-user="+ib_user_param)

  if ib_pw_param != "":
      parameter_list.append("--infobase-pwd="+ib_pw_param)

  if additional_param != "":
      parameter_list.append(additional_param)

  if host != "":
      parameter_list.append(host)

  return parameter_list

def create_password_dict():
    f = open("ib_pass.csv")
    password_dict = {}
    key = []
    value = []
    for line in f:
        line = line.replace("\n", "").split(",")
        key.append(line[0])
        tmp = []
        tmp.append(line[1])
        tmp.append(line[2])
        value.append(tmp)
        password_dict = dict(zip(key, value))
    return password_dict

if __name__ == '__main__':


    ib_user = ""
    ib_pw = ""
    cluster_id = ""
    cluster_user = "" #"Администратор"
    cluster_pw = ""
    host = "127.0.0.1"
    prog = "/opt/1C/v8.3/x86_64/rac"
    job_state_deny = "on"
    filter = "."



    cli_parser = argparse.ArgumentParser(description="Bulk change a scheduled job statuses in cluster")
    cli_parser.add_argument("-hst",dest="host",default=host,help="Ip address 1c cluster host")
    cli_parser.add_argument("-pth",dest="path",default=prog,help="local path to ./rac console command")
    cli_parser.add_argument("-iu", dest="ibuser",default=ib_user,help="Infobase administrative user, default is ")
    cli_parser.add_argument("-ip",dest="ibpassword",default=ib_pw,
                            help="Infobase administrative user password, default is "+ib_pw)
    cli_parser.add_argument("-cu",dest="cluser",default=cluster_user,
                            help="Cluster administrative user, default is " + cluster_user)
    cli_parser.add_argument("-i",dest="info",default="yes",
                            help="Get summary info about infobases, default 'yes'")
    cli_parser.add_argument("-f",dest="filter")
    args = cli_parser.parse_args()


    cluster_ids = get_cluster_id()
    if len(cluster_ids) !=0:
        cluster_id = cluster_ids[0]
    else:
        print("Не обнаружено ни одного кластера")
        sys.exit(1)
    if len(cluster_id) !=0:
        param = create_parameter_list("infobase",cluster_id,cluster_user,cluster_pw,"summary","list","","","","",host)
        proc_result = subprocess.check_output(param).decode("utf-8")
        print(proc_result)
    else:
        print("Не обнаружено ни одного кластера")
        sys.exit(1)
    try:
      passwords = create_password_dict()
    except:
      print(Exception)
    try:
      infobases_id_list =  parse_infobases(proc_result, filter, passwords)
    except:
      print(Exception)


    if args.info == "no":
      for ib_id in infobases_id_list:

        param = create_parameter_list("infobase",
                                      cluster_id,cluster_user,cluster_pw,
                                      "update", "",
                                      infobases_id_list[ib_id][0],infobases_id_list[ib_id][1],infobases_id_list[ib_id][2],
                                      "--scheduled-jobs-deny=off",
                                      host)
        try:
           subprocess.check_output(param)
           print("Состояние фонового задания изменено")
        except:
          print("Не удалось изменить состояние фоновых заданий")

    else:
        for ib_id in infobases_id_list:
            param = create_parameter_list("infobase",
                                          cluster_id, cluster_user, cluster_pw,
                                          "info", "",
                                          infobases_id_list[ib_id][0], infobases_id_list[ib_id][1], infobases_id_list[ib_id][2],"",host)
            try:
               print(subprocess.check_output(param).decode("utf-8"))
            except:
                print("Не удалось получить информацию об ИБ")
