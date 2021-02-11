import glob
import os

list_of_files = glob.glob("*upgrade*.yml")
print("number of migrations : ", len(list_of_files))

list_of_migrations = [x[x.find("upgrade"):-4] for x in list_of_files]
#print(list_of_migrations)

dict_of_migrations = {}
for file_i, filename in enumerate(list_of_files):
    #print(filename)
    with open(filename, 'r') as f:
        data = f.read()
        start_index = data.find("migration_dependencies")
        for i, migration_name in enumerate(list_of_migrations):
            outer_migration = filename[filename.find("upgrade"):-4]
            if outer_migration not in dict_of_migrations.keys():
                dict_of_migrations[outer_migration] = []
            if outer_migration != migration_name:
                if data[start_index:].find(migration_name) != -1:
                    dict_of_migrations[outer_migration].append(migration_name)

##############################################
fulfilled_dep_list = []
# for no dependecy migrations
counter_dep0 = 0
dep0_list = []
f = open("dep0.txt", "w+")
for key, val in dict_of_migrations.items():
    if val == []:
        counter_dep0 += 1
        dep0_list.append(key)
        #fulfilled_dep_list.append(key)
        f.write("ddev drush mim "+str(key)+"; ")
    #print("--", val, " ==== ", key)
    #print("---------------------------------------")
#print("migrations with no dependencies nor any optional dependencies ", counter_dep0)
print(counter_dep0, " migrations with fulfilled dependencies in file - dep"+str(0)+".txt")
fulfilled_dep_list = dep0_list

################################################
migration_level = 1
while 1:
    # for migrations with dependency completed before
    counter_dep1 = 0
    dep1_list = []
    f = open("dep"+str(migration_level)+".txt", "w+")
    for key, val in dict_of_migrations.items():
        if key not in fulfilled_dep_list: #if val != []:
            dependency_check = True
            for migration in val:
                if migration not in fulfilled_dep_list:
                    dependency_check = False
            if dependency_check:
                counter_dep1 += 1
                dep1_list.append(key)
                #fulfilled_dep_list.append(key)
                f.write("ddev drush mim "+str(key)+"; ")
    fulfilled_dep_list = fulfilled_dep_list+dep1_list
    if counter_dep1 <= 0:
        try:
            os.remove("dep"+str(migration_level)+".txt")
        except OSError:
            pass
        break
    else:
        print(counter_dep1, " migrations with fulfilled dependencies in file - dep"+str(migration_level)+".txt")
    migration_level += 1

print("migrations put into txt files :", len(fulfilled_dep_list))

################################################
print("-------migrations with unfulfilled dependencies-------")
count = 0
list_of_unfulfilled_migrations = []
for val in list_of_migrations:
    if val not in fulfilled_dep_list:
        #print(val)
        list_of_unfulfilled_migrations.append(val)
        count += 1

print("count of unfulfilled migrations : ", count)

# getting only the dependency for these; ignoring optional
dict_of_unfulfilled_migrations = {}
count = 0
for file_i, filename in enumerate(list_of_files):
    #print(filename)
    outer_migration = filename[filename.find("upgrade"):-4]
    if outer_migration not in list_of_unfulfilled_migrations:
        continue
    count += 1
    with open(filename, 'r') as f:
        data = f.read()
        start_index = data.find("migration_dependencies")
        end_index = data.rfind("optional:")
        for i, migration_name in enumerate(list_of_migrations):
            if outer_migration not in dict_of_unfulfilled_migrations.keys():
                dict_of_unfulfilled_migrations[outer_migration] = []
            if filename != migration_name:
                if data[start_index:end_index].find(migration_name) != -1:
                    dict_of_unfulfilled_migrations[outer_migration].append(migration_name)
        #print("--",dict_of_unfulfilled_migrations[outer_migration])
#print("unfulfilled migrations counted : ", count)

while 1:
    # for migrations with dependency completed before
    counter_dep1 = 0
    dep1_list = []
    f = open("dep"+str(migration_level)+".txt", "w+")
    for key, val in dict_of_unfulfilled_migrations.items():
        if key not in fulfilled_dep_list: #if val != []:
            dependency_check = True
            for migration in val:
                if migration not in fulfilled_dep_list:
                    dependency_check = False
            if dependency_check:
                counter_dep1 += 1
                dep1_list.append(key)
                #fulfilled_dep_list.append(key)
                f.write("ddev drush mim "+str(key)+"; ")
    fulfilled_dep_list = fulfilled_dep_list+dep1_list
    if counter_dep1 <= 0:
        try:
            os.remove("dep"+str(migration_level)+".txt")
        except OSError:
            pass
        break
    else:
        print(counter_dep1, " migrations with fulfilled dependencies in file - dep"+str(migration_level)+".txt")
    migration_level += 1

###########################################
print("-------final tally--------")
print("input migrations         = ", len(list_of_files))
print("migrations accounted for = ", len(fulfilled_dep_list))
