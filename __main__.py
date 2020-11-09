import os
import io
import sys
import json
from distutils.dir_util import copy_tree
from tools import fdb_to_sqlite
from os import system, name 

def clear():

    if name == 'nt': 
        _ = system('cls') 
    else: 
        _ = system('clear')



def setup_resources():
    print("Welcome to the Setup tool for OpenLU\n")
    print("Some pre requisites are required before we start")
    print("1. OpenLU: https://github.com/MashedTatoes/OpenLU\n")
    print("2. Lego Universe unpacked client: https://docs.google.com/document/d/1XmHXWuUQqzUIOcv6SVVjaNBm4bFg9lnW4Pk1pllimEg/edit\n\t(humanoid/lcdr’s unpacked client reccomended)")
    print("3. MySql: https://dev.mysql.com/downloads/mysql/")
    
    input("Once you are ready to continue press any key")
    global openluResDir 
    openluResDir = "OpenLU/Resources"
    if sys.platform == "win32":
            appdir = os.getenv('APPDATA')
            openluResDir = os.path.join(appdir,openluResDir)
            if os.path.isdir(openluResDir) == False:
                print("Making OpenLU resource directory at '%s'\n" % openluResDir)
                os.makedirs(openluResDir)
    

    luClientResDir = ""
    while os.path.isdir(luClientResDir) == False or luClientResDir == "":
        clear()
        print("Please input the path of the res directory in you Lego Universe client\n")
        luClientResDir = input(">>")
    
    usr_input = ""
    while usr_input.lower() != "y" and usr_input.lower() != "n" :
        print("{} needs to be copied to {}\ndo you want to do this step automatically[y/n]? (Could take a few minutes)\n".format(  luClientResDir,  openluResDir))
        usr_input = input(">>")
        clear()
    
    if usr_input.lower() == "y" :
        print("Copying client resource files to OpenLU Resource directory...")
        copy_tree(luClientResDir,openluResDir)
        print("Done!")
        input("Press any key to continue")
        clear()
    else:
        input("Skipped copying resources\nPlease do it manually\nOnce you are dont press any key to continue")
    if os.path.exists("%s/cdclient.fdb"% openluResDir) and os.path.exists("%s/cdclient.db"% openluResDir) == False:
        print("Creating client sqlite database")
        in_path = "%s/cdclient.fdb" % openluResDir
        out_path= "%s/cdclient.db" % openluResDir
        fdb_to_sqlite.start(in_path,out_path)
    input("Finished setting up Resources\nPress any key to continue")

def setup_db():
    input("Press enter to start database setup")
    accepted_db = ["mysql","sqlite"]
    global user_db
    user_db = ""

    while (user_db.lower() in accepted_db) == False:
        clear()
        print("Input sql provider, accpeted providers are:\n")
        for db in accepted_db:
            print(db)
        user_db = input(">>")
    clear()
    
    global connection_string
    
    ok = False
    while ok == False:
        clear()
        if user_db == "mysql":
            print("Please follow the prompts to create your connection string")
            connection_string = "server={};database={};user id={};password={};persistsecurityinfo=True;port={}"
        
            server_ip = input("Enter mysql server address >> ")
            database = input("Enter mysql database name >> ")
            user_id = input("Enter mysql database user id >> ")
            pwd = input("Enter my sql database password >> ")
            port = input("Enter mysql server port (leave blank for 3306) >> ")
            if port == "" or port == None:
                port = 3306
            connection_string = connection_string.format(server_ip,database,user_id,pwd,port)
        usr_input = ""
        while usr_input.lower() != "y" and usr_input.lower() != "n" :
            print("Your connection string is %s\nis this ok? [y/n]" % connection_string)
            usr_input = input(">>")
            clear()
        if usr_input.lower() == "y":
            ok = True

def setup_cfg():
    input("Press any to setup OpenLU configuration file (last step!)")
    
    openlu_install = ""
    while os.path.isdir(openlu_install) == False or openlu_install == "":
        clear()
        print("Enter OpenLU install directory (containing OpenLU.sln)")
        openlu_install = input(">>")
    config_file = {
        "connectionString" : connection_string,
        "luResources" : openluResDir,
        "provider" : user_db
    }
    cfg_sln = "%s/OpenLU.Configuration" % openlu_install
    if os.path.isdir(cfg_sln):
        cfg_file = None
        cfg_file_path = "%s/cfg.json" % cfg_sln
        if os.path.exists(cfg_sln):
            cfg_file = open(cfg_file_path,"w")
        else :
            cfg_file = open(cfg_file_path,"x")
        cfg_file.write(json.dumps(config_file))
        cfg_file.close()
        print("Config file save to %s" % cfg_file_path)
    else:
        print("Could not find OpenLU.Configuration\nExiting...")



if __name__ == "__main__":
    setup_resources()
    setup_db()
    setup_cfg()
    


    
