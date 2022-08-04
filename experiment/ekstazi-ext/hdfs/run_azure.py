import os, shutil, time, sys
cur_path = os.getcwd()
non_ctest_list = "nonCtestList"
project_url = "https://github.com/apache/hadoop.git"
project_path = os.path.join(cur_path, "hadoop")
project_module = "hadoop-hdfs-project/hadoop-hdfs"
project_module_path = os.path.join(project_path, project_module)
api_file_path = os.path.join(project_path, "hadoop-common-project/hadoop-common/src/main/java/org/apache/hadoop/conf/Configuration.java")
hdfs_config_api_file_path = os.path.join(project_path, "hadoop-hdfs-project/hadoop-hdfs-client/src/main/java/org/apache/hadoop/hdfs/HdfsConfiguration.java")
api_pom_file_path = os.path.join(project_path, "hadoop-common-project/hadoop-common/pom.xml")
hdfs_pom_file_path = os.path.join(project_module_path, "pom.xml")
#time_file_path = os.path.join(cur_path, "time.txt")
#test_class_num_file_path = os.path.join(cur_path, "test_class_num.txt")
ctest_configuration_file_path = os.path.join(project_module_path, "src/main/resources/hdfs-ctest.xml")
default_configuration_file_path = os.path.join(project_module_path, "src/main/resources/hdfs-default.xml")
production_configuration_file_path = os.path.join(project_module_path, "production-configuration.xml")
commits = ["1576f81dfe0156514ec06b6051e5df7928a294e2", "c665ab02ed5c400b0c5e9e350686cd0e5b5e6972", "028ec4704b9323954c091bcda3433f7b79cb61de", "832a3c6a8918c73fa85518d5223df65b48f706e9", "3fdeb7435add3593a0a367fff6e8622a73ad9fa3", "98a74e23514392dc8859f407cd40d9c96d8c5923", "1abd03d68f4f236674ce929164cc460037730abb", "8ce30f51f999c0a80db53a2a96b5be5505d4d151", "bce14e746b3d00e692820f28b72ffe306f74d0b2", "b8ab19373d1a291b5faa9944e545b6d5c812a6eb"]
configuration_list = ["core-default.xml", "prod1.xml", "prod2.xml"]
mvn_cmd = "mvn ekstazi:ekstazi -DfailIfNoTests=false | tee out.txt"
mvn_clean_cmd = "mvn ekstazi:clean"
prod1_config_changed_commit = ["c665ab02ed5c400b0c5e9e350686cd0e5b5e6972", "98a74e23514392dc8859f407cd40d9c96d8c5923", "1abd03d68f4f236674ce929164cc460037730abb"]
prod2_config_changed_commit = ["832a3c6a8918c73fa85518d5223df65b48f706e9", "b8ab19373d1a291b5faa9944e545b6d5c812a6eb"]
config_changed_commit = {"prod1":prod1_config_changed_commit, "prod2":prod2_config_changed_commit}

DEBUG_PREFIX="===============[Ekstazi-ext Evaluation: "

# Clone testing project
def clone():
    if os.path.exists(project_path):
        shutil.rmtree(project_path)
    clone_cmd = "git clone " + project_url
    os.system(clone_cmd)


# Record the experiment time
def record_time(elapsed_time, curConfig, curCommit):
    print("{}TOTAL_TIME: {}-{} : {}s\n".format(DEBUG_PREFIX, curConfig, curCommit, elapsed_time), flush=True)
#     with open(time_file_path, 'a') as f:
#         f.write("{}-{} : {}s\n".format(curConfig, curCommit, elapsed_time))


# def record_test_class_number(curConfig, curCommit):
#     os.chdir(project_module_path)
#     p = os.popen("grep 'Tests ' out.txt | sed -e 's/^.*Tests //' -e 's/.\[0;1;32m//' -e 's/.\[m//' -e 's/.\[1m//' -e 's/.\[0;1m//g' -e 's/.\[m//g' | sed -n 's/run: \([1-9][0-9]*\),.*- in \(.*\)/\2     \1/p' | wc -l")
#     with open(test_class_num_file_path, 'a') as f:
#         f.write("{}-{} : {}\n".format(curConfig, curCommit, int(p.read())))
#     os.chdir(cur_path)


# Copy the production configuration to the project for configuration tests
def copy_production_config_file(config_file_name):
    replaced_config_file_path = os.path.join(cur_path, "../../config_files/hdfs/", config_file_name)
    shutil.copy(replaced_config_file_path, production_configuration_file_path)


# Run tests
def run_test(curConfig, curCommit):
    os.chdir(project_module_path)
    start = time.time()
    os.system(mvn_cmd)
    end = time.time()
    record_time(end - start, curConfig, curCommit)
    os.chdir(cur_path)


# Checkout Revision and install
def checkout_commit(commit):
    os.chdir(project_path)
    os.system("git checkout -f " + commit)
    os.chdir(cur_path)


# Install Project
def maven_install():
    os.chdir(project_path)
    os.system("mvn clean install -DskipTests -am -pl " + project_module)
    os.chdir(cur_path)
    

# Production configuration only execute ctest (i.e., configuration test)
# Exclude non-ctest in maven-surefire for production round
# Default round still runs the whole test suite (regular test + ctest)
def exclude_non_ctest():
    excludeLines = []
    with open(non_ctest_list, 'r') as f:
        excludeLines = f.readlines()
    pom_lines = []
    with open(hdfs_pom_file_path, 'r') as f:
        for line in f:
            pom_lines.append(line)
    with open(hdfs_pom_file_path, 'w') as f:
        surefire_pos_flag = False
        for line in pom_lines:
            f.write(line)
            if "<artifactId>maven-surefire-plugin</artifactId>" in line:
                surefire_pos_flag = True
            if surefire_pos_flag and "<configuration>" in line:
                f.write("".join(excludeLines))
                f.write("\n")
                surefire_pos_flag = False


# Add ekstazi maven plugin and use 'mvn ekstazi:ekstazi'
# with instrumented JUnit Runner to dynamically set 
# production configuration value for ctest.
def add_ekstazi_runner_pom():
    plugin = "<plugin>\n" \
             "<groupId>org.ekstazi</groupId>\n" \
             "<artifactId>ekstazi-maven-plugin</artifactId>\n" \
             "<version>5.3.1-SNAPSHOT</version>\n" \
             "</plugin>\n"
    lines = []
    with open(hdfs_pom_file_path, 'r') as f:
        for line in f:
            lines.append(line)

    with open(hdfs_pom_file_path, 'w') as f:
        for line in lines:
            f.write(line)
            if "<plugins>" in line:
                f.write(plugin)


# Add ctest configuration file to project API
def modify_config_api_to_add_ctest_file():
    lines = []
    successInsert = False
    with open(hdfs_config_api_file_path, 'r') as f:
        for line in f:
            lines.append(line)
    
    with open(hdfs_config_api_file_path, 'w') as f:
        for line in lines:
            f.write(line)
            if "package org.apache.hadoop.hdfs" in line:
                f.write("import java.lang.management.ManagementFactory;\n")
            if "Configuration.addDefaultResource(\"hdfs-rbf-site.xml\");" in line:
                f.write('    String pid = ManagementFactory.getRuntimeMXBean().getName().split("@")[0]; //UNIFY_TESTS\n')
                f.write('    Configuration.addDefaultResource("hdfs-ctest-" + pid + ".xml"); //UNIFY_TESTS\n')
                successInsert = True
    
    if not successInsert:
        lines = []
        with open(hdfs_config_api_file_path, 'r') as f:
            for line in f:
                lines.append(line)

        with open(hdfs_config_api_file_path, 'w') as f:
            for line in lines:
                f.write(line)
                if "package org.apache.hadoop.hdfs" in line:
                    f.write("import java.lang.management.ManagementFactory;\n")
                if "Configuration.addDefaultResource(\"hdfs-site.xml\");" in line:
                    f.write('    String pid = ManagementFactory.getRuntimeMXBean().getName().split("@")[0]; //UNIFY_TESTS\n')
                    f.write('    Configuration.addDefaultResource("hdfs-ctest-" + pid + ".xml"); //UNIFY_TESTS\n')
                    successInsert = True
    
    if not successInsert:
        raise ValueError("Can't insert into HDFSConfiguration.java ")


# Prepare injection file
def create_empty_config_file_for_running_ctest():
    source_path = os.path.join(cur_path, "hdfs-ctest.xml")
    shutil.copy(source_path, ctest_configuration_file_path)


# Prepare mapping
def copy_config_mapping():
    source_path = os.path.join(cur_path, "mapping")
    target_path = os.path.join(project_module_path, "mapping")
    shutil.copy(source_path, target_path)


# Prepare ekstazi config file
def prepare_ekstazi_config_file():
    source_path = os.path.join(cur_path, ".ekstazirc")
    target_path = os.path.join(project_module_path, ".ekstazirc")
    shutil.copy(source_path, target_path)


def mimic_config_file_change(curCommit, cur_config_name):
    for commit in config_changed_commit[cur_config_name]:
        if commits.index(curCommit) >= commits.index(commit):
            with open(default_configuration_file_path, 'a') as f:
                f.write(" <!-- {} -->\n".format(commit))


# Prepare environment and all files
def do_preparation(curCommit, cur_config_name):
    checkout_commit(curCommit)
    modify_config_api_to_add_ctest_file()
    create_empty_config_file_for_running_ctest()
    copy_config_mapping()
    prepare_ekstazi_config_file()
    add_ekstazi_runner_pom()
    if cur_config_name != "core-default":
        mimic_config_file_change(curCommit, cur_config_name)
    maven_install()


def copy_dependency_folder(curCommit, cur_config_name):
    if not os.path.exists(os.path.join(cur_path, "dependency_folder")):
        os.makedirs(os.path.join(cur_path, "dependency_folder"))
    source_path = os.path.join(project_module_path, ".ekstazi")
    target_path = os.path.join(cur_path, "dependency_folder", cur_config_name + "-" + curCommit)
    if os.path.exists(target_path):
        shutil.rmtree(target_path)
    shutil.copytree(source_path, target_path)


def clean_dependency_folder():
    os.chdir(project_module_path)
    os.system(mvn_clean_cmd)
    os.chdir(cur_path)


def run(argv):
    clone()
    commits_to_run=[argv[1], argv[2]]
    for i in range(len(configuration_list)):
        for curCommit in commits_to_run:
            curConfig = configuration_list[i]
            cur_config_name = curConfig.split(".")[0]
            config_file_name = curConfig + "-" + curCommit
            do_preparation(curCommit, cur_config_name)
            if cur_config_name != "core-default":
                exclude_non_ctest()
            copy_production_config_file(config_file_name)
            print(DEBUG_PREFIX + curCommit + " Config: " + cur_config_name + " ===============", flush=True)
            run_test(curConfig, curCommit)
            # record_test_class_number(curConfig, curCommit)
            # copy_dependency_folder(curCommit, cur_config_name)
        clean_dependency_folder()


if __name__ == '__main__':
    run(sys.argv)